---
wrapper_template: "templates/docs/markdown.html"
markdown_includes:
  nav: "kubernetes/docs/shared/_side-navigation.md"
context:
  title: "Charmed Kubernetes on Azure"
  description: Running Charmed Kubernetes on Azure using the azure-cloud-provider.
keywords: azure, integrator, cloud-provider
tags: [install]
sidebar: k8smain-sidebar
permalink: azure-integration.html
layout: [base, ubuntu-com]
toc: False
---

**Charmed Kubernetes** will run seamlessly on Microsoft Azure<sup>&reg;</sup>.
With the addition of the `azure-cloud-provider`, your cluster will also be able
Azure native features as defined by the out-of-tree definitions.


## Azure Cloud Provider

The [`azure-cloud-provider`][azure-cloud-provider] charm gathers 
credentials from the [`azure-integrator`][azure-integrator] charm, and deploys
configurable versions of the [cloud-provider][] and [azure-disk][] into the
cluster rather than using the built-in cloud-providers within the kubernetes binaries.
After installation, the cluster can identify each node's providerID, create loadbalancers, and create AzureDisk volumes.

### Installing

If you install **Charmed Kubernetes** [using the Juju bundle][install],
you can add the azure-cloud-provider at the same time by using the following
overlay file ([download it here][asset-azure-cloud-overlay]):

```yaml
description: Charmed Kubernetes overlay to add native Azure support.
applications:
  kubernetes-control-plane:
    options:
      register-with-taints: ""
      allow-privileged: "true"
  azure-integrator:
    charm: azure-integrator
    num_units: 1
    trust: true
  azure-cloud-provider:
    charm: azure-cloud-provider

relations:
- - azure-cloud-provider:certificates
  - easyrsa:client   # or whichever application supplies cluster certs
- - azure-cloud-provider:kube-control
  - kubernetes-control-plane:kube-control
- - azure-cloud-provider:external-cloud-provider
  - kubernetes-control-plane:external-cloud-provider
- - azure-cloud-provider:azure-integration
  - azure-integrator:clients
```

To use this overlay with the **Charmed Kubernetes** bundle, it is specified
during deploy like this:

```bash
juju deploy charmed-kubernetes --overlay azure-cloud-overlay.yaml --trust
```

... and remember to fetch the configuration file!

```bash
juju scp kubernetes-control-plane/0:config ~/.kube/config
```

<div class="p-notification--information">
  <div class="p-notification__content">
    <p class="p-notification__message">A standard install of Charmed Kubernetes will use more resources than the current quotas allocated to a new Azure account. If you see error messages saying allocating machines would exceed your quota, you will need to log a <a href="https://docs.microsoft.com/en-us/azure/azure-portal/supportability/regional-quota-requests">support request with Azure</a> to increase the quota accordingly.</p>
  </div>
</div>

<div class="p-notification--caution is-inline">
  <div class="p-notification__content">
    <span class="p-notification__title">Resource usage:</span>
    <p class="p-notification__message">By relating to this charm, other charms can directly allocate resources, such
    as managed disks and load balancers, which could lead to cloud charges and
    count against quotas. Because these resources are not managed by Juju, they
    will not be automatically deleted when the models or applications are
    destroyed, nor will they show up in Juju's status or GUI. It is therefore up
    to the operator to manually delete these resources when they are no longer
    needed, using the Azure management website or API.</p>
  </div>
</div>

## Storage

This section describes creating a busybox pod with a persistent volume claim
backed by
Azure's Disk Storage.

### 1. Use the provided storage class using the `azuredisk-csi-provisioner` provisioner:

```bash
kubectl describe sc csi-azure-default
```

### 2. Create a persistent volume claim using that storage class:

```bash
kubectl create -f - <<EOY
kind: PersistentVolumeClaim
apiVersion: v1
metadata:
  name: testclaim
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 100Mi
  storageClassName: csi-azure-default
EOY
```

### 3. Create the busybox pod with a volume using that PVC:

```bash
kubectl create -f - <<EOY
apiVersion: v1
kind: Pod
metadata:
  name: busybox
  namespace: default
spec:
  containers:
    - image: busybox
      command:
        - sleep
        - "3600"
      imagePullPolicy: IfNotPresent
      name: busybox
      volumeMounts:
        - mountPath: "/pv"
          name: testvolume
  restartPolicy: Always
  volumes:
    - name: testvolume
      persistentVolumeClaim:
        claimName: testclaim
EOY
```

Charmed Kubernetes can make use of additional types of storage - for more
information see the [storage documentation][storage].

## Azure load-balancers for services

The following commands start the 'hello-world' pod behind an Azure-backed
load-balancer.

Here are the commands for Kubernetes 1.25+ and above as the kubectl run command was deprecated:

```bash
# Kubernetes 1.25+
kubectl create deployment hello-world --image=gcr.io/google-samples/hello-app:1.0  --port=8080
kubectl expose deployment hello-world --type=LoadBalancer --name=hello
watch kubectl get svc -o wide --selector=app=hello-world
```

You can then verify this works by loading the described IP address (on port
8080!) in a browser.

For more configuration options and details of the permissions which the integrator uses,
please see the [charm page][azure-cloud-provider].

## Azure load-balancers for the control plane

With revision 1015 and later of the `kubernetes-control-plane` charm, Charmed
Kubernetes can also use Azure native load balancers in front of the control
plane, replacing the need to deploy the `kubeapi-load-balancer` charm. The
`kubernetes-control-plane` charm supports two relation endpoints, `loadbalancer-external`
for a publicly accessible load balancer which can be used by external clients as
well as the control plane, and `loadbalancer-internal` for a non-public load
balancer which can only be used by the rest of the control plane but not by
external clients.

<!-- LINKS -->

[asset-azure-cloud-overlay]: https://raw.githubusercontent.com/charmed-kubernetes/bundle/main/overlays/azure-cloud-overlay.yaml

[storage]: /kubernetes/docs/storage
[azure-cloud-provider]: https://charmhub.io/azure-cloud-provider/docs
[azure-integrator]: https://charmhub.io/azure-integrator/docs

[install]: /kubernetes/docs/install-manual

<!-- FEEDBACK -->
<div class="p-notification--information">
  <div class="p-notification__content">
    <p class="p-notification__message">We appreciate your feedback on the documentation. You can
    <a href="https://github.com/charmed-kubernetes/kubernetes-docs/edit/main/pages/k8s/azure-cloud-provider.md" >edit this page</a>
    or
    <a href="https://github.com/charmed-kubernetes/kubernetes-docs/issues/new" >file a bug here</a>.</p>
  </div>
</div>

