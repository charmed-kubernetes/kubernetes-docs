---
wrapper_template: "templates/docs/markdown.html"
markdown_includes:
  nav: "kubernetes/docs/shared/_side-navigation.md"
context:
  title: "NVidia DGX"
  description: DGX certified Kubernetes.
keywords: gpu, nvidia, dgx
tags: [operating]
sidebar: k8smain-sidebar
permalink: nvidia-dgx.html
layout: [base, ubuntu-com]
toc: False
---

Charmed Kubernetes is a certified [DGX-Ready][dgx] Kubernetes.

There is no special installation step or enablement for running
Charmed Kubernetes on DGX hardware - it will automatically be
detected and the correct drivers loaded when deployed. 

## Verify the installation

A simple test job can be created to run NVIDIA's hardware reporting tool.
Please note that you may need to replace the image tag in the following
YAML with [the latest supported one][nvidia-supported-tags].

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
      - image: nvidia/cuda:11.6.0-base-ubuntu20.04
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

You can inspect the logs to find the hardware report.

```bash
kubectl logs job.batch/nvidia-smi

Thu Mar  3 14:52:26 2022       
+-----------------------------------------------------------------------------+
| NVIDIA-SMI 510.47.03    Driver Version: 510.47.03    CUDA Version: 11.6     |
|-------------------------------+----------------------+----------------------+
| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
|                               |                      |               MIG M. |
|===============================+======================+======================|
|   0  Tesla V100-SXM2...  On   | 00000000:00:1E.0 Off |                    0 |
| N/A   39C    P0    24W / 300W |      0MiB / 16384MiB |      0%      Default |
|                               |                      |                  N/A |
+-------------------------------+----------------------+----------------------+
                                                                               
+-----------------------------------------------------------------------------+
| Processes:                                                                  |
|  GPU   GI   CI        PID   Type   Process name                  GPU Memory |
|        ID   ID                                                   Usage      |
|=============================================================================|
|  No running processes found                                                 |
+-----------------------------------------------------------------------------+
```

[asset-nvidia]: https://raw.githubusercontent.com/charmed-kubernetes/kubernetes-docs/main/assets/nvidia-test.yaml
[dgx-ready]: https://www.nvidia.com/en-gb/data-center/dgx-ready-software/