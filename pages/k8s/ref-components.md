---
wrapper_template: "kubernetes/docs/base_docs.html"
markdown_includes:
  nav: "kubernetes/docs/shared/_side-navigation.md"
context:
  title: "Components of the Charmed Kubernetes bundle"
  description: A more detailed spec of the standard CK install.
keywords: install, reference, charms
tags: [reference]
sidebar: k8smain-sidebar
permalink: ref-components.html
layout: [base, ubuntu-com]
toc: False
---

Charmed Kubernetes is installed based on the contents of a Juju 'bundle', which
specifies exact revisions of Juju charms to be used.

The current release of Charmed Kubernetes is: **1.17**

The current release version of the Charmed Kubernetes bundle is: [**#335**](https://api.jujucharms.com/charmstore/v5/bundle/charmed-kubernetes-335)

## Core components

-   [containerd #53](https://jaas.ai/u/containers/containerd/53)
-   [easyrsa #295](https://jaas.ai/u/containers/containerd/53)
-   [etcd #485](https://jaas.ai/u/containers/containerd/53)
-   [flannel #466](https://jaas.ai/u/containers/containerd/53)
-   [kubeapi-load-balancer #701](https://jaas.ai/u/containers/containerd/53)
-   [kubernetes-master #788](https://jaas.ai/u/containers/kubernetes-master/788)
-   [kubernetes-worker #623](https://jaas.ai/u/containers/kubernetes-worker/623)

## Additional components

Many installs may make use of overlays to replace specific components at
install time (e.g. CNI), or simply add additional functionality (e.g.
monitoring). These components are not typically pinned to a specific revision.

### cloud integration

-   aws-integrator
-   azure-integrator
-   gcp-inegrator
-   openstack-integrator
-   vsphere-integrator

### CNI

-   Calico
-   Canal
-   Tigera Secure EE

### Monitoring/Logging

-   grafana
-   kube-state-metrics
-   nagios
-   prometheus
-   telegraf

### High Availability

-   keepalived
-   HAcluster
-   MetalLB

### Misc

-   Vault


## Deprecations/Notes

-   The `registry` action for the `kubernetes-worker` charm has been deprecated
    and will be removed in a future release. To enable a custom container
    registry, please see the [registry][] documentation.

Please see the detailed [release notes][] for information on other changes and
bug fixes.

## Upgrading

To upgrade from the previous release, please see the [upgrade][] documentation.

If you are upgrading from an older version, please check the [upgrade notes][].


<!-- FEEDBACK -->
<div class="p-notification--information">
  <p class="p-notification__response">
    We appreciate your feedback on the documentation. You can
    <a href="https://github.com/charmed-kubernetes/kubernetes-docs/edit/master/pages/k8s/operations.md" class="p-notification__action">edit this page</a>
    or
    <a href="https://github.com/charmed-kubernetes/kubernetes-docs/issues/new" class="p-notification__action">file a bug here</a>.
  </p>
</div>


<!--LINKS-->
[upgrade]: /kubernetes/docs/upgrade
[upgrade notes]: /kubernetes/docs/upgrade-notes
[release notes]: /kubernetes/docs/release-notes
[registry]: /kubernetes/docs/docker-registry
