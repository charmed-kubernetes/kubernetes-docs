---
wrapper_template: "templates/docs/markdown.html"
markdown_includes:
  nav: "kubernetes/docs/shared/_side-navigation.md"
context:
  title: "How to use CDK add-on Operator Charms"
  description: Explaining how to install and configure addon operator charms with Charmed Kubernetes.
keywords: operating, add-ons, addons, config
tags: [operating]
sidebar: k8smain-sidebar
permalink: how-to-addons.html
layout: [base, ubuntu-com]
toc: False
---

This page gives step by step guides for deploying the Operator Charm
versions of the **Charmed Kubernetes** addons. For an explanation
of these addons, please see the [addons page][].

##  Steps for all addons

In order for Juju to deploy Kubernetes applications, it will need to fetch
information and be configured to work with your Kubernetes cluster. 
These steps assume:
 * You have administrative access to the Charmed Kubernetes cluster


#### 1. Install kubectl 

You will need **kubectl** to be able to use your Kubernetes cluster. If it is not already
installed, it is easy to add via a snap package:

```bash
sudo snap install kubectl --classic
```

For other platforms and install methods, please see the
[Kubernetes documentation][kubectl].

#### 2. Retrieve the required configuration

Juju makes use of the **kubectl** config file to access the Kubernetes cluster.
For Linux-based systems, this file is usually located at `~/.kube/config`

If you are already using `kubectl` to access other clusters you may wish to merge
the configurations rather than replacing it. The following command fetches the 
config file for `kubectl` from the Kubernetes cluster and saves it to the default location:

```bash
juju scp kubernetes-control-plane/0:config ~/.kube/config
```

#### 3. Add the Kubernetes cluster to Juju

Next, add your Kubernetes cluster as a cloud to your current Juju controller:

```bash
juju add-k8s ck8s --controller $(juju switch | cut -d: -f1)
```

You may replace `ck8s` with whatever name you want to use to refer to this cluster, but
remember to substitute in the correct name in the remaining examples in this page.


#### 4. Add a model

To be able to deploy operators you will also need to create a Juju model in the cluster:

```
juju add-model my-k8s-model ck8s
```

Again, you should replace `my-k8s-model` with a name you want to use to refer to
this Kubernetes model. As well as creating a Juju model, this action will also
create a Kubernetes namespace of the same name which you can use to easily
monitor or manage operators you install on the cluster.






<div class="p-notification--caution is-inline">
  <div markdown="1" class="p-notification__content">
    <span class="p-notification__title">Caution:</span>
    <p class="p-notification__message">If you have multiple clusters you will need to manage the config file rather than just
    replacing it. See the <a href="https://kubernetes.io/docs/tasks/access-application-cluster/configure-access-multiple-clusters/">
    Kubernetes documentation</a> for more information on managing multiple clusters.</p>
  </div>
</div>Install and configure kubectl

You will need **kubectl** to be able to use your Kubernetes cluster. If it is not already
installed, it is easy to add via a snap package:

```bash
sudo snap install kubectl --classic
```

For other platforms and install methods, please see the
[Kubernetes documentation][kubectl].

The config file for accessing the newly deployed cluster is stored in the cluster itself and will be available
as soon as the installation has settled. You should use the following command to retrieve it (create a
**.kube** directory if it was not created after kubectl installation):

```bash
juju scp kubernetes-control-plane/0:config ~/.kube/config
```

<div class="p-notification--caution is-inline">
  <div markdown="1" class="p-notification__content">
    <span class="p-notification__title">Caution:</span>
    <p class="p-notification__message">If you have multiple clusters you will need to manage the config file rather than just
    replacing it. See the <a href="https://kubernetes.io/docs/tasks/access-application-cluster/configure-access-multiple-clusters/">
    Kubernetes documentation</a> for more information on managing multiple clusters.</p>
  </div>
</div>

## 2. Add your cluster to Juju 
1. add a model
1. Using `juju-switch`

## CoreDNS
Sourced from: <https://github.com/coredns/deployment.git>

CoreDNS has been the default DNS provider for Charmed Kubernetes clusters
since 1.14.

