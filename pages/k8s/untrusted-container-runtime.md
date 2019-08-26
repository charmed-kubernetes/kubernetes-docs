---
wrapper_template: "base_docs.html"
markdown_includes:
  nav: "shared/_side-navigation.md"
context:
  title: "Untrusted container runtimes"
  description: Configure and use kata containers as the untrusted container runtime
keywords: kata, untrusted runtime, image
tags: [architecture]
sidebar: k8smain-sidebar
permalink: untrusted-container-runtime.html
layout: [base, ubuntu-com]
toc: False
---

From 1.16 onwards, you have the option of attaching Kata Containers to
**Charmed Kubernetes** as part of a pluggable architecture for untrusted
container runtimes, allowing more to be developed in the future.

This runtime gives you the ability to fence containers via a hypervisor,
rather than runc.  If used correctly, this can
[improve security](https://katacontainers.io/collateral/kata-containers-1pager.pdf).

## Caveat

Kata Containers can only be used on bare metal owing to KVM's reliance on the
kvm Kernel module, which can't be installed on cloud instances.

If you see an error similar to

```
Failed create pod sandbox: rpc error: code = Unknown desc = failed to start sandbox container: failed to create containerd task: Could not access KVM kernel module: No such file or directory
qemu-vanilla-system-x86_64: failed to initialize KVM: No such file or directory
```

it's probably due to this.

## Deploying Kata Container

Kata Containers can be deployed to any Charmed Kubernetes cluster that's
running with [containerd](container-runtime).

First, we need to deploy the charm.

```bash
juju deploy cs:~containers/kata
```

After which, we need to relate the charm to the principals.  Currently, this
is only to "anchor" the charm.

```bash
juju add-relation kata kubernetes-master
juju add-relation kata kubernetes-worker
```

Finally, we can relate the untrusted container runtime with the container
runtime.

```bash
juju add-relation kata:untrusted containerd:untrusted

```

All together.

```bash
juju deploy cs:~containers/kata
juju add-relation kata kubernetes-master
juju add-relation kata kubernetes-worker
juju add-relation kata:untrusted containerd:untrusted
```

## Deploying Pods to Kata

### Untrusted Annotation

The simplest way to run your pods with Kata is to annotate them with
`io.kubernetes.cri.untrusted-workload: "true"`.  For example.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx-untrusted
  annotations:
    io.kubernetes.cri.untrusted-workload: "true"
spec:
  containers:
  - name: nginx
    image: nginx

```

### RuntimeClass

If you don't want to taint your workloads as `untrusted`, you can also create
the following `RuntimeClass`.

```yaml
apiVersion: node.k8s.io/v1beta1
kind: RuntimeClass
metadata:
  name: kata
handler: kata
```

After this `RuntimeClass` is created, we can run workloads that are pinned to
the class.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx-kata
spec:
  runtimeClassName: kata
  containers:
  - name: nginx
    image: nginx
```
