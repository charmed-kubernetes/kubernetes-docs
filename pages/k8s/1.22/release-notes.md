---
wrapper_template: "templates/docs/markdown.html"
markdown_includes:
  nav: "kubernetes/docs/shared/_side-navigation.md"
context:
  title: "Release notes"
  description: Release notes for Charmed Kubernetes
keywords: kubernetes,  release, notes
tags: [news]
sidebar: k8smain-sidebar
permalink: 1.22/release-notes.html
layout: [base, ubuntu-com]
toc: False
---

# 1.22

### September 1, 2021 - [charmed-kubernetes-761](https://api.jujucharms.com/charmstore/v5/charmed-kubernetes-761/archive/bundle.yaml)

## What's new

- Calico BGP Service IP Advertisement

The Calico charm now supports advertising Kubernetes service IPs over BGP. More
information can be found in the
[CNI with Calico][calico-service-ip-advertisement] page.

- Improved load balancer provider support

The support for load balancing the Kubernetes control plane is being improved with
two new relation endpoints: `loadbalancer-external` and `loadbalancer-internal`.
This change adds support for Azure native load balancers for the Kubernetes control
plane, and improves LB configurability while still simplifying the relations needed
between the various components of the cluster.

## Component upgrades

## Fixes

A list of bug fixes and other minor feature updates in this release can be found at
[the launchpad milestone page](https://launchpad.net/charmed-kubernetes/+milestone/1.22).

## Notes and Known Issues

## Deprecations and API changes

- [LP 1935992](https://bugs.launchpad.net/charm-kubernetes-worker/+bug/1935992) Code Cleanup

The following deprecated `kubernetes-master` features have been removed in this release:

- addons-registry config
- create-rbd-pv action and related templates
- monitoring-storage config
- kube-dns interface
- migrate_from_pre_snaps code

The following deprecated `kubernetes-worker` features have been removed in this release:

- allow-privileged config
- kube-dns interface
- registry action and related templates
- code path for k8s < 1.10

- Upstream

For details of other deprecation notices and API changes for Kubernetes 1.22, please see the
relevant sections of the [upstream release notes](https://github.com/kubernetes/kubernetes/blob/master/CHANGELOG/CHANGELOG-1.22.md#deprecation)

## Previous releases

Please see [this page][rel] for release notes of earlier versions.

<!--LINKS-->
[upgrade-notes]: /kubernetes/docs/upgrade-notes
[rel]: /kubernetes/docs/release-notes
[images-per-release]: https://github.com/charmed-kubernetes/bundle/tree/master/container-images
[arc-docs]: https://github.com/Azure/azure-arc-validation/blob/main/README.md
[calico-service-ip-advertisement]: /kubernetes/docs/cni-calico#service-ip-advertisement
