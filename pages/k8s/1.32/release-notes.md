
---
wrapper_template: templates/docs/markdown.html
markdown_includes:
  nav: kubernetes/docs/shared/_side-navigation.md
context:
  title: 1.32 Release notes
  description: Release notes for Charmed Kubernetes
keywords: kubernetes, release, notes
tags:
  - news
sidebar: k8smain-sidebar
permalink: 1.32/release-notes.html
layout:
  - base
  - ubuntu-com
toc: False
---
# 1.32

### February 24, 2025 - `charmed-kubernetes --channel 1.32/stable`

The release bundle can also be [downloaded here](https://raw.githubusercontent.com/charmed-kubernetes/bundle/main/releases/1.32/bundle.yaml).

## What's new

<!-- ### aws-cloud-provider

* Support kube-control v2 schema

### aws-k8s-storage

* Support kube-control v2 schema -->

### ceph-csi

* [LP#2068524](https://bugs.launchpad.net/bugs/2068524)Reimagine ceph-csi charm with the reconciler pattern
* Map ceph-csi to juju terraform syntax
* Add `image-registry` configuration option
* Create charm tolerations for ceph-rbd and cephfs deployments and daemonsets
* Support alternate names for ceph-fs charm and associated storage class
<!-- * Upgrade ceph upstream versions including 3.12 and 3.13 -->

<!-- ### cinder-csi

* Support kube-control v2 schema -->

### etcd

* Adding support from focal to noble
* [LP#2053031](https://bugs.launchpad.net/charm-etcd/+bug/2053031) Adding tuning parameters

### kubernetes-worker

* [LP#2083925](https://bugs.launchpad.net/charm-kubernetes-worker/+bug/2083925)
Add rules to access leases for nginx ingress

### openstack-cloud-controller

<!-- * Support kube-control v2 schema -->
* Authorize the CCM to have CRD permissions
* Map openstack-cloud-controller to juju terraform syntax

### openstack-integrator

* Map openstack-integrator to juju terraform syntax
* lb-consumers now ignores default config lb-port if port mapping was provided

## Component Versions

### Charm/Addons pinned versions

- kube-ovn ?????
- calico ?????
- cephcsi ?????
- cinder-csi-plugin ?????
- coredns ?????
- ingress-nginx ?????
- k8s-keystone-auth ?????
- kube-state-metrics ?????
- kubernetes-dashboard ?????
- openstack-cloud-controller-manager ?????

### Charm default versions

- cloud-provider-vsphere ?????
- vsphere-csi-driver ?????
- cloud-provider-azure ?????
- azuredisk-csi-driver ?????
- cloud-provider-aws ?????
- aws-ebs-csi-driver ?????
- gcp-compute-persistent-disk-csi-driver ?????

## Fixes

- **ceph-csi** - [LP#2098004](https://bugs.launchpad.net/charm-ceph-csi/+bug/2098004)purge any cephfs storage classes installed by ops.manifest
- **etcd** - [LP#2096820](https://bugs.launchpad.net/charm-etcd/+bug/2096820) Don't push stderr through stdout when running etcdctl
- **kube-ovn** - [LP#2071494](https://bugs.launchpad.net/charm-kube-ovn/+bug/2071494) Run configure hook only on leader
- **kubernetes-control-plane** - [LP#2044219](https://bugs.launchpad.net/charm-kubernetes-master/+bug/2044219)
Untested port of cis-benchmark action to the kubernetes-control-plane  -->
- **kubernetes-control-plane** - [LP#2087936](https://bugs.launchpad.net/charm-kubernetes-master/+bug/2087936) Address failing grafana-agent relation at CK boot
- **kubernetes-worker** - [LP#2077189](https://bugs.launchpad.net/charm-kubernetes-worker/+bug/2077189) Don't use a status context on actions
- **openstack-cloud-controller** - [LP#2077468](https://bugs.launchpad.net/charm-openstack-cloud-controller/+bug/2077468)
Update out of date links
- **openstack-integrator** - [LP#2095043](https://launchpad.net/bugs/2095043) Address mishandled config of manage-security-group
- **openstack-integrator** - [LP#2098017](https://bugs.launchpad.net/charm-openstack-integrator/+bug/2098017) Pin pbr version so it continues to use setuptools

A full list of bug fixes and other minor feature updates in this release can be found
at
[the launchpad milestone page for 1.32](https://launchpad.net/charmed-kubernetes/+milestone/1.32).

## Notes and Known Issues

## Deprecations and API changes

- Upstream

For details of other deprecation notices and API changes for Kubernetes 1.32,
please see the relevant sections of the
[upstream release notes][upstream-changelog-1.32].

[upstream-changelog-1.32]: https://github.com/kubernetes/kubernetes/blob/master/CHANGELOG/CHANGELOG-1.32.md#deprecation

<!--LINKS-->

[rel]: /kubernetes/docs/release-notes
