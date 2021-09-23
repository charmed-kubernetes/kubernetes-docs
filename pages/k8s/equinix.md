---
wrapper_template: "templates/docs/markdown.html"
markdown_includes:
  nav: "kubernetes/docs/shared/_side-navigation.md"
context:
  title: "Charmed Kubernetes on Equinix Metal"
  description: Running Charmed Kubernetes on Equinix.
keywords: equinix, integrator, ebs, elb
tags: [install]
sidebar: k8smain-sidebar
permalink: equinix.html
layout: [base, ubuntu-com]
toc: False
---

As with any cloud supported by Juju, **Charmed Kubernetes** can be deployed and used on
[Equinix Metal][]. This document provides some extra information and an overlay to 
help get the most out of this cloud


## Before installing

Equinix Metal has been added to the clouds Juju automatically knows about. To check, you can
run the command:

```bash
juju list-clouds --all
```

If `equinix` does not appear in the list, your local Juju install probably just needs to 
refresh its list of clouds. Run:

```bash
juju update-public-clouds
```

You should also add your credentials for this cloud. Use the interactive command:

```bash
juju add-credential equinix
```

...and follow the prompts to enter the information required (including the project id, and 
your auth token).



## Installing

If you install **Charmed Kubernetes** [using the Juju bundle][install], xxxxxxxxxxxx xxxx
 using the following overlay file 
 ([download it here][asset-equinix-overlay]):

```yaml





  ```

To use this overlay with the **Charmed Kubernetes** bundle, it is specified during deploy like this:

```bash
juju deploy charmed-kubernetes  --overlay ~/path/equinix-overlay.yaml --trust
```

... and remember to fetch the configuration file!

```bash
juju scp kubernetes-master/0:config ~/.kube/config
```

For more configuration options and details of the permissions which the integrator uses,
please see the [charm readme][aws-integrator-readme].

## Post install

To use Kubernetes on Equinix Metal, you should now set up the [Equinix Cloud Controller Manager][].

While the deployment is in progress no pods will be able to spun up on the Kubernetes due to 
taints being set on each node. The taints will be removed once the Cloud Controller Manager (CCM) 
is enabled and the nodes are registered with the cloud control plane.

First, a Kubernetes secret has to be created, defining the variables for the CCM:

```bash
kubectl create -f - <<EOY
apiVersion: v1
kind: Secret
metadata:
  name: metal-cloud-config
  namespace: kube-system
stringData:
  cloud-sa.json: |
    {
    "apiKey": "<Metal API key>",
    "projectID": "<Metal Project ID>",
    “loadbalancer”: “kube-vip://”
    }
EOY
```




```bash
curl  http://ad5fc7750350611e99768068a686bb67-239702253.eu-west-1.elb.amazonaws.com:8080
```
```
Hello Kubernetes!
```

<div class="p-notification--caution">
  <p markdown="1" class="p-notification__response">
    <span class="p-notification__status">Note:</span>
xxxxxxxxxxxxxxxxxxxxxxxx xxxxxxxxxxxxxxx x x x x x x x x x xxxxxxxxxxxxxxxxx
  </p>
</div>


### Troubleshooting

If you have any specific problems with the aws-integrator, you can report bugs on
[Launchpad][bugs].


```

## See also:

If you are an AWS user, you may also be interested in how to
[use AWS IAM for authorisation and authentication][aws-iam].

<!-- LINKS -->

[asset-equinix-overlay]: 
[quickstart]: /kubernetes/docs/quickstart
[storage]: /kubernetes/docs/storage
[ebs-info]: https://aws.amazon.com/ebs/features/
[cloudtrail]: https://console.aws.amazon.com/cloudtrail/
[bugs]: https://bugs.launchpad.net/charmed-kubernetes
[aws-integrator-readme]: https://charmhub.io/containers-aws-integrator
[aws-iam]: /kubernetes/docs/aws-iam-auth
[install]: /kubernetes/docs/install-manual
[Equinix Cloud Controller Manager]: https://github.com/equinix/cloud-provider-equinix-metal/

<!-- FEEDBACK -->
<div class="p-notification--information">
  <p class="p-notification__response">
    We appreciate your feedback on the documentation. You can
    <a href="https://github.com/charmed-kubernetes/kubernetes-docs/edit/master/pages/k8s/equinix.md" class="p-notification__action">edit this page</a>
    or
    <a href="https://github.com/charmed-kubernetes/kubernetes-docs/issues/new" class="p-notification__action">file a bug here</a>.
  </p>
</div>
