
---
wrapper_template: templates/docs/markdown.html
markdown_includes:
  nav: kubernetes/charmed-k8s/docs/shared/_side-navigation.md
context:
  title: 1.34 Release notes
  description: Release notes for Charmed Kubernetes
keywords: kubernetes, release, notes
tags:
  - news
sidebar: k8smain-sidebar
permalink: 1.34/release-notes.html
layout:
  - base
  - ubuntu-com
toc: False
---
# 1.34

### September 24, 2025 - `charmed-kubernetes --channel 1.34/stable`

The release bundle can also be [downloaded here](https://raw.githubusercontent.com/charmed-kubernetes/bundle/main/releases/1.34/bundle.yaml).

## What's new
### aws-cloud-provider
Subordinate charms don't use constraints (#10)
### aws-iam
Pin dependencies to 1.34 branch
### aws-integrator
[LP#2111261] Tag iam roles and policies with juju-model-uuid (#8)
Pin dependencies to 1.34 branch
### aws-k8s-storage
Subordinate charms don't use constraints (#18)
add missing trust (#19)
### azure-cloud-provider
Pin dependencies to 1.34 branch
### azure-integrator
Pin dependencies to 1.34 branch
### canal
Pin dependencies to 1.34 branch
### containerd
Pin layers to 1.34 layers
### docker-registry
Pin dependencies to 1.34 branch
### easyrsa
Pin layers to 1.34 layers
### etcd
Pin layers to 1.34 layers
### flannel
Pin dependencies to 1.34 branch
### gcp-integrator
Pin dependencies to 1.34 branch
### keepalived
Pin dependencies to 1.34 branch
### kubeapi-load-balancer
Pin dependencies to 1.34 branch
### kubernetes-control-plane
chore: switch integration tests to noble (#391)
Signed-off-by: Reza Abbasalipour <reza.abbasalipour@canonical.com>
fix: support dual stack kubelet node ip addresses (#389)
* fix: support dual stack kubelet node ip addresses
---------
Signed-off-by: Reza Abbasalipour <reza.abbasalipour@canonical.com>
fix: set context for status (#392)
Signed-off-by: Reza Abbasalipour <reza.abbasalipour@canonical.com>
Use `node-base.address` library (#393)
* Use node-base NodeAddress library
* Pin node-base to a commit
* Update src/charm.py
Co-authored-by: Mateo Florido <mateo.florido@canonical.com>
* incorporate review comments
---------
Co-authored-by: Mateo Florido <mateo.florido@canonical.com>
Pin dependencies to 1.34 branch
use `charms.kubernetes-snaps` (#404)
### kubernetes-e2e
Cluster Validation using Canonical K8s (#35)
* Use kube-control v2 to directly relate to k8s
* Update deployment docs integrating with k8s
* Use charmcraft channel
Run e2e tests against canonical k8s and charmed-kubernetes (#41)
Pin dependencies to 1.34 branch
### kubernetes-worker
fix: support dual stack kubelet node ip addresses (#192)
* fix: support dual stack kubelet node ip addresses
---------
Signed-off-by: Reza Abbasalipour <reza.abbasalipour@canonical.com>
Use node-base.address library (#193)
* Use node-base NodeAddress library
* Pin node-base to a commit
* incorporate review comments
Pin dependencies to 1.34 branch
use `charms.kubernetes-snaps` (#202)
### openstack-cloud-controller
Set default TF channel and supported bases
Merge pull request #16 from charmed-kubernetes/tf/pin-noble-variables
Set default TF channel and supported bases
### openstack-integrator
[LP#2110221] Config change and Creds changes validates LB Requests (#19)
* Allows for config changes and creds changes to trigger validation of loadbalancer requets
* pin versions of calver and hatching to install a pinned opentelemetry_api
* revert wheelhouse changes
Allow juju admin to specify o7k endpoint proxy values by charm or model (#18)
* Allow juju admin to specify o7k endpoint proxy values by charm or model
* updated to use new layer on main branch
* Guardrail proxy url
* Adapt to spec KU144
* Share the client proxy-settings
* Rename enumeration from subordinates to integrations
* Swap application name from integrations to clients
* Continue to match KU158 spec as it changes
* Pivot to jmodelproxylib for proxy config
* Remove unused code
* clear lb errors on successful management
* timeout commands and urlopen
* Test reactive methods
* Update to approved ux web-proxy-enable
Pin dependencies to 1.34 branch
### vsphere-cloud-provider
Adds support to integrate with Canonical K8s (#36)
* Adds support to integrate with Canonical K8s
* Confirm on jammy and noble
### vsphere-integrator
Pin dependencies to 1.34 branch

## Component Versions

### Charm/Addons pinned versions
- kube-ovn ?????
- calico ?????
- cephcsi ?????
- cinder-csi-plugin ?????
- coredns ?????
- ingress-nginx ?????
- k8s-keystone-auth ?????
- kube-state-metrics ?????
- kubernetes-dashboard ?????
- openstack-cloud-controller-manager ?????

### Charm default versions
- cloud-provider-vsphere ?????
- vsphere-csi-driver ?????
- cloud-provider-azure ?????
- azuredisk-csi-driver ?????
- cloud-provider-aws ?????
- aws-ebs-csi-driver ?????
- gcp-compute-persistent-disk-csi-driver ?????


## Fixes

A list of bug fixes and other minor feature updates in this release can be found at
[the launchpad milestone page for 1.34](https://launchpad.net/charmed-kubernetes/+milestone/1.34).


## Notes and Known Issues


## Deprecations and API changes

- Upstream

For details of other deprecation notices and API changes for Kubernetes 1.34, please see the
relevant sections of the [upstream release notes][upstream-changelog-1.34].

[upstream-changelog-1.34]: https://github.com/kubernetes/kubernetes/blob/master/CHANGELOG/CHANGELOG-1.34.md#deprecation

<!-- AUTOGENERATED RELEASE 1.34 ABOVE -->


<!--LINKS-->

[rel]: /kubernetes/charmed-k8s/docs/release-notes
