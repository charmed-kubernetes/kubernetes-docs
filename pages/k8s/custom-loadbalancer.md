---
wrapper_template: "kubernetes/docs/base_docs.html"
markdown_includes:
  nav: "kubernetes/docs/shared/_side-navigation.md"
context:
  title: "Custom load balancers"
  description: How to configure your Kubernetes cluster to use a custom load balancer.
keywords: high availability, vip, load balancer, f5
tags: [operating]
sidebar: k8smain-sidebar
permalink: custom-loadbalancer.html
layout: [base, ubuntu-com]
toc: False
---

**Charmed Kubernetes** supports setting a
custom IP address for the control plane.  There are two ways of achieving this, depending
on which type of load balancing solution you wish to configure:

 -  If you have a virtual IP to place in front of machines, configure the settings on the
    `kubeapi-load-balancer` charm.

 -  If a full load balancing solution is in place such as an F5 appliance, remove the
     `kubeapi-load-balancer` and use the settings on the `kubernetes-master` charm to
      configure the load balancer.

Both solutions are described in the sections below.

# Virtual IP in front of kubeapi-load-balancer

If you have a virtual IP in front of the kubeapi-load-balancer
units which isn't charm based, you should use the loadbalancer-ips configuration to
specify them:

```bash
juju config kubeapi-load-balancer loadbalancer-ips="10.0.0.1 10.0.0.2"
```

Multiple IP addresses should be given as a space-separated list.


# Custom load balancer in front of kubernetes-master charm

If you have a full load balancer such as an F5 appliance or OpenStack's Neutron,
use the configuration options on the `kubernetes-master` charm and forgo
`kubeapi-load-balancer`  entirely.

Remove the `kubeapi-load-balancer` application if it exists:

```bash
juju remove-application kubeapi-load-balancer
```

Then configure the IP addresses provided by the load balancing solution with the
`kubernetes-master` charm.

```bash
juju config kubernetes-master loadbalancer-ips="192.168.1.1 192.168.2.1"
```

Multiple IP addresses should be given as a space-separated list.
