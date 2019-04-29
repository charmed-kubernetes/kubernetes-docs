---
wrapper_template: "base_docs.html"
markdown_includes:
  nav: "shared/_side-navigation.md"
context:
  title: "Custom Load Balancers"
  description: How to configure your Kubernetes cluster to use a custom load balancer.
keywords: high availability, vip, load balancer, f5
tags: [operating]
sidebar: k8smain-sidebar
permalink: custom-lb.html
layout: [base, ubuntu-com]
toc: False
---

# Overview

Charmed Kubernetes supports a custom IP address for the control plane via a setting
on the kubeapi-load-balancer charm or the kubernetes-master charm. Which you would
use depends on your situation and if you need a load balancer. If you have a
virtual IP you can float in front of machines and need load balancing, use
settings on the kubeapi-load-balancer charm. If a full load balancing solution is
in place such as an F5 appliance, remove the kubeapi-load-balancer and use the
settings on the kubernetes-master charms to tell the cluster about the load
balancer.

# Virtual IP in front of kubeapi-load-balancer

If you have a custom setup with a virtual IP in front of the kubeapi-load-balancer
units that isn't charm based, you should use loadbalancer-ips to specify them:

```bash
juju config kubeapi-load-balancer loadbalancer-ips="10.0.0.1 10.0.0.2"
```

# Custom load balancer in front of kubernetes-master charm

If you have a full load balancer such as an F5 appliance or Openstack's Neutron,
use the config options on the kubernetes-master charm and forgo the
kubeapi-load-balancer charm entirely.

Remove the kubeapi-load-balancer application if it exists:

```bash
juju remove-application kubeapi-load-balancer
```

And then add the virtual IPs provided by the load balancing solution to the
kubernetes-master charm.

```bash
juju config kubernetes-master loadbalancer-ips="192.168.1.1 192.168.2.1"
```
