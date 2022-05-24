from dataclasses import dataclass, fields, field
import logging
import os
from pathlib import Path
from typing import List

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
        "jobs/includes/charm-support-matrix.inc", ref="docs/components"
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
    content = choices[-1].decoded_content
    return [
        line.decode("utf-8")[len(ROCKS_PATH) :].strip() for line in content.splitlines()
    ]


def generate_component_page(version: str, output):
    env = Environment(
        loader=PackageLoader("k8s_docs_tools"), autoescape=select_autoescape()
    )

    component_tmp = env.get_template("component.j2")
    context = dict(
        release=version,
        charms=get_charms(),
        containers=get_containers(version),
    )
    output.write(component_tmp.render(**context))
