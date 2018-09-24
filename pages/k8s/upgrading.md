---
title: "Upgrading | Canonical Distribution of Kubernetes&reg;"
keywords: juju, upgrading, track, version
tags: [operating]
sidebar: k8smain-sidebar
permalink: upgrading.html
layout: base
toc: False
summary: This page is currently a work in progress. For existing documentation, please visit <a href="https://kubernetes.io/docs/getting-started-guides/ubuntu/"> https://kubernetes.io/docs/getting-started-guides/ubuntu/ </a>
---

# Upgrading

It is recommended that you keep your Kubernetes deployment updated to the
latest available stable version. You should also update the other applications
which make up the **Canonical Distribution of Kubernetes<sup>&reg;</sup>.**
Keeping up to date makes sure you have the latest bug-fixes and security
patches for smooth operation of your cluster.

There is no set cadence to the releases of **Kubernetes**,  but you can check
the latest release version on the  
[Kubernetes release page on GitHub][k8s-release].  The **CDK** is kept in close sync
with upstream Kubernetes.

!!! Note: Kubernetes will automatically handle patch releases. This means that the cluster will perform an unattended automatic upgrade between patch versions, e.g. 1.10.7 -> 1.10.8. Attended upgrades are only required when you wish to upgrade a minor version, e.g. 1.9.x to 1.10.x.

You can see which version of each application is currently deployed by running

```bash
juju status
```

The 'App' section of the ouput lists each application and its version number.
Note that this is the version of the upstream application deployed. The version
of the Juju charm is indicated under the column titled 'Rev'. The charms may be
updated in between new versions of the application.

## Before you begin

As with all upgrades, there is a possibility that there may be unforeseen
difficulties. It is **highly recommended that you make a backup** of any
important data, including any running workloads. For more details on creating
backups, see the separate [documentation on backups][backups].

You should also make sure:

  * The machine from which you will perform the backup has sufficient internet access to
      retrieve updated software
  * Your cluster is running normally
  * You read the [Upgrade notes][notes] to see if any caveats apply to the versions you are
     upgrading to/from
  * You read the [Release notes][release-notes] for the version you are upgrading to,
      which will alert you to any important changes to the operation of your cluster

## Infrastructure updates

The applications which run alongside the core Kubernetes components can be
upgraded at any time. These applications are widely used and may frequently
receive upgrades outside of the cycle of new releases of Kubernetes.

This includes:

 - easyrsa  
 - etcd                
 - flannel

 Note that this may include other applications which you may have installed, such as
 Elasticsearch, Prometheus, Nagios, Helm, etc.

### Upgrading **etcd**

 As **etcd** manages critical data for the cluster, it is advisable to create a snapshot of
 this data before running an upgrade. This is covered in more detail in the  
 [documentation on backups][backups], but the basic steps are:

  * **Run the snapshot action on the charm:**
     ```bash
     juju run-action etcd/0 snapshot --wait
     ```
     You should see confirmation of the snapshot being created, and the location of the
     file _on the **etcd** unit_
 * **Fetch a local copy of the snapshot**
    Knowing the path to the snapshot file from the output of the above command, you can
    download a local copy:
    ```bash
    juju scp etcd/0:/home/ubuntu/etcd-snapshots/<filename>.tar.gz .
    ```
You can now upgrade **etcd**:

```bash
juju upgrade-charm etcd
```

### Upgrading additional components

The other infrastructure applications can be upgraded by running the `upgrade-charm` command:

```bash
juju upgrade-charm flannel
juju upgrade-charm easyrsa
```
Any other infrastructure charms can be upgraded in a similar way.

## Upgrading Kubernetes

Before you upgrade the **Kubernetes** components, you should be aware of the
exact release you wish to upgrade to.

The Kubernetes charms use **snap**  _channels_ to manage the version of
Kubernetes to use.  Channels are explained in more detail in the  [official
snap documentatio][snap-channels], but in terms of Kubernetes all you need to
know are the major and minor version numbers and the 'risk-level':

| Risk level |   Description                                                                                       |
|----------------|---------------------------------------------------------------------------------------|
|stable	        | The latest stable released version of Kubernetes                 |
|candidate  |	Release candidate versions of Kubernetes                              |
|beta	           | Latest alpha/beta of Kubernetes for the specified release|
|edge	          | Nightly builds of the specified release of Kubernetes          |

### Upgrading the **kube-api-loadbalancer**

A core part of **CDK** is the kubeapi-load-balancer component. A mismatch of versions
could have an effect on API availability and access controls. To ensure API service
continuity this upgrade should preceed any upgrades to the **Kubernetes** master
and worker units.

```bash
juju upgrade-charm kubeapi-load-balancer
```

### Upgrading the Kubernetes master units

### Upgrading the Kubernetes worker units

 <!--LINKS-->

 [k8s-release]: https://github.com/kubernetes/kubernetes/releases
 [backups]: ./backups.html
 [notes]: ./upgrade-notes.html
 [snap-channels]: https://docs.snapcraft.io/reference/channels