For additional control over CoreDNS, you can also deploy it into the cluster
using the [CoreDNS Kubernetes operator charm][coredns-charm]. To do so, set
the `dns-provider` [kubernetes-control-plane configuration][] option to `none` and
deploy the charm into a Kubernetes model on your cluster. You will also need
to cross-model relate it to kubernetes-control-plane.

With the Charmed Kubernetes model selected from Juju, run:

```bash
juju config kubernetes-control-plane dns-provider=none
```

Use `juju-switch`to identify and switch to the controller set up for your
Kubernetes deployment. For example, 
juju add-k8s k8s-cloud --controller mycontroller
juju add-model k8s-model k8s-cloud
juju deploy coredns --channel=latest/stable --trust
juju offer coredns:dns-provider
juju consume -m cluster-model k8s-model.coredns
juju relate -m cluster-model coredns kubernetes-control-plane
```

Once everything settles out, new or restarted pods will use the CoreDNS
charm as their DNS provider. The CoreDNS charm config allows you to change
the cluster domain, the IP address or config file to forward unhandled
queries to, add additional DNS servers, or even override the Corefile entirely.

## Kubernetes Dashboard
Sourced from: <https://github.com/kubernetes/dashboard.git>

The Kubernetes Dashboard is a standard and easy way to inspect and
interact with your Kubernetes cluster.

![dashboard image](https://assets.ubuntu.com/v1/4ec7e026-ck8s-dashboard.png)

For instructions on how to access the dashboard, please see the
[Operations page][].

If desired, the dashboard can be disabled:

```bash
juju config kubernetes-control-plane enable-dashboard-addons=false
```

...and re-enabled with:

```
juju config kubernetes-control-plane enable-dashboard-addons=true
```

For additional control over the Kubernetes Dashboard, you can also deploy it into
the cluster using the [Kubernetes Dashboard operator charm][kubernetes-dashboard-charm].
To do so, set the `enable-dashboard-addons` [kubernetes-control-plane configuration][]
option to `false` and deploy the charm into a Kubernetes model on your cluster:

```bash
juju config -m cluster-model kubernetes-control-plane enable-dashboard-addons=false
juju add-k8s k8s-cloud --controller mycontroller
juju add-model k8s-model k8s-cloud
juju deploy kubernetes-dashboard --channel=latest/stable --trust
```

For accessing the Dashboard use the same instructions in the [Operations page][].

## Nvidia plugin
Sourced from: <https://github.com/NVIDIA/k8s-device-plugin.git>

This plugin enables GPU support for nodes when running with the appropriate
resources. The plugin is set to 'auto' by default, so it only runs when
the drivers and GPU resources are available on the host system.

If you wish to disable the plugin entirely, it can be turned off by setting the
`kubernetes-control-plane` configuration:

```bash
juju config kubernetes-control-plane enable-nvidia-plugin="false"
```

The default setting is "auto", and it is also possible to set the configuration
to "true", which will load the plugin regardless of whether the resources were
found, which may be useful for troubleshooting.

There is more information on using GPUs for workloads, and working with
public cloud GPU instances, on the [GPU workers page][].

## OpenStack/Keystone
Sourced from: <https://github.com/kubernetes/cloud-provider-openstack.git>

This addon provides the components required to enable **Charmed Kubernetes**
to work with LDAP/Keystone for Authentication and Authorisation.

Please refer to the [LDAP and Keystone page][] for more information on using
this feature.


## Metrics
**Charmed Kubernetes** provides multiple means of installing services `kube-state-metrics` and `metrics-server` for monitoring some health aspects of the kubernetes cluster.

### Built-in Addons
For each **Charmed Kubernetes** release, baked into the snap which the charm deploys into the `kubernetes-control-plane` charm, are two metrics services.  
* `kube-state-metrics` - a fixed commit aligned with the latest-at-the-time release
* `metrics-server` - a set of kubernetes components defined by kubernetes as an in-tree addon

Both `kube-state-metrics` and `metrics-server` applications can be disabled with:

```bash
juju config kubernetes-control-plane enable-metrics=false
```

...or re-enabled with:
```bash
juju config kubernetes-control-plane enable-metrics=true
```

### Kube-State Metrics
Sourced from: <https://github.com/kubernetes/kube-state-metrics.git>

Kube-State-Metrics is described by upstream docs: 
> kube-state-metrics (KSM) is a simple service that listens to the Kubernetes API server and generates metrics about the state of the objects. ... It is not focused on the health of the individual Kubernetes components, but rather on the health of the various objects inside, such as deployments, nodes and pods.

You may follow the installation instructions from [kube-state-metrics example][]

#### Juju Deployment
`kube-state-metrics` can also be deployed as a juju charm.

One only needs to [add a k8s cloud][] so that juju exposes a means of installing Kubernetes operators into the kubernetes-cluster.

Deploy the [kube-state-metrics-operator][] charm into this kubernetes model with:

```bash
juju deploy kube-state-metrics --trust
juju relate kube-state-metrics prometheus  # if a prometheus application is deployed in the same model
```


### Kubernetes Metrics Server
The Kubernetes Metrics server is described by the upstream docs:

*** "Metrics Server is a scalable, efficient source of container resource metrics for Kubernetes built-in autoscaling pipelines.
 Metrics Server collects resource metrics from Kubelets and exposes them in Kubernetes apiserver through Metrics API for use by Horizontal Pod Autoscaler and Vertical Pod Autoscaler. Metrics API can also be accessed by `kubectl top`, making it easier to debug autoscaling pipelines."***

* In-Tree addon - <https://github.com/kubernetes/kubernetes/tree/master/cluster/addons/metrics-server>
* Out-of-Tree - <https://github.com/kubernetes-sigs/metrics-server.git>

Since version 1.24, the `metrics-server` can be deployed into the cluster just like any other kubernetes application.

In order to deploy a different version of the metrics-server, first you must disable the built-in service while ensuring the kubernetes-api service still allows the [aggregation-extentions][].

```bash
juju config kubernetes-control-plane enable-metrics=false
juju config kubernetes-control-plane api-aggregation-extension=true
```

After which, one may follow the upstream deployment instructions from [metrics-server releases][]

#### Juju Deployment
The `metrics-server` can also be deployed as a juju charm.

One only needs to [add a k8s cloud][] so that juju exposes a means of installing Kubernetes operators into the kubernetes-cluster.

Deploy the [kubernetes-metrics-server][] charm into this kubernetes model with:

```bash
juju deploy kubernetes-metrics-server
```

This charm offers the following options 
* upgrade the release of the `metrics-server` via config
  ```bash
  juju config kubernetes-metrics-server release="v0.6.0"
  ```
* adjust the base image registry if the cluster demands a private registry
  ```bash
  juju config kubernetes-metrics-server image-registry="my.registry.server:5000"
  ```
* adjust the arguments of the running service
  ```bash
  juju config kubernetes-metrics-server extra-args="--kubelet-insecure-tls"
  ```


<!-- LINKS -->
[addons page]: /kubernetes/docs/cdk-addons
[Operations page]: /kubernetes/docs/operations
[kubernetes-control-plane configuration]: https://charmhub.io/kubernetes-control-plane/configure
[Storage documentation]: /kubernetes/docs/storage
[GPU workers page]: /kubernetes/docs/gpu-workers
[LDAP and Keystone page]: /kubernetes/docs/ldap
[monitoring docs]: /kubernetes/docs/monitoring
[coredns-charm]: https://charmhub.io/coredns
[kubernetes-dashboard-charm]: https://charmhub.io/kubernetes-dashboard
[kube-state-metrics example]: https://github.com/kubernetes/kube-state-metrics/tree/master/examples/standard
[metrics-server releases]: https://github.com/kubernetes-sigs/metrics-server/releases
[add a k8s cloud]: https://juju.is/docs/olm/get-started-on-kubernetes#heading--register-the-cluster-with-juju
[kubernetes-metrics-server]: https://charmhub.io/kubernetes-metrics-server
[aggregation-extentions]: https://kubernetes.io/docs/tasks/extend-kubernetes/configure-aggregation-layer/
