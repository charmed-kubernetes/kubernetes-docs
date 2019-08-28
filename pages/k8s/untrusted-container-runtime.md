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

Beginning with **Charmed Kubernetes** 1.16, the
[Kata Containers](https://katacontainers.io) runtime can be used with
containerd to safely run insecure or untrusted pods. When enabled, Kata
provides hypervisor isolation for pods that request it, while trusted pods can
continue to run on a shared kernel via runc. The instructions below
demonstrate how to configure and use
[Kata Containers](https://katacontainers.io).

## Caveat

Due to their reliance on the KVM kernel module, Kata Containers can only be used on hosts that support virtualisation. Attempting to use Kata on a host that doesn't support virtualisation may result in an error similar to this one:

```
Failed create pod sandbox: rpc error: code = Unknown desc = failed to start sandbox container: failed to create containerd task: Could not access KVM kernel module: No such file or directory
qemu-vanilla-system-x86_64: failed to initialize KVM: No such file or directory
```

## Deploying Kata Container

Kata Containers can be deployed to any Charmed Kubernetes cluster that's
running with [containerd](container-runtime).

### New Cluster

After bootstrapping a Juju controller, you can deploy Charmed Kubernetes with
the following YAML overlay:

```yaml
applications:
  kata:
    charm: cs:~containers/kata
relations:
- - kata:untrusted
  - containerd:untrusted
- - kata
  - kubernetes-master
- - kata
  - kubernetes-worker

```

Save this YAML and then deploy:

```bash
juju deploy charmed-kubernetes --overlay kata.yaml
```

### Existing Cluster

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

## Deploying pods to Kata

### Untrusted annotation

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
