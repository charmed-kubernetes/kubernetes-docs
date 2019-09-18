---
wrapper_template: "kubernetes/docs/base_docs.html"
markdown_includes:
  nav: "kubernetes/docs/shared/_side-navigation.md"
context:
  title: "Using GPU workers"
  description: How to run workloads with GPU support.
keywords: gpu, nvidia, cuda
tags: [operating]
sidebar: k8smain-sidebar
permalink: gpu-workers.html
layout: [base, ubuntu-com]
toc: False
---

**Charmed Kubernetes** supports GPU-enabled
instances for applications which can use them. The kubernetes-worker charm will
automatically detect NVIDIA hardware and enable the appropriate support.
However, the implementation of GPU-enabled instances differs greatly between
public clouds. This page outlines the recommended methods for running GPU
enabled hardware for different public clouds.

### Deploying Charmed Kubernetes with GPU workers on AWS

If you are installing Charmed Kubernetes using a bundle, you can use constraints to specify
that the worker units are deployed on GPU-enabled machines. Because GPU support
varies considerably depending on the underlying cloud, this requires specifying
a particular instance type.

This can be done with a YAML overlay file. For example, when deploying Charmed
Kubernetes on AWS, you may decide you wish to use AWS's 'p2.xlarge' instances
(you can check the AWS instance definitions on the
[AWS website][aws-instance]). A YAML overlay file can be constructed like this:

```yaml
#gpu-overlay.yaml
applications:
  kubernetes-worker:
    constraints: instance-type=p2.xlarge
```

And then deployed with Charmed Kubernetes like this:

```bash
juju deploy charmed-kubernetes --overlay ~/path/aws-overlay.yaml --overlay ~/path/gpu-overlay.yaml
```

As demonstrated here, you can use multiple overlay files when deploying, so you
can combine GPU support with an integrator charm or other custom configuration.

You may then want to [test a GPU workload](#test)

### Adding GPU workers with AWS

It isn't necessary for all the worker units to have GPU support. You can simply
add GPU-enabled workers to a running cluster. The recommended way to do this is
to first create a new constraint for the kubernetes-worker:

```bash
juju set-constraints kubernetes-worker instance-type=p2.xlarge
```

Then you can add as many new worker units as required. For example, to add two
new units.

```bash
juju add-unit kubernetes-worker -n2
```

### Adding GPU workers with GCP

Google supports GPUs slightly differently to most clouds. There are no GPUs
included in any of the default instance templates, and therefore they have
to be added manually.

To begin, add a new machine with Juju. Include any desired constraints for
memory,cores,etc :

```bash
juju add-machine --constraints cores=2
```

The command will return, telling you the number of the machine that was
created - keep a note of this number.

Next you will need to use the gcloud tool or the GCP console to stop the
instance, edit its configuration and then restart the machine.

Once it is up and running, you can then add it as a worker:

```bash
juju add-unit kubernetes-worker --to 10
```

...replacing '10' in the above with the number of the machine you created.

As the charm installs, the GPU will be detected and the relevant drivers will
also be installed.
<a  id="test"> </a>

## Testing

As GPU instances can be costly, it is useful to test that they can actually be
used. A simple test job can be created to run NVIDIA's hardware reporting tool.

This can also be [downloaded here][asset-nvidia].

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: nvidia-smi
spec:
  template:
    metadata:
      name: nvidia-smi
    spec:
      restartPolicy: Never
      containers:
      - image: nvidia/cuda
        name: nvidia-smi
        args:
          - nvidia-smi
        resources:
          limits:
            nvidia.com/gpu: 1
          requests:
            nvidia.com/gpu: 1
        volumeMounts:
        - mountPath: /usr/bin/
          name: binaries
        - mountPath: /usr/lib/x86_64-linux-gnu
          name: libraries
      volumes:
      - name: binaries
        hostPath:
          path: /usr/bin/
      - name: libraries
        hostPath:
          path: /usr/lib/x86_64-linux-gnu

```

Download the file and run it with:

```bash
kubectl create -f nvidia-test.yaml
```

If you then check the Kubernetes dashboard, you can inspect the logs to
find the hardware report.

![dashboard image][img-log]


<!-- IMAGES -->

[img-log]: https://assets.ubuntu.com/v1/2ba88cee-nvidia.png


<!-- LINKS -->
[asset-nvidia]: https://raw.githubusercontent.com/juju-solutions/kubernetes-docs/master/assets/nvidia-test.yaml
[quickstart]: /kubernetes/docs/quickstart
[aws-instance]: https://aws.amazon.com/ec2/instance-types/
[azure-instance]: https://docs.microsoft.com/en-us/azure/virtual-machines/windows/sizes-gpu
