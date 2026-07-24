---
wrapper_template: "templates/docs/markdown.html"
markdown_includes:
  nav: "kubernetes/charmed-k8s/docs/shared/_side-navigation.md"
context:
  title: "Installing Charmed Kubernetes"
  description: installing to different substrates
keywords: install, , metallb, loadbalancer
tags: [operating]
sidebar: k8smain-sidebar
permalink: how-to-install.html
layout: [base, ubuntu-com]
toc: False
---

In addition to the easy to follow [tutorial](/kubernetes/charmed-k8s/docs/quickstart) for
Charmed Kubernetes, additional guides are available to take you through the
installation steps for a number of different substrates. The 'Cloud' install
page covers many different scenarios with Juju-supported clouds.

<div class="p-notification--caution is-inline">
  <div markdown="1" class="p-notification__content">
    <span class="p-notification__title">Warning:</span>
    <p class="p-notification__message">Canonical is decommissioning the <code>rocks.canonical.com</code> container image registry as part of our infrastructure modernization. The registry will be unavailable after <strong>August 10, 2026</strong>. This affects Charmed Kubernetes releases 1.35 and earlier. New deployments of later releases use <code>ghcr.io/canonical/cdk</code> by default; existing deployments, or deployments with an overridden <code>image-registry</code> value, must be migrated. Configure the <code>image-registry</code> value for each Charmed Kubernetes component charm, including CNI and CSI charms, to use <code>ghcr.io/canonical/cdk</code>. We apologize for any inconvenience this migration may cause.</p>

```bash
juju config <charm-name> image-registry=ghcr.io/canonical/cdk
```

For example:

```bash
juju config kubernetes-control-plane image-registry=ghcr.io/canonical/cdk
```

  </div>
</div>

- [Install on a cloud](/kubernetes/charmed-k8s/docs/install-manual)
- [Install on existing machines](/kubernetes/charmed-k8s/docs/install-existing)
- [Install locally with LXD](/kubernetes/charmed-k8s/docs/install-local)
- [Install on Equinix](/kubernetes/charmed-k8s/docs/equinix)

There are also two 'special case' scenarios we provide guidance for:

- [Installing offline, or in a restricted environment](/kubernetes/charmed-k8s/docs/install-offline)
- [Installing for NVIDIA DGX](/kubernetes/charmed-k8s/docs/nvidia-dgx)

If you wish to uninstall:

- [Uninstalling Charmed Kubernetes](/kubernetes/charmed-k8s/docs/uninstall)

<!-- FEEDBACK -->
<div class="p-notification--information">
  <div class="p-notification__content">
    <p class="p-notification__message">We appreciate your feedback on the documentation. You can
    <a href="https://github.com/charmed-kubernetes/kubernetes-docs/edit/main/pages/k8s/how-to-install.md" >edit this page</a>
    or
    <a href="https://github.com/charmed-kubernetes/kubernetes-docs/issues/new">file a bug here</a>.</p>
    <p>See the guide to <a href="/kubernetes/charmed-k8s/docs/how-to-contribute"> contributing </a> or discuss these docs in our <a href="https://kubernetes.slack.com/archives/CG1V2CAMB"> public Slack channel</a>.</p>
  </div>
</div>
