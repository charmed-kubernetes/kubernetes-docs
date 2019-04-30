---
wrapper_template: "base_docs.html"
markdown_includes:
  nav: "shared/_side-navigation.md"
context:
  title: "CNI with flannel"
  description: How to manage and deploy Kubernetes with flannel
keywords: CNI, networking
tags: [operating]
sidebar: k8smain-sidebar
permalink: cni-with-flannel.html
layout: [base, ubuntu-com]
toc: False
---


Flannel intro


## Deploying **CDK** with flannel

Flannel is the default choice for networking with **CDK**. If you
[install using `conjure-up`][quickstart], or by
[manually deploying the bundle][install-manual] without changing the default settings,
flannel will be used for CNI.

## Flannel options


| Name                  |  Type     |  Default value | Description  |
|=============|=======|============|====================================|
| cidr                       | string     | 10.1.0.0/16      | Network CIDR to assign to Flannel  |
| iface                      | string     | see description>  |  The interface to bind flannel overlay networking. The default value is the interface bound to the CNI endpoint. |
|  nagios_context |  string |  juju  |  A string that will be prepended to instance name to set the host name in nagios.If you're running multiple environments with the same services in them this allows you to differentiate between them. Used by the nrpe subordinate charm. |
| nagios_servicegroups | string  | (empty)  | A comma-separated list of nagios servicegroups. If left empty, the nagios_context will be used as the servicegroup  |

## Troubleshooting

If there is an issue with connectivity, it can be useful to inspect the Juju logs. To see a
complete set of logs for flannel

```bash
juju debug-log --replay --include=flannel
```

For additional troubleshooting pointers, please see the [dedicated troubleshooting page][troubleshooting].



<!-- LINKS -->

[flannel]: https://github.com/coreos/flannel/
[troubleshooting]: /kubernetes/docs/troubleshooting
[quickstart]:  /kubernetes/docs/quickstart
[install-manual]:  /kubernetes/docs/install-manual
