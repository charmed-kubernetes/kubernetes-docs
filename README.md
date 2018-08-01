## Canonical Distribution of Kubernetes docs

This is a temporary repository for iterating on new versions of the Canonical Kubernetes docs. This repository is set up as a simple github-pages/jekyll website, which serves pages at:

[https://juju-solutions.github.com/kubernetes-docs/]

## Layout

The content is contained in two main places:

1.  The **pages** folder, which contains markdown files mapping to individual pages of the docs.

1.  The **news** folder, which contains blog-like entires in markdown files.

## Testing docs

If you have cloned this repo and wish to build it locally to test changes, the easiest way is to have docker (and docker-compose) installed and run:

      docker-compose build --no-cache && docker-compose up
