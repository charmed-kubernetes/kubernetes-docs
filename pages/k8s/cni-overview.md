---
wrapper_template: "base_docs.html"
markdown_includes:
  nav: "shared/_side-navigation.md"
context:
  title: "CNI overview"
  description: How to manage and deploy Kubernetes with flannel, calico, canal or Tigera Secure EE
keywords: CNI, networking
tags: [operating]
sidebar: k8smain-sidebar
permalink: cni-overview.html
layout: [base, ubuntu-com]
toc: False
---

Managing a network where containers can interoperate efficiently is very important.
Kubernetes has adopted the Container Network Interface(CNI) specification for managing
network resources on a cluster. This relatively simple specification makes it easy for
Kubernetes to interact with a wide range of CNI-based software solutions.

With the  **Charmed Distribution of Kubernetes<sup>&reg;</sup>**, these networking
'plug-ins' are deployed as subordinate charms with each  node running as a
`kubernetes-master` or `kubernetes-worker`, and ensure the smooth running of the
cluster. It is possible to choose one of several different CNI providers for **CDK**, which
are listed below:

## Supported CNI options

The currently supported CNI solutions for **CDK** are:

 -   Flannel
 -   Calico
 -   Canal
 -   Tigera Secure EE

By default, **CDK** will deploy the cluster using flannel. To chose a different CNI provider,
either make that choice during a `conjure-up` install:

![conjure-up controller menu](https://assets.ubuntu.com/v1/cd3e83d6-CDK-network.png)

Or follow the links in the list above to see how to manually install  with a different CNI
option.

## Migrating to a different CNI solution

As networking is a fundamental part of the cluster, changing the network on a live cluster
is not straightforward. Currently it is recommended to create a new cluster with **CDK**
using the desired option. When [federation][] becomes part of a future release of
Kubernetes, such a migration should be manageable with no downtime.

Changing the CNI option on a running cluster in any other way carries inherent risks of
downtime and/or loss of data. However, with this understood there are a number of
ways to change the CNI provider for a running cluster:

<<WARNING>>
