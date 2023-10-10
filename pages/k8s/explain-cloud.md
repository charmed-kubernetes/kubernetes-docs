---
wrapper_template: "templates/docs/markdown.html"
markdown_includes:
  nav: "kubernetes/docs/shared/_side-navigation.md"
context:
  title: "Integrate Charmed Kubernetes with your cloud"
  description: Why should one use cloud integrators
keywords: Cloud, cluster, storage
tags: [operating]
sidebar: k8smain-sidebar
permalink: explain-cloud.html
layout: [base, ubuntu-com]
toc: False
---

The vanilla installation of Kubernetes as provided by Charmed Kubernetes intentionally doesn't presume which cloud infrastructure the charms may be running on, in an effort to provide the same kubernetes experience regardless of the underlying cloud. But there are many cases a cloud operator would like to take advantage of specific cloud features from the cloud provider.  

Many features like Storage Drivers (CSIs), Network Drivers (CNIs), authentication integration, (et al.) require the kubernetes control plane to have authorization to contact the cloud-provider APIs and request access to these features. 

### As an example
If the Charmed Kubernetes installation is on Azure compute nodes, one may wish to employ using AzureDisk for volumes mapped into their Deployments. Charmed Kubernetes provides a means of installing the [azure-cloud-provide charm](https://charmhub.io/azure-cloud-provider) which will apply the appropriate manifests for AzureDisk integration based the release and relations in the cluster.

### Further Reading
For more details, see the various cloud integration pages.

- [AWS](/kubernetes/docs/aws-integration)
- [Azure](/kubernetes/docs/azure-integration)
- [GCP](/kubernetes/docs/gcp-integration)
- [OpenStack](/kubernetes/docs/openstack-integration)
- [vSphere](/kubernetes/docs/vsphere-integration)
- [LXD](/kubernetes/docs/install-local)
- [Equinix Metal](/kubernetes/docs/equinix)


<!-- FEEDBACK -->
<div class="p-notification--information">
  <div class="p-notification__content">
    <p class="p-notification__message">We appreciate your feedback on the documentation. You can
    <a href="https://github.com/charmed-kubernetes/kubernetes-docs/edit/main/pages/k8s/how-to-clouds.md" >edit this page</a>
    or
    <a href="https://github.com/charmed-kubernetes/kubernetes-docs/issues/new" >file a bug here</a>.</p>
  </div>
</div>
