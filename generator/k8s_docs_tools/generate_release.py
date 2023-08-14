from dataclasses import dataclass, fields, field
from datetime import datetime
import logging
import os
import re
from pathlib import Path
from typing import List, Mapping

import semver
from github import Github, UnknownObjectException
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


def _prior_version(ver):
    as_tuple = _ver_to_tuple(ver)
    return ".".join(map(str, (as_tuple[0], as_tuple[1] - 1)))


def within_channel_range(ersion: str, ranges: Mapping[str, str]):
    if ranges is None:
        return True
    rel = _ver_to_tuple(ersion)
    _min = ranges.get("min")
    _max = ranges.get("max")
    if _min and _max:
        return _ver_to_tuple(_min) <= rel <= _ver_to_tuple(_max)
    elif _min:
        return _ver_to_tuple(_min) <= rel
    elif _max:
        return rel <= _ver_to_tuple(_max)
    return True


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
    downstream: str = ""
    upstream: str = "github.com/charmed-kubernetes/"
    bugs: str = "https://bugs.launchpad.net/charmed-kubernetes"
    tags: List[str] = field(default_factory=list)

    def __lt__(self, other: "Charm"):
        """Sort by charm name."""
        return self.name < other.name


@dataclass
class Changelog:
    name: str
    commit_log: str = ""


def get_charms(ersion: str) -> List[Charm]:
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
            and within_channel_range(ersion, c.get("channel-range"))
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

    def generate_whats_new(self):
        # cache results
        _whats_new = getattr(self, "_whats_new", None)
        if _whats_new:
            return _whats_new

        context: Mapping[str, Changelog] = {}
        _from = _prior_version(self.version)
        _to = self.version
        for each in get_charms(self.version):
            report = context.setdefault(each.name, Changelog(each.name))
            try:
                comparison = (
                    gh()
                    .get_repo(each.downstream.strip(".git"))
                    .compare(f"release_{_from}", f"release_{_to}")
                )
            except UnknownObjectException:
                continue
            for commit in comparison.commits:
                report.commit_log += (
                    commit.commit.message.strip()
                    .replace("\r\n", "\n")
                    .replace("\n\n", "\n")
                )
                report.commit_log += "\n"

        self._whats_new = context
        return context

    def generate_component_page(self):
        output_path = _with_parent(self.release_path / "components.md")
        output = output_path.open("w")
        component_tmp = self.env.get_template("component.j2")
        context = dict(
            release=self.version,
            charms=get_charms(self.version),
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
            whats_new=self.generate_whats_new(),
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

    def append_release_notes(self):
        output_path = _with_parent(self.k8s_path / "release-notes.md")
        new_notes = self.generate_release_notes_page(as_str=True).splitlines()
        lines, release_token = [], "AUTOGENERATE RELEASE NOTES HERE"
        for line in output_path.read_text().splitlines():
            if lines and release_token in lines[-1]:
                if self.version in line:
                    # found version in release-notes already, skipping
                    pass
                else:
                    # previous release found in release-notes, appending
                    lines += new_notes
            lines.append(line)
        text = "\n".join(lines) + "\n"
        output_path.write_text(text)
        return text

    def generate_supported_versions(self):
        output_path = _with_parent(self.k8s_path / "supported-versions.md")
        output = output_path.open("wb")
        template = self.env.get_template("supported-versions.j2")

        context = dict(
            release=self.version,
            supported_releases_x=", ".join([f"{r}.x" for r in self.supported]),
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
        pw.append_release_notes,
        pw.generate_supported_versions,
    ]:
        page()
