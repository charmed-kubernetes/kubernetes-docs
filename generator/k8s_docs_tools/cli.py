#!/usr/bin/env python
# -*- coding: utf-8 -*-

import click
import logging

from k8s_docs_tools.generate_release import generate_component_page

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
@click.argument("output", type=click.File("w"))
def component(release, output):
    generate_component_page(release, output)


if __name__ == "__main__":
    cli()
