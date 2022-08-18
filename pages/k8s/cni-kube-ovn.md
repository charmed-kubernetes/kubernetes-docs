---
wrapper_template: "templates/docs/markdown.html"
markdown_includes:
  nav: "kubernetes/docs/shared/_side-navigation.md"
context:
  title: "CNI with Kube-OVN"
  description: How to manage and deploy Kubernetes with Kube-OVN
keywords: CNI, networking
tags: [operating]
sidebar: k8smain-sidebar
permalink: cni-kube-ovn.html
layout: [base, ubuntu-com]
toc: False
---

[Kube-OVN][kube-ovn] is a CNI implementation based on OVN that provides a rich
set of networking features for advanced enterprise applications.

TODO: what sets it apart from other CNIs?

## Cloud configuration

TODO

## Deploying Charmed Kubernetes with Kube-OVN

To deploy a cluster with Kube-OVN, deploy the `charmed-kubernetes` bundle with
the [Kube-OVN overlay][kube-ovn-overlay]:

```bash
juju deploy charmed-kubernetes --overlay kube-ovn-overlay.yaml
```

You can apply any additional customisation overlays that would apply to
`charmed-kubernetes` to this deployment as well.

## Kube-OVN configuration options

A full list of Kube-OVN configuration options and their descriptions can be found
in the [Kube-OVN charm][kube-ovn-charm] page.

### Checking the current configuration

To check the current configuration settings for Kube-OVN, run the command:

```bash
juju config kube-ovn
```

### Setting a config option

To set an option, simply run the config command with and additional
`<key>=<value>` argument. For example, to set the default pod CIDR and gateway:

```bash
juju config kube-ovn default-cidr=10.123.0.0/16 default-gateway=10.123.0.1
```

TODO: better example here because these cannot be changed post-deploy

Config settings which require additional explanation are described below.

## Configuring the default subnet

When kube-ovn is first deployed, it creates a default subnet that it uses to
assign IPs to pods. By default, this subnet is `192.168.0.0/24`.

To configure the default pod subnet at deploy time, create a file named
`kube-ovn-config.yaml` that contains the following:

```yaml
applications:
  kube-ovn:
    options:
      default-cidr: 10.123.0.0/16
      default-gateway: 10.123.0.1
```

Then include the overlay when you deploy Charmed Kubernetes:

```bash
juju deploy charmed-kubernetes --overlay kube-ovn-overlay.yaml --overlay kube-ovn-config.yaml
```

## Changing the default subnet after deployment

TODO

## Creating namespaced subnets

TODO

## TODO: advanced configuration


## Using a private Docker registry

For a general introduction to using a private Docker registry with
**Charmed Kubernetes**, please refer to the [Private Docker Registry][] page.

In addition to the steps documented there, you will need to upload the
following image to the registry:

```no-highlight
docker.io/kubeovn/kube-ovn:v1.10.4
```

The Kube-OVN charm will automatically use the image registry that
kubernetes-control-plane is configured to use. If needed, you can override
the Kube-OVN image registry by setting the image-registry config:

```bash
export IP=`juju run --unit docker-registry/0 'network-get website --ingress-address'`
export PORT=`juju config docker-registry registry-port`
export REGISTRY=$IP:$PORT
juju config kube-ovn image-registry=$REGISTRY
```

## Troubleshooting

If there is an issue with connectivity, it can be useful to inspect the Juju logs.
To see a complete set of logs for Kube-OVN:

```bash
juju debug-log --replay --include=kube-ovn
```

For additional troubleshooting pointers, please see the [dedicated troubleshooting page][troubleshooting].

## Useful links

- [Kube-OVN on GitHub][kube-ovn]
- [Kube-OVN charm on Charmhub][kube-ovn-charm]
- [Kube-OVN Architecture Guide][kube-ovn-architecture]

<!-- LINKS -->

[kube-ovn]: https://github.com/kubeovn/kube-ovn
[kube-ovn-architecture]: https://kubeovn.github.io/docs/en/reference/architecture/
[kube-ovn-charm]: https://charmhub.io/kube-ovn
[kube-ovn-overlay]: https://raw.githubusercontent.com/charmed-kubernetes/bundle/main/overlays/kube-ovn-overlay.yaml
[private docker registry]: /kubernetes/docs/docker-registry
[troubleshooting]: /kubernetes/docs/troubleshooting

<!-- FEEDBACK -->
<div class="p-notification--information">
  <div class="p-notification__content">
    <p class="p-notification__message">We appreciate your feedback on the documentation. You can
    <a href="https://github.com/charmed-kubernetes/kubernetes-docs/edit/main/pages/k8s/cni-kube-ovn.md" >edit this page</a>
    or
    <a href="https://github.com/charmed-kubernetes/kubernetes-docs/issues/new" >file a bug here</a>.</p>
  </div>
</div>
