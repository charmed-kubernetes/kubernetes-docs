---
wrapper_template: "templates/docs/markdown.html"
markdown_includes:
  nav: "kubernetes/charmed-k8s/docs/shared/_side-navigation.md"
context:
  title: "Release notes"
  description: Release notes for Charmed Kubernetes
keywords: kubernetes,  release, notes
tags: [news]
sidebar: k8smain-sidebar
permalink: 1.23/release-notes.html
layout: [base, ubuntu-com]
toc: False
---

# 1.23

### December 15, 2021 - [charmed-kubernetes-862](https://raw.githubusercontent.com/charmed-kubernetes/bundle/main/releases/1.23/bundle.yaml)

## What's new

- CNI support added to kubernetes-master

The core CNI plugins have been added to kubernetes-master, and the CNI
subordinate charms have been updated to render CNI configuration when attached
to kubernetes-master. These changes pave the way for Kubelet to be added to
kubernetes-master in a future release.

- Grafana dashboard for etcd

The etcd charm can now be related to the Prometheus and Grafana charms. When
doing so, a new Grafana dashboard will be created that makes it easier to monitor
the performance characteristics of etcd.

## Component upgrades

- kube-dns 1.21.1 (note: coredns 1.8.3 is the default DNS provider)
- metrics-server 0.5.1

## Fixes

A list of bug fixes and other feature updates in this release can be found at
[the launchpad milestone page](https://launchpad.net/charmed-kubernetes/+milestone/1.23).

## Notes and Known Issues

- [LP 1907153](https://bugs.launchpad.net/snapd/+bug/1907153) Snap install failure in LXD

Snaps may fail to install when the `kubernetes-master` charm is deployed to a LXD container.
This happens when the version of `snapd` on the host does not match the version inside the
container. As a workaround, ensure the same version of `snapd` is installed on the host and
in LXD containers.

- [LP 1936816](https://bugs.launchpad.net/bugs/1936816) and [LP 1913228](https://bugs.launchpad.net/bugs/1913228) Filesystem Hierachy Standards

  Applications running inside a kubernetes-master should set pid files and log files in
appropriate operational locations like `/run/` and `/var/log/kubernetes/`. Care was taken to restart
services using these new locations and migrate some existing files out of `/root/cdk/`.

  For the service `cdk.master.auth-webhook` the new pid file and log files are named
`/run/cdk.master.auth-webhook.pid` and `/var/log/kubernetes/cdk.master.auth-webhook.log`
to match the systemctl service name.

  If the [`filebeat`](https://charmhub.io/filebeat) charm is related to kubernetes-master,
ensure that its logpath include this new path ( e.g. `juju config filebeat logpath='/var/log/kubernetes/*.log'` )

## Deprecations and API changes

- Upstream

  For details of other deprecation notices and API changes for Kubernetes 1.23, please see the
relevant sections of the [upstream release notes][upstream-changelog].

## Previous releases

Please see [this page][rel] for release notes of earlier versions.

<!--LINKS-->
[rel]: /kubernetes/charmed-k8s/docs/release-notes
[upstream-changelog]: https://github.com/kubernetes/kubernetes/blob/master/CHANGELOG/CHANGELOG-1.23.md#deprecation
