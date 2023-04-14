#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
from setuptools import setup, find_packages

setup(
    author="Adam Dyess",
    author_email="adam.dyess@canonical.com",
    description="Generator for Managing Kubernetes docs",
    long_description=Path("README.md").read_text(),
    long_description_content_type='text/markdown',
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    license="MIT license",
    include_package_data=True,
    keywords=["documentation", "markdown", "kubernetes"],
    name="k8s-docs-tools",
    packages=find_packages(include=["k8s_docs_tools"]),
    package_data={
        "k8s_docs_tools": ["templates/*.j2"]
    },
    url="https://github.com/charmed-kubernetes/kubernetes-docs",
    version="0.0.1",
    zip_safe=True,
    install_requires=[
        "click", "jinja2", "pygithub", "pyyaml", "semver"
    ],
    entry_points=dict(
        console_scripts=[
            'k8s_docs_tools = k8s_docs_tools.cli:cli'
        ]
    )
)
