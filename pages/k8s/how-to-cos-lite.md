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
first-class integration between Charmed Kubernetes and COS Lite. This guide
will help you integrate a COS Lite deployment with a Charmed Kubernetes deployment.

This document assumes you have a controller with an installation of
Charmed Kubernetes. If this is not your case, refer to
["how-to-install"][how-to-install].

## Preparing a platform for COS Lite

First, create a Microk8s model to act as a deployment cloud for COS Lite:

```
juju add-model --config logging-config='<root>=DEBUG' \
  microk8s-ubuntu aws
```

Deploy the Ubuntu charm as an application called "microk8s":

```
juju deploy ubuntu microk8s --series=focal --constraints="mem=16G cores=8 root-disk=50G"
```

To actually deploy Microk8s on Ubuntu, access the Microk8s unit using `juju ssh
microk8s/0` and follow the configuration steps available at: [Install
Microk8s][how-to-install].

After configuring Microk8s, export its kubeconfig file to your current directory:

```
juju ssh microk8s/0 -- microk8s config > microk8s-config.yaml
```

Now, register Microk8s as a Juju cloud (see ["juju
add-k8s"][add-k8s] for details on the add-k8s
command):

```
KUBECONFIG=microk8s-config.yaml juju add-k8s microk8s
```

## Deploying COS Lite on the Microk8s cloud

Create a new model for cos-lite on the Microk8s cloud and deploy the cos-lite charm:

```
juju add-model cos-lite microk8s
juju deploy cos-lite
```

Offer cos-lite's endpoints for integration across models:

```
juju offer grafana:grafana-dashboard
juju offer prometheus:receive-remote-write
```

Check the status of these offerings with `juju status --relations` to see
both grafana and prometheus listed.

So far, we've created a model that runs Microk8s on Ubuntu, and added that
model as a Kubernetes cloud to Juju. We then used this cloud as a substrate
for the COS Lite deployment. We therefore have 2 models on the same controller.

This process created two models (one for Ubuntu with Microk8s deployed, and
another for COS Lite), and set up COS Lite's endpoints for cross-model
integration. Next, proceed to integrate charmed-kubernetes with COS Lite.

## Integrating COS Lite with Charmed Kubernetes

Switch to your charmed-kubernetes model:

`juju switch <charmed-kubernetes-model>`

Consume the COS Lite endpoints:

```
juju consume cos-lite.grafana
juju consume cos-lite.prometheus
```

Deploy the grafana-agent:

```
Juju deploy grafana-agent
```

Relate `grafana-agent` to `k8s`, `kubernetes-control-plane` and `kubernetes-worker`:

```
juju integrate grafana-agent:cos-agent k8s:cos-agent
juju integrate grafana-agent:cos-agent kubernetes-control-plane:cos-agent
juju integrate grafana-agent:cos-agent kubernetes-worker:cos-agent
```

Relate `grafana-agent` to the COS Lite offered interfaces:

```
juju integrate grafana-agent grafana
juju integrate grafana-agent prometheus
```

Get the credentials and login URL for Grafana:

```
juju run grafana/0 get-admin-password -m cos-lite
```

The above command will output:

```
admin-password: b9OhxF5ndUDO
url: http://10.246.154.87/cos-lite-grafana
```

The username for this credential is `admin`.

Congratulations! You now have access to a complete observability stack when you
visit the URL and enter the credentials.

Once you feel ready to dive deeper into your shiny new observability platform,
you can head over to the [COS Lite documentation][cos-lite-docs].

<!-- LINKS -->

[how-to-install]: /kubernetes/docs/how-to-install
[add-k8s]: https://juju.is/docs/juju/juju-add-k8s
[cos-lite-docs]: https://charmhub.io/topics/canonical-observability-stack

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
