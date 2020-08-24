---
wrapper_template: "kubernetes/docs/base_docs.html"
markdown_includes:
  nav: "kubernetes/docs/shared/_side-navigation.md"
context:
  title: "Release notes"
  description: Release notes for CDK
keywords: kubernetes,  release, notes
tags: [news]
sidebar: k8smain-sidebar
permalink: release-notes.html
layout: [base, ubuntu-com]
toc: False
---

# 1.19 pre-release

<div class="p-notification--warning">
  <p markdown="1" class="p-notification__response">
    <span class="p-notification__status">Warning:</span>
This version is currently in pre-release and is presented here solely for
testing purposes. Any information on this and other pages connected to this release
is subject to change.
  </p>
</div>

### August XXth, 2020 - [charmed-kubernetes-475](https://api.jujucharms.com/charmstore/v5/charmed-kubernetes-475/archive/bundle.yaml)

Before upgrading, please read the [upgrade notes](/kubernetes/docs/upgrade-notes).

## What's new

- IPv6 support

This release of Charmed Kubernetes can now enable the alpha IPv6 dual-stack or
beta IPv6-only support in Kubernetes by using IPv6 CIDRs in addition to or
instead of IPv4 CIDRs in the Kubernetes Master charm's `service-cidr` and the
Calico charm's `cidr` charm config.

More information can be found in [Using IPv6 with Charmed Kubernetes][ipv6],
including limitations and known issues.

- CIS benchmark compliance

Charmed Kubernetes is now compliant with the Center for Internet Security (CIS)
benchmark for Kubernetes. Significant changes to the `kubernetes-master` and
`kubernetes-worker` charms have been made to achieve this. Find more information
about these changes, running the benchmark, and analyzing test results in the
[CIS compliance for Charmed Kubernetes][cis-benchmark] documentation.

- Authentication changes

File-based authentication is not compliant with the CIS benchmark. Charmed Kubernetes
now deploys a webhook authentication service that compares API requests to Kubernetes
secrets. If needed, any existing entries in previous authentication files
(`basic_auth.csv` and `known_tokens.csv`) are migrated to secrets during the
`kubernetes-master` charm upgrade.

More information about this new service can be found in the
[Authorisation and Authentication][authn] documentation.

- New Calico configuration options

(description) `veth-mtu` for Calico. `ignore-loose-rpf` for Calico/Canal/Tigera Secure EE.

- Ubuntu 20.04

The default operating system for deployed machines is now Ubuntu 20.04 (Focal). Ubuntu 18.04 (Bionic) and 16.04 (Xenial) are still supported.

- SR-IOV CNI

A new SR-IOV CNI addon has been made available for Charmed Kubernetes. Using
SR-IOV CNI, it is now possible to take network interfaces that are SR-IOV
Virtual Functions and attach them directly to pods. For more information, see
the new [SR-IOV CNI documentation][cni-sriov].

## Component upgrades

- addon-resizer 1.8.9
- ceph-csi 2.1.2
- cloud-provider-openstack (TODO https://bugs.launchpad.net/cdk-addons/+bug/1889433)
- coredns 1.6.7
- kube-state-metrics 1.9.7
- kubernetes-dashboard 2.0.1
- nginx-ingress 0.31.1

## Fixes

A list of bug fixes and other minor feature updates in this release can be found at
[https://launchpad.net/charmed-kubernetes/+milestone/1.19](https://launchpad.net/charmed-kubernetes/+milestone/1.18).

## Notes / Known Issues

- The `insecure-bind-address` and `insecure-port` options to `kube-apiserver` have
been removed in this release. Using `juju run` with `kubectl` to interact with the
cluster now requires an explicit `--kubeconfig <file>` option:

    ```bash
    juju run --unit kubernetes-master/0 'kubectl --kubeconfig /root/.kube/config get nodes'
    NAME              STATUS   ROLES    AGE   VERSION
    ip-172-31-10-19   Ready    <none>   71m   v1.19.0
    ```

## Previous releases

Please see [this page][historic] for release notes of earlier versions.

<!--LINKS-->
[upgrade-notes]: /kubernetes/docs/upgrade-notes
[bundle]: https://api.jujucharms.com/charmstore/v5/canonical-kubernetes-471/archive/bundle.yaml
[cis-benchmark]: /kubernetes/docs/cis-compliance
[bundle]: https://api.jujucharms.com/charmstore/v5/canonical-kubernetes-471/archive/bundle.yaml
[historic]: /kubernetes/docs/release-notes-historic
[ipv6]: /kubernetes/docs/ipv6
[cni-sriov]: /kubernetes/docs/cni-sriov
[authn]: /kubernetes/docs/auth#authn

<!-- FEEDBACK -->
<div class="p-notification--information">
  <p class="p-notification__response">
    We appreciate your feedback on the documentation. You can
    <a href="https://github.com/charmed-kubernetes/kubernetes-docs/edit/master/pages/k8s/release-notes.md" class="p-notification__action">edit this page</a>
    or
    <a href="https://github.com/charmed-kubernetes/kubernetes-docs/issues/new" class="p-notification__action">file a bug here</a>.
  </p>
</div>
