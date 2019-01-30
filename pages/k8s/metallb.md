---
wrapper_template: "base_docs.html"
markdown_includes:
  nav: "shared/_side-navigation.md"
context:
  title: "MetalLB"
  description: How to configure your Kubernetes cluster to use MetalLB.
keywords: high availability, metallb, vip, load balancer
tags: [operating]
sidebar: k8smain-sidebar
permalink: metallb.html
layout: [base, ubuntu-com]
toc: False
---
# About

[MetalLB][metallb] is a Kubernetes-aware solution that will monitor for services with the type LoadBalancer and assign an IP address from a virtual pool that is available. It uses BGP or ARP to expose services. MetalLB has support for local traffic, meaning that the machine that receives the data will be the machine that services the request. This now works with ARP or BGP. It is not suggested to use a virtual IP with high traffic workloads because only one machine will receive the traffic for a service. The other machines are just there for failover. BGP does not have this limitation but does see nodes as the atomic unit. This means if the service is running on 2 of 5 nodes then only those two nodes will receive traffic, but they will each receive 50% of the traffic even in one of the nodes has 3 pods and one has 1 pod running on it. It is recommended to use node anti-affinity to prevent pods from stacking on a single node. It is currently not available as a Juju CaaS charm, so the best way to install it is with a helm chart.

<!-- LINKS -->

[metallb]: https://metallb.universe.tf
