#!/usr/bin/env python
# -*- coding: utf-8 -*-

import click
import logging
from pathlib import Path

from k8s_docs_tools.generate_release import generate_release_docs

FORMAT = "%(name)s %(levelname)s: %(message)s"
logging.basicConfig(format=FORMAT)


@click.group()
def cli():
    pass


@cli.command()
@click.option(
    "--release",
    required=True,
    type=str,
    help="Version identifing the stable charmed-kubernetes release.",
)
@click.argument("output", type=Path)
def generate_release(release, output):
    destination = Path(output)
    destination.mkdir(exist_ok=True)
    generate_release_docs(release, destination)


if __name__ == "__main__":
    cli()
