---
wrapper_template: "templates/docs/markdown.html"
markdown_includes:
  nav: "kubernetes/docs/shared/_side-navigation.md"
context:
  title: "Kubernetes Inclusive Naming"
  description: Kubernetes commitment to inclusivity 
keywords: inclusive, requirements, developer 
tags: [install]
sidebar: k8smain-sidebar 
permalink: inclusive-naming.html 
layout: [base, ubuntu-com]
toc: False
---

The software industry has used words unintentionally which may stir painful emotions in individuals. In an effort
to more clearly state technical details, Canonical Kubernetes strives to improve the language used in its products to 
better reflect its components, relations, status messages, and source code repositories.  We also realize that 
software is built on a trust that renaming some component doesn't break existing working deployments.  Thusly, we will
document all inclusive-naming changes, and take care to make non-breaking adjustments. 

## [Kubernetes Control Plane](kubernetes-control-plane) charm

Ending with the charms release 1.23, Charmed Kubernetes is replacing the charm `kubernetes-master` with 
`kubernetes-control-plane`.  This charm has always hosted applications such as the api-server, controller-manager, 
proxy, and scheduler.  Aside from [`etcd`](etcd), which is provided by a separate charm, these services are considered 
the central kubernetes control plane services and are better represented under this charm name.

See [Upgrading](upgrading) for more details about how to switch to this charm.

## Repository default branch names

Charmed Kubernetes charms have a legacy position of working from a default branch which doesn't accurately reflect
that it is the `main` branch of code. Many charms build also on charm layers and interfaces which are reusable 
source components for these charms. As a part of this progress, the project will transition the names of the default
branches to `main`.


<!-- IMAGES -->



<!-- LINKS -->

[LXD-image]: https://linuxcontainers.org/lxd/docs/master/image-handling
[kubernetes-control-plane]: /kubernetes/docs/charm-kubernetes-control-plane
[etcd]: /kubernetes/docs/charm-etcd
[upgrading]: /kubernetes/docs/upgrading

<!-- FEEDBACK -->
<div class="p-notification--information">
  <p class="p-notification__response">
    We appreciate your feedback on the documentation. You can
    <a href="https://github.com/charmed-kubernetes/kubernetes-docs/edit/main/pages/k8s/inclusive-naming.md" >edit this page</a>
    or
    <a href="https://github.com/charmed-kubernetes/kubernetes-docs/issues/new" >file a bug here</a>.
  </p>
</div>
