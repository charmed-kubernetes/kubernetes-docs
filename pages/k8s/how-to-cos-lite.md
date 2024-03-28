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
permalink: explain-cos-lite.html
layout: [base, ubuntu-com]
toc: False
---

First, initialize a controller on your preferred cloud platform (vSphere, AWS,
Azure) using Juju. Run the following command, ensuring to replace placeholder
values with your specifics:

```
juju bootstrap --credential $XYZ \
  --debug \
  --model-default automatically-retry-hooks=false \
  --model-default 'logging-config=<root>=DEBUG' \
  --bootstrap-image="juju-ci-root/templates/jammy-test-template" \
  --bootstrap-series=jammy \
  --bootstrap-constraints "arch=amd64" \
  aws tutorial-controller
```

Next, create a microk8s model to act as a deployment cloud for cos-lite:

```
juju add-model --config logging-config='<root>=DEBUG' \
  microk8s-ubuntu aws
```

Deploy Ubuntu on the microk8s-ubuntu model with the following specifications:

```
juju deploy ubuntu --series=focal --constraints="mem=16G cores=8 root-disk=50G"
```

To deploy microk8s on ubuntu, access the unit ubuntu using `juju ssh ubuntu/0`
and follow the configuration steps available at: <https://charmhub.io/topics/canonical-observability-stack/tutorials/install-microk8s#heading--configure-microk8s>

After configuring microk8s, export its kubeconfig file to your current directory:

```
juju ssh ubuntu/0 -- microk8s config > microk8s-config.yaml
```

Now, register microk8s as a Juju cloud:

```
KUBECONFIG=microk8s-config.yaml juju add-k8s microk8s
```

Create a new model for cos-lite on this cloud and deploy cos-lite:

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
This process bootstrapped a controller, created two models (one for Ubuntu
with microk8s deployed, and another for cos-lite), and set up cos-lite's
endpoints for cross-model integration.
Next, proceed to deploy charmed Kubernetes and link it with cos-lite.

Create a model for charmed kubernetes:

```
juju add-model --config logging-config='<root>=DEBUG' charmed-k8s aws
```

Deploy charmed kubernetes:

```
juju deploy charmed-kubernetes
```

Consume cos-lite endpoints:

```
juju consume cos-lite.grafana
juju consume cos-lite.prometheus
```

Deploy the grafana-agent:

```
Juju deploy grafana-agent
```

Relate grafana-agent to k8s and kubernetes-control-plane and kubernetes-worker:

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
