---
wrapper_template: "base_docs.html"
markdown_includes:
  nav: "shared/_side-navigation.md"
context:
  title: "High Availability"
  description: How to configure your Kubernetes cluster for high availability.
keywords: high availability, hacluster, vip, load balancer
tags: [operating]
sidebar: k8smain-sidebar
permalink: high-availability.html
layout: [base, ubuntu-com]
toc: False
---


It is a natural desire to have a CDK cluster be highly available and resilient to failures.
This is not an easy task though and requires much more thought than initially expected.
Note that this document is dealing with on-premise or private cloud clusters that have no
hardware load balancer such as an F5. The public cloud providers have solutions for this
and should be used in those situations. For on-premise, we start with the two basic
components of a Kubernetes cluster: your control plane, the kubernetes-master charm, and
the worker units, the kubernetes-worker charm.

![master worker image](master-worker.png)

These two things are the points of ingress on the cluster and where we will focus our
effort for high availability. We need to be able to communicate with the cluster as
robustly as possible.

### Control Plane
The first thought when attempting to make the control plan highly available is to scale
the number of master units with `juju add-unit kubernetes-master`.

![multi-master worker image](multi-master.png)

While this will add more machines, it doesn’t work as initially expected. What happens
is that the workers will randomly pick a master to communicate with and always use that
master unit. This means if that master is disabled in a way that doesn’t remove it
from juju, those workers are simply unable to communicate with the control plane. If
workers arbitrarily pick the same master, they can also overload the master with traffic.

Load balancing the masters is the next logical step:

![single load balancer image](single-loadbalancer.png)

The workers now all use the load balancer to talk to the control plane. This will
balance the load to the master units, but we have just moved the single point of
failure to the load balancer. Floating a virtual IP address in front of the master
units works in a similar manner but without any load balancing. If your cluster
won’t generate enough traffic to saturate a single master, but you want high
availability on the control plane, multiple masters floating a virtual IP address
is a solid choice.

The next thought is to add multiple load balancers to add resiliency there:

![multi-load balancer image](multi-load-balancer.png)

We’re now back to the problem where the workers are talking to a random load balancer
and if that balancer fails they will fail. We can float a virtual IP address in the
front of these load balancers to solve that.

#### Summary
The way to handle a highly available control plane is virtual IP addresses in front
of either the master units or load balancers depending on load balance requirements.
If the desire is simply to avoid a node dying from taking away the cluster, a virtual
IP on the master nodes will handle that. Note that multiple virtual IP addresses can
be used if load exceeds a single machine, but realize that without proper load
balancing the load on the master units will not necessarily be even due to the random
IP selection in the Kubernetes worker charms.

### Worker Ingress
Worker ingress is a very similar problem to the control plane, with the exception of
the random IP selection of the API server isn’t relevant to worker ingress. There
are a few ways to get traffic into Kubernetes. Two common ways are to forward incoming
traffic to the service IP and route that to any worker. It will get routed by
kube-proxy to a pod that will service it. The other option is to forward incoming
traffic to a nodeport on any worker to be proxied.

Multiple virtual IPs would be a good choice in front of the workers. This allows a
bit of load balancing with round-robin DNS and also allows individual workers to fail.
A more robust option would be to add load balancers in front of the workers and
float virtual IPs on those. Note a downside here is the east-west traffic once the
traffic hits a worker node as it may be routed due to load or just to find a worker
with the destination pod. This problem is under active development with projects
that are Kubernetes-aware such as MetalLB, which will be discussed in the next section.

## Solutions
### [Keepalived][keepalived]

### [HAcluster][hacluster]

### [MetalLB][metallb]

<!-- LINKS -->

[keepalived]: /kubernetes/docs/keepalived
[hacluster]: /kubernetes/docs/hacluster
[metallb]: /kubernetes/docs/metallb
