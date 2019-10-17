Using network spaces in Juju, it's possible to deploy CDK in an environment with multiple networks and assign traffic to different networks explicitly.

Note: As of Juju 2.3.5, multiple network spaces are only supported on MAAS.

This guide assumes you're familiar with the basics of MAAS and Juju. If you're not, you can familiarize yourself with them using the [MAAS documentation](https://docs.maas.io/) and [Juju documentation](https://jujucharms.com/docs/).

## Configuring MAAS

Starting with the following assumptions:
1. You have MAAS nodes that are attached to multiple logical networks (separate physical networks or VLANs)
2. You have commissioned the nodes in MAAS

### Create spaces in MAAS

In the Subnets tab of the MAAS GUI, click Add -> Space to create spaces as needed. To add subnets to a space, enter the subnet's VLAN configuration page (click in the VLAN column on the main Subnets page) and assign it to the space.

### Enable network interfaces on nodes

By default, only the first network interface is enabled on each node. You need to manually enable the rest - Juju won't do it for you.

Go to the Nodes tab, click on a node, click the Interfaces tab. Make sure each interface's IP mode is set to `Auto assign`.

## Configuring Juju

If you've already bootstrapped a Juju controller, use `juju reload-spaces` to pick up the changes from MAAS. Otherwise, just bootstrap and the spaces in Juju should be configured automatically.

Run `juju spaces` and make sure you see the spaces and subnet assignments that you're expecting.

## Deploying CDK

You'll need to deploy a custom bundle. You can start by downloading one of our standard bundles, for example: https://api.jujucharms.com/charmstore/v5/canonical-kubernetes/archive/bundle.yaml

Add `spaces` constraints as needed to make sure the units land on machines belonging to the networks you want. Add `bindings` entries to assign network traffic to specific spaces.

Here's an example bundle that does both:

```
series: xenial
description: A nine-machine Kubernetes cluster, appropriate for production. Includes a three-machine etcd cluster and three Kubernetes worker nodes.
services:
  easyrsa:
    annotations:
      gui-x: '450'
      gui-y: '550'
    charm: cs:~containers/easyrsa-39
    constraints: "root-disk=8G spaces=juju,^etcd-peer,^etcd-client,^flannel,^apiserver,^loadbalancer,^workload"
    num_units: 1
    bindings:
      "": juju
  etcd:
    annotations:
      gui-x: '800'
      gui-y: '550'
    charm: cs:~containers/etcd-77
    constraints: "root-disk=8G spaces=juju,etcd-peer,etcd-client,^flannel,^apiserver,^loadbalancer,^workload"
    num_units: 3
    bindings:
      "": juju
      cluster: etcd-peer
      db: etcd-client
  flannel:
    annotations:
      gui-x: '450'
      gui-y: '750'
    charm: cs:~containers/flannel-52
    bindings:
      "": juju
      cni: flannel
  kubeapi-load-balancer:
    annotations:
      gui-x: '450'
      gui-y: '250'
    charm: cs:~containers/kubeapi-load-balancer-57
    constraints: "root-disk=8G spaces=juju,^etcd-peer,^etcd-client,^flannel,apiserver,loadbalancer,^workload"
    expose: true
    num_units: 1
    bindings:
      "": juju
      website: loadbalancer
  kubernetes-master:
    annotations:
      gui-x: '800'
      gui-y: '850'
    charm: cs:~containers/kubernetes-master-102
    constraints: "root-disk=16G spaces=juju,^etcd-peer,etcd-client,flannel,apiserver,^loadbalancer,^workload"
    num_units: 1
    options:
      channel: 1.10/stable
    bindings:
      "": juju
      kube-api-endpoint: apiserver
      kube-control: apiserver
  kubernetes-worker:
    annotations:
      gui-x: '100'
      gui-y: '850'
    charm: cs:~containers/kubernetes-worker-114
    constraints: "cores=4 mem=4G root-disk=16G spaces=juju,^etcd-peer,etcd-client,flannel,apiserver,loadbalancer,workload"
    expose: true
    num_units: 3
    options:
      channel: 1.10/stable
    bindings:
      "": juju
      kube-control: apiserver
relations:
- - kubernetes-master:kube-api-endpoint
  - kubeapi-load-balancer:apiserver
- - kubernetes-master:loadbalancer
  - kubeapi-load-balancer:loadbalancer
- - kubernetes-master:kube-control
  - kubernetes-worker:kube-control
- - kubernetes-master:certificates
  - easyrsa:client
- - etcd:certificates
  - easyrsa:client
- - kubernetes-master:etcd
  - etcd:db
- - kubernetes-worker:certificates
  - easyrsa:client
- - kubernetes-worker:kube-api-endpoint
  - kubeapi-load-balancer:website
- - kubeapi-load-balancer:certificates
  - easyrsa:client
- - flannel:etcd
  - etcd:db
- - flannel:cni
  - kubernetes-master:cni
- - flannel:cni
- kubernetes-worker:cni
```

You can read more about bindings in bundles, here: https://jujucharms.com/docs/stable/charms-bundles#binding-endpoints-within-a-bundle

## Reference: Endpoints

The following endpoints are available for use in bindings:

| Charm | Endpoint | Description of traffic |
| ----- | -------- | ----------- |
| etcd  | cluster  | ETCD internal (peer) |
| etcd  | db       | ETCD external (client) |
| flannel | cni | Flannel traffic (pod to pod communication) |
| canal | cni | Flannel traffic (pod to pod communication) |
| calico | cni | Calico traffic (pod to pod communication) |
| kubernetes-master | kube-api-endpoint | Main traffic to kube-apiserver, from kubeapi-load-balancer |
| kubernetes-master | kube-control | Secondary traffic to kube-apiserver, from pods |
| kubeapi-load-balancer | website | Traffic to kubeapi-load-balancer, from kubectl, kubelet and kube-proxy |
| kubernetes-worker | kube-control | Traffic to kubelet, from kube-apiserver (health checks) |
