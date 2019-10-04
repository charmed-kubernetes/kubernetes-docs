---
wrapper_template: "kubernetes/docs/base_docs.html"
markdown_includes:
  nav: "kubernetes/docs/shared/_side-navigation.md"
context:
  title: "Charm reference"
  description: Detailed configuration and usage for the Charmed Kubernetes charms
keywords: charm, reference, kubernetes
tags: [reference]
sidebar: k8smain-sidebar
permalink: charm-reference.html
layout: [base, ubuntu-com]
toc: False
---


General into xxxxxxxxx

Generic notes about charms. Possible links to upgrades?

## Core charms

[kubernetes-master][]
[kubernetes-worker][]
[kubeapi-load-balancer][]
[etcd][]
...

## CNI Charms

See the [CNI Overview][cni] for more detail on the individual CNI-related
charms (Flannel, Calico, etc.)

## Integrator Charms

These charms are specific to particular clouds

[aws-integrator][]
[gcp-integrator][]
[openstack-integrator][]




<!-- LINKS -->
[aws-integrator]: /kubernetes/docs/aws-integration
[gcp-integrator]: /kubernetes/docs/gcp-integration
[openstack-integrator]: /kubernetes/docs/openstack-integration
[kubernetes-master]: /kubernetes/docs/charm-kubernetes-master
[kubernetes-worker]: /kubernetes/docs/charm-kubernetes-worker
[kubeapi-load-balancer]: /kubernetes/docs/charm-kubeapi-load-balancer
[etcd]: /kubernetes/docs/charm-etcd
