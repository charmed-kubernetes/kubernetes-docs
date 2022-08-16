from dataclasses import dataclass, fields, field
from datetime import datetime
from backports.cached_property import cached_property
import logging
import os
import re
from pathlib import Path
from subprocess import check_output
from typing import List
from urllib.request import urlopen

import semver
from github import Github
from jinja2 import Environment, PackageLoader, select_autoescape
import yaml


log = logging.getLogger(__name__)


def gh():
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        log.warning("Missing GITHUB_TOKEN. Without a token, github may rate limit.")
    return Github(token)


def _ver_to_tuple(ver):
    return tuple(int(i) for i in ver.split("."))


@dataclass
class ReleaseBundle:
    release: str
    bundle: str

    def __gt__(self, other):
        return _ver_to_tuple(self.release) > _ver_to_tuple(other.release)

    @property
    def no_cs_bundle(self):
        return self.bundle.split(":", 1)[-1]


@dataclass
class Charm:
    name: str
    summary: str = ""
    store: str = "charmhub.io"
    docs: str = "charmhub.io"
    upstream: str = "github.com/charmed-kubernetes/"
    bugs: str = "https://bugs.launchpad.net/charmed-kubernetes"
    tags: List[str] = field(default_factory=list)

    def __lt__(self, other: "Charm"):
        """Sort by charm name."""
        return self.name < other.name


def get_charms():
    jenkins = gh().get_repo("charmed-kubernetes/jenkins")
    charm_matrix_file = jenkins.get_contents(
        "jobs/includes/charm-support-matrix.inc", ref="main"
    )
    charm_matrix = yaml.safe_load(charm_matrix_file.decoded_content)
    charm_fields = set(f.name for f in fields(Charm)) - {"name"}
    return sorted(
        [
            Charm(name, **{k: c[k] for k in charm_fields})
            for matrix in charm_matrix
            for name, c in matrix.items()
            if all(field in c for field in charm_fields)
        ]
    )


def get_containers(ersion: str):
    ROCKS_PATH = r"rocks.canonical.com/cdk/"
    major, minor = map(int, ersion.split("."))
    bundles = gh().get_repo("charmed-kubernetes/bundle")
    image_files = bundles.get_dir_contents("container-images")
    txt_files = filter(lambda p: p.path.endswith(".txt"), image_files)
    w_version = [
        (x, semver.VersionInfo.parse(Path(x.path).stem[1:])) for x in txt_files
    ]
    choices = [
        path
        for path, ver in sorted(w_version, key=lambda f: f[1])
        if (ver.major, ver.minor) == (major, minor)
    ]
    if not choices:
        return []
    content = choices[-1].decoded_content
    return [
        line.decode("utf-8")[len(ROCKS_PATH) :].strip() for line in content.splitlines()
    ]


def _with_parent(path_file: Path) -> Path:
    path_file.parent.mkdir(parents=True, exist_ok=True)
    return path_file


@dataclass
class PageWriter:
    version: str
    base: Path
    env: Environment = Environment(
        loader=PackageLoader("k8s_docs_tools"), autoescape=select_autoescape()
    )

    @property
    def k8s_path(self):
        return self.base / "pages" / "k8s"

    @property
    def release_path(self):
        return self.k8s_path / self.version

    @property
    def supported(self):
        major, minor = _ver_to_tuple(self.version)
        return [f"{major}.{min}" for min in range(minor, minor - 3, -1)]

    @cached_property
    def _bundle_table(self):
        bundles = gh().get_repo("charmed-kubernetes/bundle")
        release_bundles = bundles.get_dir_contents("releases")
        symlinks = sorted(
            ReleaseBundle(
                urlopen(t.download_url).read().decode().strip("/"),
                t.name,
            )
            for t in release_bundles
            if getattr(t, "type") == "symlink"
        )[::-1]
        table_tmp = self.env.get_template("bundle_table.j2")
        return table_tmp.render(all_bundles=symlinks)

    def generate_component_page(self):
        output_path = _with_parent(self.release_path / "components.md")
        output = output_path.open("w")
        component_tmp = self.env.get_template("component.j2")
        context = dict(
            release=self.version,
            charms=get_charms(),
            containers=get_containers(self.version),
        )
        output.write(component_tmp.render(**context))

    def generate_release_notes_page(self, as_str=False) -> str:
        header = footer = not as_str
        if not as_str:
            output_path = _with_parent(self.release_path / "release-notes.md")
            output = output_path.open("w")
        component_tmp = self.env.get_template("release-notes.j2")
        context = dict(
            date=datetime.now().strftime("%B %d, %Y"),
            release=self.version,
            header=header,
            footer=footer,
        )
        rendered = component_tmp.render(**context)
        if not as_str:
            output.write(rendered)
        return rendered

    def generate_upgrading_page(self):
        output_path = _with_parent(self.release_path / "upgrading.md")
        output = output_path.open("w")
        template = self.env.get_template("upgrading.j2")
        context = dict(release=self.version)
        text = template.render(**context)
        output.write(text)
        return text

    def update_index(self):
        output_path = _with_parent(self.base / "index.md")
        line_re = re.compile(r"^- \[Version \d+.\d+")
        lines = [
            line_re.sub(f"- [Version {self.version}", line)
            for line in output_path.read_text().splitlines()
        ]
        text = "\n".join(lines) + "\n"
        output_path.write_text(text)
        return text

    def update_install_manual(self):
        output_path = _with_parent(self.k8s_path / "install-manual.md")
        lines, bundle_token, bundle_started = [], "AUTOGENERATED BUNDLE TABLE", False
        for line in output_path.read_text().splitlines():
            if not bundle_started:
                lines.append(line)
            if bundle_token in line and not bundle_started:
                lines += self._bundle_table.splitlines()
                bundle_started = True
            elif bundle_token in line and bundle_started:
                lines.append(line)
                bundle_started = False
        output_path.write_text("\n".join(lines) + "\n")

    def append_release_notes(self):
        output_path = _with_parent(self.k8s_path / "release-notes.md")
        new_notes = self.generate_release_notes_page(as_str=True).splitlines()
        lines, release_token = [], "AUTOGENERATE RELEASE NOTES HERE"
        for line in output_path.read_text().splitlines():
            last_lines = lines[-1:]
            if any(release_token in _last for _last in last_lines):
                if self.version in line:
                    # found version in release-notes already, skipping
                    pass
                else:
                    # previous release found in release-notes, appending
                    lines += new_notes
            lines.append(line)
        output_path.write_text("\n".join(lines) + "\n")

    def generate_supported_versions(self):
        output_path = _with_parent(self.k8s_path / "supported-versions.md")
        output = output_path.open("wb")
        template = self.env.get_template("supported-versions.j2")
        bundle_table = self._bundle_table
        cmd = ["snap", "info", "kube-apiserver", "--unicode=always", "--color=always"]
        snap_info = check_output(cmd, env={"COLUMNS": "120"}).decode()

        context = dict(
            release=self.version,
            supported_releases_x=", ".join([f"{r}.x" for r in self.supported]),
            bundle_table=bundle_table,
            snap_info_kubeapiserver=snap_info,
            release_n1=self.supported[1],
            release_n2=self.supported[2],
        )
        text = template.render(**context).encode("utf-8")
        output.write(text)
        return text


def generate_release_docs(version: str, dest: Path):
    pw = PageWriter(version, dest)
    for page in [
        pw.generate_component_page,
        pw.generate_release_notes_page,
        pw.generate_upgrading_page,
        pw.update_index,
        pw.update_install_manual,
        pw.append_release_notes,
        pw.generate_supported_versions,
    ]:
        page()
