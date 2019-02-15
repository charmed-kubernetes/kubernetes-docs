---
wrapper_template: "base_docs.html"
markdown_includes:
  nav: "shared/_side-navigation.md"
context:
  title: "CDK on AWS"
  description: Running CDK on AWS using the aws-integrator.
keywords: aws, integrator, ebs, elb
tags: [install]
sidebar: k8smain-sidebar
permalink: using-aws.html
layout: [base, ubuntu-com]
toc: False
---

## AWS integrator

The `aws-integrator` charm simplifies working with **CDK** on AWS. Using the
credentials provided to Juju, it acts as a proxy between CDK and the underlying cloud,
granting permissions to dynamically create, for example EBS volumes.

### Installing

If you use the [recommended install method][quickstart] with `conjure-up`, the
integrator charm will be installed by default, and trust granted automatically.

If you install **CDK** using the Juju bundle, you can add the aws-integrator at
the same time by using the following overlay file
([download it here][asset-aws-overlay]):

```yaml
applications:
  aws-integrator:
    charm: cs:~containers/aws-integrator
    num_units: 1
relations:
  - ['aws-integrator', 'kubernetes-master']
  - ['aws-integrator', 'kubernetes-worker']
  ```

To use this overlay with the **CDK** bundle, it is specified during deploy like this:

```bash
juju deploy canonical-kubernetes  --overlay ~/path/aws-overlay.yaml
```

Then run the command to share credentials with this charm:

```bash
juju trust aws-integrator
```

... and remember to fetch the configuration file!

```bash
juju scp kubernetes-master/0:config ~/.kube/config
```

### Using EBS volumes

Many  pods you may wish to deploy will require storage. Although you can use any type
of storage supported by Kubernetes (see the [storage documentation][storage]), you
also have the option to use the native AWS storage, Elastic Block Store (EBS).

First we need to create a storage class which can be used by Kubernetes.  To start with,
we will create one for the 'General Purpose SSD' type of EBS storage:

```bash
```

You can confirm this has been added by running:

```bash
kubectl get sc
```

which should return:
```bash
NAME      PROVISIONER             AGE
ebs-gp2   kubernetes.io/aws-ebs   39s
```

You can create additional storage classes for the other types of EBS storage if
needed, simply give them a different name and replace the 'type: gp2' with a
different type (See the [AWS website][ebs-info] for more information on the
available types).

To actually create storage using this new class, you can make a Persistent Volume Claim:

```bash
kubectl create -f - <<EOY
kind: PersistentVolumeClaim
apiVersion: v1
metadata:
  name: testclaim
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 100Mi
  storageClassName: ebs-gp2
EOY
```

This should finish with a confirmation. You can check the cureent PVCs with:

```bash
kubectl get pvc
```

...which should return something similar to:

```bash
NAME        STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS   AGE
testclaim   Bound    pvc-54a94dfa-3128-11e9-9c54-028fdae42a8c   1Gi        RWO            ebs-gp2        9s
```

This PVC can then be used by pods operating in the cluster. As an example, the following
deploys a `busybox` pod:

```bash
kubectl create -f - <<EOY
apiVersion: v1
kind: Pod
metadata:
  name: busybox
  namespace: default
spec:
  containers:
    - image: busybox
      command:
        - sleep
        - "3600"
      imagePullPolicy: IfNotPresent
      name: busybox
      volumeMounts:
        - mountPath: "/pv"
          name: testvolume
  restartPolicy: Always
  volumes:
    - name: testvolume
      persistentVolumeClaim:
        claimName: testclaim
EOY
```

<div class="p-notification--caution">
  <p markdown="1" class="p-notification__response">
    <span class="p-notification__status">Note:</span>
If you create EBS volumes and subsequently tear down the cluster, make sure to check
with the AWS console to make sure all the associated resources have also been released.
  </p>
</div>

### Using ELB Loadbalancers

### Upgrading the integrator-charm

### Troubleshooting

<!-- LINKS -->

[ebs-info]: https://aws.amazon.com/ebs/features/
