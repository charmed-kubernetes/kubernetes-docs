---
wrapper_template: "base_docs.html"
markdown_includes:
  nav: "shared/_side-navigation.md"
context:
  title: "CNI with Calico"
  description: How to manage and deploy Kubernetes with Calico
keywords: CNI, networking
tags: [operating]
sidebar: k8smain-sidebar
permalink: cni-with-calico.html
layout: [base, ubuntu-com]
toc: False
---


<<Calico intro text>>


## Deploying **CDK** with Calico


## Calico configuration options


| Name                  |  Type     |  Default value | Description  |
|=============|=======|============|====================================|
| calico-policy-image  | string     | quay.io/calico/kube-controllers:v1.0.5     | The image id to use for calico/kube-controllers |
| calico-node-image  | string     | quay.io/calico/node:v2.6.12  |  The image id to use for calico/node |
|  ipip|   bool | False |  Enable IP tunnelling |
| nat-outgoing | bool  | True  | Enable NAT on outgoing traffic  |



## Checking the current configuration

## Changing the configuration


## Troubleshooting

If there is an issue with connectivity, it can be useful to inspect the Juju logs. To see a
complete set of logs for Calico

```bash
juju debug-log --replay --include=calico
```

For additional troubleshooting pointers, please see the [dedicated troubleshooting page][troubleshooting].



<!-- LINKS -->

[calico]:
[troubleshooting]: /kubernetes/docs/troubleshooting
[quickstart]:  /kubernetes/docs/quickstart
[install-manual]:  /kubernetes/docs/install-manual
