---
wrapper_template: "kubernetes/docs/base_docs.html"
markdown_includes:
  nav: "kubernetes/docs/shared/_side-navigation.md"
context:
  title: "Release notes"
  description: Release notes for CDK
keywords: kubernetes,  release, notes
tags: [news]
sidebar: k8smain-sidebar
permalink: release-notes.html
layout: [base, ubuntu-com]
toc: False
---

# 1.18+ck1 Bugfix release

### June 11, 2020 - [charmed-kubernetes-464](https://api.jujucharms.com/charmstore/v5/charmed-kubernetes-464/archive/bundle.yaml)

Before upgrading from 1.17 or earlier, please read the
[upgrade notes](/kubernetes/docs/upgrade-notes).

## What's new

- New options for custom TLS data in container runtime charms

All container runtime subordinate charms now support a `custom-registry-ca`
option that can be used to specify a `base64` encoded Certificate Authority
(CA) certificate. The value set here will be installed as a system-wide
trusted CA. See the
[related issue](https://bugs.launchpad.net/layer-container-runtime-common/+bug/1831153)
for more details.

For users that require custom TLS configuration per registry, the `containerd`
subordinate charm has expanded the `custom_registries` config option to
support `ca_file`, `cert_file`, and `cert_key`. These can be set for each
custom registry to enable TLS without altering the system-wide trusted CAs.
See the
[related issue](https://bugs.launchpad.net/charm-containerd/+bug/1879347)
for more details.

Both of the above options allow the container runtime located on
`kubernetes-worker` units to pull containers from a registry that utilizes
custom TLS certificates.

- New memory constraint for `kubeapi-load-balancer`

Deploying Charmed Kubernetes now requires a minimum of 4GB of RAM for the
`kubeapi-load-balancer`. This addresses OOM errors reported in the
[related issue](https://bugs.launchpad.net/charmed-kubernetes-bundles/+bug/1873044).

- Updated profile when deploying to LXD

An updated LXD profile has been included in `kubernetes-master` and
`kubernetes-worker` charms. This resolves an
[issue](https://bugs.launchpad.net/charm-kubernetes-worker/+bug/1876618)
where containers would fail to start in a LXD environment.

## Fixes

Bug fixes included in this release can be found at
[https://launchpad.net/charmed-kubernetes/+milestone/1.18+ck1](https://launchpad.net/charmed-kubernetes/+milestone/1.18+ck1).

# 1.18

### April 13, 2020 - [charmed-kubernetes-430](https://api.jujucharms.com/charmstore/v5/charmed-kubernetes-430/archive/bundle.yaml)

Before upgrading, please read the [upgrade notes](/kubernetes/docs/upgrade-notes).

## What's new

- New SSL options for nginx-ingress-controller

New configuration options on the kubernetes-worker charm,
`ingress-default-ssl-certificate` and `ingress-default-ssl-key`, allow you to
configure nginx-ingress-controller with your own SSL certificate for serving
Kubernetes ingress traffic.

- Multus support

This release of Charmed Kubernetes introduces support for
[Multus](https://github.com/intel/multus-cni), a CNI provider that makes it
possible to attach multiple network interfaces to your pods.

Along the way, we've also updated existing charms to make it possible for
multiple CNI providers to be deployed together in the same cluster.

For more details on Multus support in Charmed Kubernetes and how to get started,
please refer to the [Multus documentation page](/kubernetes/docs/cni-multus).

- CIS Benchmark 1.5.0

The `cis-benchmark` action now supports version 1.5.0 of the CIS Kubernetes Benchmark.
See the [CIS compliance](/kubernetes/docs/cis-compliance) page for information on
running this action on Charmed Kubernetes components.

- Containerd version hold

The version of [containerd](https://containerd.io/) will now be held. This means 
that the version of [containerd](https://containerd.io/) will not be upgraded along
with the charm. To update containerd to the latest stable, currently 1.3.3, you can
call the `upgrade-containerd` action:

```bash
juju run-action --wait containerd/0 upgrade-containerd
```

This will perform the upgrade and return any output. If you have more than
one unit of containerd,  you should run this on each unit. The upgrades can be
staggered to avoid downtime.

## Component Upgrades

Many of the components in Charmed Kubernetes 1.18 have been upgraded. The following list
highlights some of the more notable version changes:

- containerd 1.3.3 (see above)
- coredns 1.6.7
- dashboard 2.0.0-rc5
- etcd 3.3.15
- openstack-provider 1.17

## Fixes

A list of bug fixes and other minor feature updates in this release can be found at
[https://launchpad.net/charmed-kubernetes/+milestone/1.18](https://launchpad.net/charmed-kubernetes/+milestone/1.18).

## Notes / Known Issues

- Heapster, InfluxDB, Grafana addons have been removed from `cdk-addons`

Heapster was initially [deprecated][heapster-deprecation] in 1.11; users
were encouraged to move to the `metrics-server` for similar functionality.
With 1.18, the `cluster-monitoring` addons (Heapster, InfluxDB, and Grafana)
have been removed from the Kubernetes source tree and therefore removed from
the `cdk-addons` snap as well. Customers relying on these addons should
migrate to a `metrics-server` solution prior to upgrading. Note: these
removals do not affect the Kubernetes Dashboard nor the methods described in
[Monitoring Charmed Kubernetes](/kubernetes/docs/monitoring).

- Containerd cannot pull images from a registry with TLS mutual authentication

An issue with the `containerd` charm prevents pulling images from a private
container registry when TLS mutual authentication is enabled. Where possible,
users can workaround this issue by disabling mutual authentication on the
registry. More details can be found in the following bug:

https://bugs.launchpad.net/charm-containerd/+bug/1853653

- New provisioner value for Cinder storage classes

The new version of the openstack-provisioner includes an upstream change
to the `provisioner` field for storage classes using Cinder. The `cdk-cinder`
storage class will be automatically updated, but any manually created storage
classes will need to be edited and the `provisioner` field changed to
`cinder.csi.openstack.org`. Existing volumes will be unaffected, but new
PVCs using those storage classes will hang until the storage class is updated.

=======
# 1.17+ck2 Bugfix release

### March 2, 2020 - [charmed-kubernetes-410](https://api.jujucharms.com/charmstore/v5/charmed-kubernetes-410/archive/bundle.yaml)

## Fixes

CephFS is now supported in Charmed Kubernetes. This allows for ReadWriteMany volumes
which can be attached to multiple pods. More information can be found in the
[storage documentation](/kubernetes/docs/storage).

Additional bug fixes included in this release can be found at
[https://launchpad.net/charmed-kubernetes/+milestone/1.17+ck2](https://launchpad.net/charmed-kubernetes/+milestone/1.17+ck2).

# 1.17+ck1 Bugfix release

### January 15, 2020 - [charmed-kubernetes-372](https://api.jujucharms.com/charmstore/v5/charmed-kubernetes-372/archive/bundle.yaml)

## Fixes

We fixed an issue where pod-to-pod network traffic was being unnecessarily
masqueraded when using Flannel or Canal. More details can be found at
[https://launchpad.net/charmed-kubernetes/+milestone/1.17+ck1](https://launchpad.net/charmed-kubernetes/+milestone/1.17+ck1).

# 1.17

### December 17, 2019 - [charmed-kubernetes-335](https://api.jujucharms.com/charmstore/v5/charmed-kubernetes-335/archive/bundle.yaml)

Before upgrading, please read the [upgrade notes](/kubernetes/docs/upgrade-notes).

## What's new

- CIS Benchmark

The **Center for Internet Security (CIS)** maintains a [Kubernetes benchmark][cis-benchmark]
that is helpful to ensure clusters are deployed in accordance with security best practices.
See the [CIS Compliance](/kubernetes/docs/cis-compliance) documentation for instructions on
how to run this compliance benchmark.

- Snap Coherence

Beginning with Charmed Kubernetes 1.17, updates to Kubernetes snap packages used by
`kubernetes-master` and `kubernetes-worker` charms will be applied in a controlled fashion. Known
as **Snap Coherence**, this feature ensures snap updates are first applied to individual master
units, followed by workers. If an update fails, the process is aborted before affecting the entire
cluster. This feature also allows snap revisions to be controlled by a snap store proxy. See
[snap coherence](/kubernetes/docs/snap-coherence) documentation for details.

- Nagios checks

Additional Nagios checks have been added for the `kubernetes-master` and `kubernetes-worker` charms.
These checks enhance the monitoring and reporting available via Nagios by collecting data on node
registration and API server connectivity.

- Improved metrics

`kube-state-metrics` is now added by default to the cluster when monitoring is enabled. New default
dashboards are also included to highlight these metrics with Prometheus/Grafana.

- Storage Classes created by default

Storage classes will now be created if the `kubernetes-master` charm is related to an
integrator charm. These classes are for AWS, GCE, Openstack, and Azure and are named cdk-ebs,
cdk-gce-pd, cdk-cinder, and cdk-azure-disk, respectively.

- Support for etcd 3.3 and 3.4

Whilst Charmed Kubernetes 1.17 ships with etcd 3.3 by default, it also brings support for
running etcd 3.4. To do so, you can simply run the followiung Juju command:

```bash
juju config etcd channel=3.4/stable
```

## Component Upgrades

Many of the components in Charmed Kubernetes 1.17 have been upgraded. The following list
highlights some of the more notable version changes:

- calico 3.10.1
- coredns 1.6.5
- etcd 3.3
- nfs-provisioner 3.1.0
- nginx-ingress-controller 0.26.1

## Fixes

A list of bug fixes and other minor feature updates in this release can be found at
[https://launchpad.net/charmed-kubernetes/+milestone/1.17](https://launchpad.net/charmed-kubernetes/+milestone/1.17).

## Notes / Known Issues

- The `registry` action for the `kubernetes-worker` charm has been deprecated and will be removed
in a future release. To enable a custom container registry, please see the
[registry](/kubernetes/docs/docker-registry) documentation.

# 1.16+ck2 Bugfix release

### November 22, 2019 - [charmed-kubernetes-316](https://api.jujucharms.com/charmstore/v5/bundle/charmed-kubernetes-316/archive/bundle.yaml)

## Fixes

A list of bug fixes and other minor feature updates in this release can be found at
[https://launchpad.net/charmed-kubernetes/+milestone/1.16+ck2](https://launchpad.net/charmed-kubernetes/+milestone/1.16+ck2).

# 1.16+ck1 Bugfix release

### October 4, 2019 - [charmed-kubernetes-270](https://api.jujucharms.com/charmstore/v5/bundle/charmed-kubernetes-270/archive/bundle.yaml)

## Fixes

A list of bug fixes and other minor feature updates in this release can be found at
[https://launchpad.net/charmed-kubernetes/+milestone/1.16+ck1](https://launchpad.net/charmed-kubernetes/+milestone/1.16+ck1).

# 1.16

### September 27, 2019 -  [charmed-kubernetes-252](https://api.jujucharms.com/charmstore/v5/charmed-kubernetes-252/archive/bundle.yaml)

Before upgrading, please read the [upgrade notes](/kubernetes/docs/upgrade-notes).

## What's new

- Kata Containers support

Beginning with Charmed Kubernetes 1.16, the [Kata Containers](https://katacontainers.io) runtime can be used
with containerd to safely run insecure or untrusted pods. When enabled, Kata provides hypervisor isolation
for pods that request it, while trusted pods can continue to run on a shared kernel via runc.
For details on using Kata Containers with Charmed Kubernetes, consult the [documentation](/kubernetes/docs/kata).

- AWS IAM support

Amazon AWS IAM authentication and authorisation is now supported via a subordinate charm. See
[AWS-IAM documentation](/kubernetes/docs/aws-iam-auth) for details on how to use AWS credentials
to log in to your Charmed Kubernetes cluster.

- SSL passthrough support

A new configuration parameter was added to the kubernetes-worker charm to enable ssl passthrough.
This allows TLS termination to happen on the workload. Refer to the
[upstream documentation](https://kubernetes.github.io/ingress-nginx/user-guide/tls/#ssl-passthrough)
for more information.

- Improved LXD support

LXD containers used for hosting Kubernetes components require some specific profile settings. These
profiles are now embedded in the charms themselves and applied when deployed, dramatically
simplifying the process of installing Charmed Kubernetes on a single machine. See the
[Local install documentation](/kubernetes/docs/install-local) for the updated instructions.

- Improved Prometheus/Grafana integration

The setup and configuration of Prometheus and Grafana has been significantly streamlined with
new relations to allow the charms to manage the scraper job and dashboards. This means that
monitoring can now be added by specifying a single overlay when deploying Charmed Kubernetes.
Refer to the [updated documentation](/kubernetes/docs/monitoring) for more information.

- Improved OpenStack integration

The OpenStack Integrator charm can now replace the Kube API Load Balancer by providing a
native OpenStack load balancer (Octavia or Neutron) to provide HA load balancing for the
Kubernetes control plane. Refer to the [updated documentation](/kubernetes/docs/openstack-integration)
for more information.

- Docker Registry with Containerd

The Docker registry charm can now be related directly to the Containerd runtime charm.
Refer to the [documentation](/kubernetes/docs/docker-registry) for instructions on how to deploy the charm.

- Renamed default container registry

The Canonical container image registry has a new, firewall-friendly name:
`image-registry.canonical.com:5000` is now `rocks.canonical.com`. The old URL
is an alias for `rocks` and will continue to work. However, the default
configuration for current charms has changed to the new URL.

## Fixes

A list of bug fixes and other minor feature updates in this release can be found at
[https://launchpad.net/charmed-kubernetes/+milestone/1.16](https://launchpad.net/charmed-kubernetes/+milestone/1.16).

Special thanks to [pierrop](https://github.com/pierrop) for contributing a fix to
[issue 1841965](https://bugs.launchpad.net/charm-kubernetes-master/+bug/1841965)!

## Known Issues

The Kubernetes Dashboard shipped with Charmed Kubernetes 1.16 is version 2.0.0-beta4. While unusual to ship a beta component with a stable release, in this case it was necessary, since the latest stable dashboard (v1.10.1) does not work with Kubernetes 1.16.

## Previous releases

Please see [this page][historic] for release notes of earlier versions.

<!--LINKS-->
[upgrade-notes]: /kubernetes/docs/upgrade-notes
[bundle]: https://api.jujucharms.com/charmstore/v5/canonical-kubernetes-471/archive/bundle.yaml
[historic]: /kubernetes/docs/release-notes-historic
[upgrading-docker]: /kubernetes/docs/upgrading#upgrading-docker
[tigera-home]: https://www.tigera.io/tigera-secure-ee/
[tigera-docs]: /kubernetes/docs/tigera-secure-ee
[haoverview]: /kubernetes/docs/high-availability
[metallb-docs]: /kubernetes/docs/metallb
[hacluster-docs]: /kubernetes/docs/hacluster
[cni-calico]: /kubernetes/docs/cni-calico
[containerd]: /kubernetes/docs/containerd
[container-runtime]: /kubernetes/docs/container-runtime
[cis-benchmark]: https://www.cisecurity.org/benchmark/kubernetes/
[heapster-deprecation]: https://github.com/kubernetes-retired/heapster/blob/master/docs/deprecation.md

<!-- FEEDBACK -->
<div class="p-notification--information">
  <p class="p-notification__response">
    We appreciate your feedback on the documentation. You can 
    <a href="https://github.com/charmed-kubernetes/kubernetes-docs/edit/master/pages/k8s/release-notes.md" class="p-notification__action">edit this page</a> 
    or 
    <a href="https://github.com/charmed-kubernetes/kubernetes-docs/issues/new" class="p-notification__action">file a bug here</a>.
  </p>
</div>
