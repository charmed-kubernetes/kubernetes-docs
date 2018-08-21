---
title: "Ceph and CDK | Canonical Distribution of Kubernetes&reg;"
keywords: quickstart
tags: [getting_started]
sidebar: k8smain-sidebar
permalink: ceph.html
layout: base
toc: False
summary: How to get Ceph deployed and related to Kubernetes in order to have a default storage class. This allows for easy storage allocation.
---
## What you'll need

  * A CDK environment set up and running. See the quickstart in order to get this going.
  * An existing Ceph cluster or the ability to create one.

## Installing Ceph

Note: If you have a working juju-based Ceph cluster, you can skip this section.

Installing Ceph is easy with Juju. Just deploy the monitor charms and some storage(osd) charms and related them.

```bash
$ juju deploy -n 3 ceph-mon
$ juju deploy -n 3 cs:ceph-osd --storage osd-devices=ebs,32G,2 --storage osd-journals=ebs,8G,1
```

In this example, we are installing to AWS, using 3 machines for the Ceph monitor, using 3 machines
for the storage(osd), creating 2 32 gig storage devices per osd machine, and 1 8 gig journal device
per osd machine. This means overall this cluster with have 192 gigs of storage and 24 gigs of journal
space.

## Relating to CDK

Making CDK aware of your Ceph cluster is an easy process that just involves a juju relation.

```bash
$ juju relate ceph-mon kubernetes-master
```

Note that the Ceph CSI containers require privileged access:

```bash
$ juju config kubernetes-master allow-privileged=true
```

And finally, you need the pools that are defined in the storage class:

```bash
$ juju run-action ceph-mon/0 create-pool name=xfs-pool --wait
unit-ceph-mon-0:
  id: c12f0688-f31b-4956-8314-abacd2d6516f
  status: completed
  timing:
    completed: 2018-08-20 20:49:34 +0000 UTC
    enqueued: 2018-08-20 20:49:31 +0000 UTC
    started: 2018-08-20 20:49:31 +0000 UTC
  unit: ceph-mon/0
$ juju run-action ceph-mon/0 create-pool name=ext4-pool --wait
unit-ceph-mon-0:
  id: 4e82d93d-546f-441c-89e1-d36152c082f2
  status: completed
  timing:
    completed: 2018-08-20 20:49:45 +0000 UTC
    enqueued: 2018-08-20 20:49:41 +0000 UTC
    started: 2018-08-20 20:49:43 +0000 UTC
  unit: ceph-mon/0
```

## Verifying things are working

Now you can look at the CDK related pieces to verify things are working well:

```bash
kubectl get sc,po
NAME                                             PROVISIONER     AGE
storageclass.storage.k8s.io/ceph-ext4            csi-rbdplugin    7m
storageclass.storage.k8s.io/ceph-xfs (default)   csi-rbdplugin    7m

NAME                                                   READY     STATUS    RESTARTS   AGE
pod/csi-rbdplugin-attacher-0                           1/1       Running   0          7m
pod/csi-rbdplugin-cnh9k                                2/2       Running   0          7m
pod/csi-rbdplugin-lr66m                                2/2       Running   0          7m
pod/csi-rbdplugin-mnn94                                2/2       Running   0          7m
pod/csi-rbdplugin-provisioner-0                        1/1       Running   0          7m
```

And then install a helm chart if you have helm installed and verify the persistent volume is automatically created for you.

```bash
$ helm install stable/phpbb
$ kubectl get pvc
NAME                            STATUS    VOLUME                 CAPACITY   ACCESS MODES   STORAGECLASS   AGE
calling-wombat-phpbb-apache     Bound     pvc-b1d04079a4bd11e8   1Gi        RWO            ceph-xfs       34s
calling-wombat-phpbb-phpbb      Bound     pvc-b1d1131da4bd11e8   8Gi        RWO            ceph-xfs       34s
data-calling-wombat-mariadb-0   Bound     pvc-b1df7ac9a4bd11e8   8Gi        RWO            ceph-xfs       34s
```

## Conclusion

Now you have a Ceph cluster talking to your Kubernetes cluster. From here
you can install any of the things that require storage out of the box.