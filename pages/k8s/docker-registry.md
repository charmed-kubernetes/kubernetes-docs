---
wrapper_template: "kubernetes/docs/base_docs.html"
markdown_includes:
  nav: "kubernetes/docs/shared/_side-navigation.md"
context:
  title: "Private Docker Registry"
  description: How to use a private Docker registry to serve Docker images to your Kubernetes cluster components.
keywords: juju, docker, registry
tags: [operating]
sidebar: k8smain-sidebar
permalink: docker-registry.html
layout: [base, ubuntu-com]
toc: False
---

The [docker-registry][registry-charm] charm facilitates the storage and
distribution of container images. Include this in a **Kubernetes**
deployment to provide images to cluster components without requiring
access to public registries.
See [https://docs.docker.com/registry/][upstream-registry] for
details.

## Deploy

The registry is deployed as a stand-alone application. Many deployment
scenarios are described in the [charm readme][registry-charm]. The most common
scenario for **Kubernetes** integration is to configure a registry with TLS
and basic (htpasswd) authentication enabled.

If needed, consult the [quickstart guide][quickstart] to install
**Charmed Kubernetes**. Then deploy and configure `docker-registry` as
follows.

```bash
juju deploy ~containers/docker-registry
juju add-relation docker-registry easyrsa:client
juju config docker-registry \
  auth-basic-user='admin' \
  auth-basic-password='password'
```

### Custom Certificates

Relating `docker-registry` to `easyrsa` above will generate new TLS data
to support secure communication with the registry. Alternatively, custom
TLS data may be provided as base64-encoded config options to the charm:

```bash
juju config docker-registry \
  tls-ca-blob=$(base64 /path/to/ca) \
  tls-cert-blob=$(base64 /path/to/cert) \
  tls-key-blob=$(base64 /path/to/key)
```

### Proxied Registry

Advanced networking or highly available deployment scenarios may require
multiple `docker-registry` units to be deployed behind a proxy. In this case,
the network information of the proxy will be shared with the container runtime
units when the registry is related.

<div class="p-notification--information">
  <p markdown="1" class="p-notification__response">
    <span class="p-notification__status">Note:</span>
SSL pass-thru is supported between 'docker-registry' and 'haproxy', though
manual configuration is required. The recommended approach for a proxied
registry is to disable SSL on 'docker-registry' prior to relating it to
'haproxy'. Consult the 'docker-registry' charm readme if SSL is required in a
proxied environment.
  </p>
</div>

The environment described in the `Deploy` section above can be adjusted to
create a highly available registry as follows:

```bash
juju deploy haproxy
juju add-unit docker-registry
juju remove-relation docker-registry easyrsa:client
juju add-relation docker-registry haproxy:reverseproxy
```

<div class="p-notification--information">
  <p markdown="1" class="p-notification__response">
    <span class="p-notification__status">Note:</span>
With multiple registry units deployed, the proxy relation allows for a
highly available deployment. Load balancing across multiple registry units is
not supported.
  </p>
</div>

## Verify

Make note of the registry address. By default, this address is only accessible
within the deployment model. See the [charm readme][registry-charm] for host
and proxy configuration options if desired.

```bash
export IP=`juju run --unit docker-registry/0 'network-get website --ingress-address'`
export PORT=`juju config docker-registry registry-port`
export REGISTRY=$IP:$PORT
```

Verify basic authentication is working:

```bash
juju run --unit docker-registry/0 "docker login -u admin -p password $REGISTRY"
Login Succeeded
...
```

## Connecting to a Charmed Kubernetes cluster

Relate the deployed registry to the appropriate
[container runtime][container-runtime] for your cluster. This configures
the runtime with authentication, proxy, and/or TLS data from the registry.

### Containerd

```bash
juju add-relation docker-registry containerd
```

### Docker

```bash
juju add-relation docker-registry docker
```

## Kubernetes images

A list of images that may be used by **Charmed Kubernetes** can be found in
the [container-images.txt][container-images-txt] document. This is a
comprehensive list sorted by release; not all images are required for all
deployments. Take note of the images required by your deployment that will
need to be hosted in your private registry.

## Hosting images

To make an image available in the deployed registry, it must be tagged and
pushed. As an example, push the `defaultbackend-amd64` image to
`docker-registry`:

```bash
juju run-action docker-registry/0 \
  push \
  image=k8s.gcr.io/defaultbackend-amd64:1.5 \
  tag=$REGISTRY/defaultbackend-amd64:1.5 \
  --wait
...
  results:
    outcome: success
    raw: pushed 172.31.28.74:5000/k8s.gcr.io/defaultbackend-amd64:1.5
  status: completed
...
```

The above procedure should be repeated for all required images.

## Using hosted images

The image registry used by **Charmed Kubernetes** is controlled by a
`kubernetes-master` config option. Configure `kubernetes-master` to use your
private registry as follows:

```bash
juju config kubernetes-master image-registry=$REGISTRY
```

<!-- LINKS -->

[registry-charm]: http://jujucharms.com/u/containers/docker-registry
[upstream-registry]: https://docs.docker.com/registry/
[quickstart]: /kubernetes/docs/quickstart
[container-runtime]: /kubernetes/docs/container-runtime
[container-images-txt]: https://github.com/charmed-kubernetes/bundle/blob/master/container-images.txt

<!-- FEEDBACK -->
<div class="p-notification--information">
  <p class="p-notification__response">
    We appreciate your feedback on the documentation. You can 
    <a href="https://github.com/charmed-kubernetes/kubernetes-docs/edit/master/pages/k8s/docker-registry.md" class="p-notification__action">edit this page</a> 
    or 
    <a href="https://github.com/charmed-kubernetes/kubernetes-docs/issues/new" class="p-notification__action">file a bug here</a>.
  </p>
</div>
