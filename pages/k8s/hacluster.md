---
wrapper_template: "base_docs.html"
markdown_includes:
  nav: "shared/_side-navigation.md"
context:
  title: "HAcluster"
  description: How to configure your Kubernetes cluster to use HAcluster.
keywords: high availability, hacluster, vip, load balancer
tags: [operating]
sidebar: k8smain-sidebar
permalink: hacluster.html
layout: [base, ubuntu-com]
toc: False
---

**HAcluster** is a **Juju** subordinate charm that encapsulates **corosync**
and *pacemaker** for floating virtual IP or DNS addresses and is similar to
[keepalived][keepalived]. It differentiates itself in that it allows servers
to span subnets via the DNS option, which communicates directly with
[MAAS][maas]. It also has the ability to shoot the other node in the
head(STONITH) via **MAAS** to prevent issues in a split-brain scenario.

**Charmed Kubernetes** supports **HAcluster** via a relation and the configuration options
`ha-cluster-vips` and `ha-cluster-dns`. Relations to the kubernetes-master and
kubeapi-load-balancer charms are supported. These options are mutually exclusive.

## Deploying

In order to use HAcluster, the first decision is if a load balancer is desired.
This depends on the size of the cluster and the expected control plane load.
Note that HAcluster requires a minimum of 3 units for a quorum, so you will
need 3 kubeapi-load-balancer or 3 kubernetes-master units to use HAcluster.

### With Load Balancer

```bash
juju deploy charmed-kubernetes
juju add-unit -n 2 kubeapi-load-balancer
juju deploy hacluster
juju config kubeapi-load-balancer ha-cluster-vips=”192.168.0.1 192.168.0.2”
juju relate kubeapi-load-balancer hacluster
```

### Without Load Balancer

```bash
juju deploy kubernetes-core
juju add-unit -n 2 kubernetes-master
juju deploy hacluster
juju config kubernetes-master ha-cluster-vips=”192.168.0.1 192.168.0.2”
juju relate kubernetes-master hacluster
```

## Validation

Once things settle, the virtual IP addresses should be pingable. A new
kubeconfig file will be created containing the virtual IP addresses. You will
need to replace your kubeconfig with the new one:

```bash
juju scp kubernetes-master/0:config ~/.kube/config
```

<!-- LINKS -->

[keepalived]: /kubernetes/docs/keepalived
[maas]: https://maas.io
