---
wrapper_template: "base_docs.html"
markdown_includes:
  nav: "shared/_side-navigation.md"
context:
  title: "CNI with Calico"
  description: How to manage and deploy Kubernetes with Calico
keywords: CNI, networking
tags: [operating]
sidebar: k8smain-sidebar
permalink: cni-with-calico.html
layout: [base, ubuntu-com]
toc: False
---

[Calico][] is a software-defined network solution that can be used with Kubernetes.
Support for Calico in **CDK** is provided in the form of a `calico` subordinate
charm.

Unlike Flannel, Calico provides out-of-the-box support for the
[NetworkPolicy][] feature of Kubernetes, along with different modes of
network encapsulation that advanced users may find useful for optimising
the throughput of their clusters.

## Cloud configuration

Calico's network traffic is filtered on many clouds, and may require
special configuration at the cloud level to support it.

If Calico is configured to use [BGP mode][bgp] (the default), then all of the
Kubernetes instances must be located in the same subnet.

If Calico is configured to use IPIP mode, then the cloud must be configured to
allow IPIP (protocol 4) network traffic.

### AWS

On AWS, it is recommended to run Calico in BGP mode. This usually requires the
creation of a VPC that has only a single subnet associated with it. See Juju's
[Creating an AWS VPC][] documentation for instructions on how to create a VPC
that's compatible with Juju.

After deployment, each AWS instance must be manually configured to disable
source/destination checks. See AWS's [Disabling Source/Destination Checks][]
documentation for instructions.

## Deploying Charmed Kubernetes with Calico

To deploy CDK with Calico, deploy the kubernetes-calico bundle:

```bash
juju deploy cs:~containers/kubernetes-calico
```

The calico bundle is identical to the standard `charmed-kubernetes` bundle with the
exception of replacing flannel with calico. You can apply any customisation overlays
that would apply to `charmed-kubernetes` to this bundle also.

## Calico configuration options

| Name                |  Type  |  Default value                           | Description                                                    |
|=====================|========|==========================================|================================================================|
| calico-node-image   | string | docker.io/calico/node:v3.6.1             | The image id to use for calico/node                            |
| calico-policy-image | string | docker.io/calico/kube-controllers:v3.6.1 | The image id to use for calico/kube-controllers                |
| ipip                | string | Never                                    | IPIP mode. Must be one of "Always", "CrossSubnet", or "Never". |
| nat-outgoing        | bool   | True                                     | Enable NAT on outgoing traffic                                 |

### Checking the current configuration

To check the current configuration settings for Calico, run the command:

```bash
juju config calico
```

### Setting a config option

To set an option, simply run the config command with and additional `<key>=<value>` argument. For example, to disable NAT on outgoing traffic:

```bash
juju config calico nat-outgoing=False
```

Config settings which require additional explanation are described below.

## Calico IPIP configuration

By default, IPIP encapsulation is disabled. To enable IPIP encapsulation, set
the `ipip` charm config to `Always`:

```
juju config calico ipip=Always
```

Alternatively, if you would like IPIP encapsulation to be used for cross-subnet
traffic only, set the `ipip` charm config to `CrossSubnet`:

```
juju config calico ipip=CrossSubnet
```

## Using a private Docker registry

For a general introduction to using a private Docker registry with **CDK**, please
refer to the [Private Docker Registry][] page.

In addition to the steps documented there, you will need to upload the
following images to the registry:

```no-highlight
docker.io/calico/node:v3.6.1
docker.io/calico/kube-controllers:v3.6.1
```

And configure Calico to use the registry:

```bash
export IP=`juju run --unit docker-registry/0 'network-get website --ingress-address'`
export PORT=`juju config docker-registry registry-port`
export REGISTRY=$IP:$PORT
juju config calico \
  calico-node-image=$registry/calico/node:v3.6.1 \
  calico-policy-image=$registry/calico/kube-controllers:v3.6.1
```

## Troubleshooting

If there is an issue with connectivity, it can be useful to inspect the Juju logs.
To see a complete set of logs for Calico

```bash
juju debug-log --replay --include=calico
```

For additional troubleshooting pointers, please see the [dedicated troubleshooting page][troubleshooting].


## Useful links

-

<!-- LINKS -->

[NetworkPolicy]: https://kubernetes.io/docs/concepts/services-networking/network-policies/
[Creating an AWS VPC]: https://docs.jujucharms.com/2.5/en/charms-fan-aws-vpc
[Disabling Source/Destination Checks]: https://docs.aws.amazon.com/vpc/latest/userguide/VPC_NAT_Instance.html#EIP_Disable_SrcDestCheck
[private docker registry]: /kubernetes/docs/docker-registry
[bgp]: https://docs.projectcalico.org/v3.7/networking/service-advertisement#about-advertising-kubernetes-services-over-bgp
[Calico]: https://www.projectcalico.org/
[troubleshooting]: /kubernetes/docs/troubleshooting
[quickstart]:  /kubernetes/docs/quickstart
[install-manual]:  /kubernetes/docs/install-manual
