---
wrapper_template: "templates/docs/markdown.html"
markdown_includes:
  nav: "kubernetes/docs/shared/_side-navigation.md"
context:
  title: "Integrating COS Lite with Charmed Kubernetes"
  description: Integrating COS Lite with Charmed Kubernetes
keywords: Cloud, cluster, observability
tags: [observability, operating]
sidebar: k8smain-sidebar
permalink: how-to-cos-lite.html
layout: [base, ubuntu-com]
toc: False
---

**Charmed Kubernetes** includes the standard Kubernetes dashboard for
monitoring your cluster. However, it is often advisable to have a monitoring
solution which will run whether the cluster itself is running or not. It may
also be useful to integrate monitoring into existing setups.

To make monitoring your cluster a delightful experience, Canonical provides
first-class integration between charmed-kubernetes and COS Lite. This guide
will help you integrate a COS Lite deployment with a charmed-kubernetes deployment.

This document assumes you have a controller with an installation of
charmed-kubernetes. If this is not your case, refer to
["how-to-install"].(<https://ubuntu.com/kubernetes/docs/how-to-install>)

## Preparing a platform for COS Lite

First, create a microk8s model to act as a deployment cloud for cos-lite:

```
juju add-model --config logging-config='<root>=DEBUG' \
  microk8s-ubuntu aws
```

Deploy Ubuntu on the microk8s-ubuntu model with the following specifications:

```
juju deploy ubuntu microk8s --series=focal --constraints="mem=16G cores=8 root-disk=50G"
```

The above command deploys the ubuntu charm as an application called microk8s.

To deploy microk8s on ubuntu, access the unit ubuntu using `juju ssh microk8s/0`
and follow the configuration steps available at: <https://charmhub.io/topics/canonical-observability-stack/tutorials/install-microk8s#heading--configure-microk8s>

After configuring microk8s, export its kubeconfig file to your current directory:

```
juju ssh microk8s/0 -- microk8s config > microk8s-config.yaml
```

Now, register microk8s as a Juju cloud (see "[juju
add-k8s"](https://juju.is/docs/juju/juju-add-k8s) for details on the add-k8s
command):

```
KUBECONFIG=microk8s-config.yaml juju add-k8s microk8s
```

Create a new model for cos-lite on the microk8s cloud and deploy the cos-lite charm:

```
juju add-model cos-lite microk8s
juju deploy cos-lite
```

Offer cos-lite's endpoints for integration across models:

```
juju offer grafana:grafana-dashboard
juju offer prometheus:receive-remote-write
```

Check the status of these offerings with juju status --relations to see
both grafana and prometheus listed.

So far, we've created a model that runs microk8s on Ubuntu, and added that
model as a Kubernetes cloud to Juju. We then used this cloud as a substrate
for the cos-lite deployment. We therefore have 2 models on the same controller.


This process created two models (one for Ubuntu with microk8s deployed, and
another for cos-lite), and set up cos-lite's endpoints for cross-model
integration. Next, proceed to integrate charmed-kubernetes with COS Lite.

Switch to your charmed-kubernetes model:

`juju switch <charmed-kubernetes-model>`

Consume cos-lite endpoints:

```
juju consume cos-lite.grafana
juju consume cos-lite.prometheus
```

Deploy the grafana-agent:

```
Juju deploy grafana-agent
```

Relate grafana-agent to k8s, kubernetes-control-plane and kubernetes-worker:

```
juju integrate grafana-agent:cos-agent k8s:cos-agent
juju integrate grafana-agent:cos-agent kubernetes-control-plane:cos-agent
juju integrate grafana-agent:cos-agent kubernetes-worker:cos-agent
```

Relate grafana-agent to the cos-lite offerings:

```
juju integrate grafana-agent grafana
juju integrate grafana-agent prometheus
```

Get the credentials and login url for grafana:

```
juju run grafana/0 get-admin-password -m cos-lite

admin-password: b9OhxF5ndUDO
url: http://10.246.154.87/cos-lite-grafana
```

<!-- FEEDBACK -->
<div class="p-notification--information">
  <div class="p-notification__content">
    <p class="p-notification__message">We appreciate your feedback on the documentation. You can
    <a href="https://github.com/charmed-kubernetes/kubernetes-docs/edit/main/pages/k8s/how-to-cos-lite.md" >edit this page</a>
    or
    <a href="https://github.com/charmed-kubernetes/kubernetes-docs/issues/new">file a bug here</a>.</p>
    <p>See the guide to <a href="/kubernetes/docs/how-to-contribute"> contributing </a> or discuss these docs in our <a href="https://chat.charmhub.io/charmhub/channels/kubernetes"> public Mattermost channel</a>.</p>
  </div>
</div>
