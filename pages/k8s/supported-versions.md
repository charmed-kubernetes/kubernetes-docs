---
wrapper_template: "kubernetes/docs/base_docs.html"
markdown_includes:
  nav: "kubernetes/docs/shared/_side-navigation.md"
context:
  title: "Supported versions"
  description: The Charmed Kubernetes release cycle and current supported versions.
keywords: juju, upgrading, track, version
tags: [operating]
sidebar: k8smain-sidebar
permalink: supported-versions.html
layout: [base, ubuntu-com]
toc: False
---

Charmed Kubernetes officially supports the most recent three (3) minor releases
of Kubernetes.

Current Release: **1.19**

Supported releases: **1.19.x, 1.18.x, 1.17.x**

## Charmed Kubernetes bundle versions

The **Juju Charm Store** hosts the **Charmed Kubernetes** bundles as well as
individual charms. To deploy the latest, stable bundle, run the command:

```bash
juju deploy charmed-kubernetes
```

It is also possible to deploy a specific version of the bundle by including the
revision number. For example, to deploy the **Charmed Kubernetes** bundle for the Kubernetes 1.14
release, you could run:

```bash
juju deploy cs:~containers/charmed-kubernetes-124
```

<div class="p-notification--positive">
  <p markdown="1" class="p-notification__response">
    <span class="p-notification__status">Older Versions:</span>
Previous versions of <strong>Charmed Kubernetes</strong> used the name
<code>canonical-kubernetes</code>. These versions are still available under that name
and links in the charm store. Versions from 1.14 onwards will use
<code>charmed-kubernetes</code>.
  </p>
</div>


The revision numbers for bundles are generated automatically when the bundle is
updated, including for testing and beta versions, so it isn't always the case
that a higher revision number is 'better'. The revision numbers for the release
versions of the **Charmed Kubernetes** bundle are shown in the table below:

<a  id="table"></a>

| Kubernetes version | Charmed Kubernetes bundle |
| --- | --- |
| 1.19.x         | [charmed-kubernetes-519](https://api.jujucharms.com/charmstore/v5/charmed-kubernetes-509/archive/bundle.yaml) |
| 1.18.x         | [charmed-kubernetes-485](https://api.jujucharms.com/charmstore/v5/charmed-kubernetes-485/archive/bundle.yaml) |
| 1.17.x         | [charmed-kubernetes-410](https://api.jujucharms.com/charmstore/v5/charmed-kubernetes-410/archive/bundle.yaml) |
| 1.16.x         | [charmed-kubernetes-316](https://api.jujucharms.com/charmstore/v5/charmed-kubernetes-316/archive/bundle.yaml) |
| 1.15.x         | [charmed-kubernetes-209](https://api.jujucharms.com/charmstore/v5/charmed-kubernetes-209/archive/bundle.yaml) |
| 1.14.x         | [charmed-kubernetes-124](https://api.jujucharms.com/charmstore/v5/charmed-kubernetes-124/archive/bundle.yaml) |
| 1.13.x         | [canonical-kubernetes-435](https://api.jujucharms.com/charmstore/v5/~containers/bundle/canonical-kubernetes-435/archive/bundle.yaml?channel=stable) |
| 1.12.x         | [canonical-kubernetes-357](https://api.jujucharms.com/charmstore/v5/~containers/bundle/canonical-kubernetes-357/archive/bundle.yaml?channel=stable) |
| 1.11.x         | [canonical-kubernetes-254](https://api.jujucharms.com/charmstore/v5/~containers/bundle/canonical-kubernetes-254/archive/bundle.yaml?channel=stable) |
| 1.10.x         | [canonical-kubernetes-211](https://api.jujucharms.com/charmstore/v5/~containers/bundle/canonical-kubernetes-211/archive/bundle.yaml?channel=stable)  |
| 1.9.x        | [canonical-kubernetes-179](https://api.jujucharms.com/charmstore/v5/~containers/bundle/canonical-kubernetes-179/archive/bundle.yaml?channel=stable) |
| 1.8.x | [canonical-kubernetes-132](https://api.jujucharms.com/charmstore/v5/~containers/bundle/canonical-kubernetes-132/archive/bundle.yaml?channel=stable) |
| 1.7.x | [canonical-kubernetes-101](https://api.jujucharms.com/charmstore/v5/~containers/bundle/canonical-kubernetes-101/archive/bundle.yaml?channel=stable) |
| 1.6.x | [canonical-kubernetes-38](https://api.jujucharms.com/charmstore/v5/~containers/bundle/canonical-kubernetes-38/archive/bundle.yaml?channel=stable) |

<div class="p-notification--caution">
  <p markdown="1" class="p-notification__response">
    <span class="p-notification__status">Note:</span>
Only the latest three versions of Charmed Kubernetes are supported at any time.
  </p>
</div>


## Finding version info

To check which versions of Kubernetes are available, use the `snap info` command:

```bash
snap info kube-apiserver
```

Keep in mind that although snap info enumerates all available versions, only
the latest three stable versions are officially supported:

```no-highlight
name:      kube-apiserver
summary:   Kubernetes master component that exposes the Kubernetes API.
publisher: Canonical✓
contact:   https://www.ubuntu.com/kubernetes
license:   Apache-2.0
description: |
  Kube-apiserver is the front-end for the Kubernetes control plane. It validates and configures data
  for the api objects which include pods, services, replicationcontrollers, and others. The API
  Server services REST operations and provides the frontend to the cluster’s shared state through
  which all other components interact.

  For more information, consult the [reference
  documentation](https://kubernetes.io/docs/reference/command-line-tools-reference/kube-apiserver/).
snap-id: KMZLusdClmUyLXAjjcI4sVnpjk1kM653
channels:
  stable:         1.17.0         2019-12-17 (1493) 22MB -
  candidate:      1.17.0         2019-12-17 (1493) 22MB -
  beta:           1.17.0         2019-12-17 (1493) 22MB -
  edge:           1.17.0         2019-12-17 (1493) 22MB -
  1.18/stable:    –
  1.18/candidate: –
  1.18/beta:      –
  1.18/edge:      1.18.0-alpha.1 2019-12-18 (1512) 22MB -
  1.17/stable:    1.17.0         2019-12-10 (1493) 22MB -
  1.17/candidate: 1.17.0         2019-12-10 (1493) 22MB -
  1.17/beta:      1.17.0         2019-12-10 (1493) 22MB -
  1.17/edge:      1.17.0         2019-12-10 (1493) 22MB -
  1.16/stable:    1.16.4         2019-12-16 (1501) 25MB -
  1.16/candidate: 1.16.4         2019-12-16 (1501) 25MB -
  1.16/beta:      1.16.4         2019-12-16 (1501) 25MB -
  1.16/edge:      1.16.4         2019-12-16 (1501) 25MB -
  1.15/stable:    1.15.7         2019-12-16 (1500) 24MB -
  1.15/candidate: 1.15.7         2019-12-16 (1500) 24MB -
  1.15/beta:      1.15.7         2019-12-16 (1500) 24MB -
  1.15/edge:      1.15.7         2019-12-16 (1500) 24MB -
  1.14/stable:    1.14.10        2019-12-16 (1505) 24MB -
  1.14/candidate: 1.14.10        2019-12-16 (1505) 24MB -
  1.14/beta:      1.14.10        2019-12-16 (1505) 24MB -
  1.14/edge:      1.14.10        2019-12-16 (1505) 24MB -
  1.13/stable:    1.13.12        2019-10-17 (1434) 23MB -
  1.13/candidate: 1.13.12        2019-10-17 (1434) 23MB -
  1.13/beta:      1.13.12        2019-10-17 (1434) 23MB -
  1.13/edge:      1.13.13-beta.0 2019-10-16 (1371) 23MB -
  1.12/stable:    1.12.9         2019-06-05 (1004) 27MB -
  1.12/candidate: 1.12.9         2019-05-29 (1004) 27MB -
  1.12/beta:      1.12.9         2019-05-29 (1004) 27MB -
  1.12/edge:      1.12.9         2019-05-29 (1004) 27MB -
  1.11/stable:    1.11.9         2019-03-29  (866) 26MB -
  1.11/candidate: 1.11.9         2019-03-26  (866) 26MB -
  1.11/beta:      1.11.9         2019-03-26  (866) 26MB -
  1.11/edge:      1.11.9         2019-03-26  (866) 26MB -
  1.10/stable:    1.10.13        2019-02-27  (744) 25MB -
  1.10/candidate: 1.10.13        2019-03-21  (838) 25MB -
  1.10/beta:      1.10.13        2019-03-21  (838) 25MB -
  1.10/edge:      1.10.13        2019-03-21  (838) 25MB -
  1.9/stable:     1.9.11         2018-10-08  (454) 24MB -
  1.9/candidate:  1.9.11         2018-10-17  (466) 24MB -
  1.9/beta:       1.9.11         2018-10-17  (466) 24MB -
  1.9/edge:       1.9.11         2018-10-17  (466) 24MB -
  1.8/stable:     1.8.15         2018-07-11  (435) 23MB -
  1.8/candidate:  1.8.15         2018-10-17  (465) 23MB -
  1.8/beta:       1.8.15         2018-10-17  (465) 23MB -
  1.8/edge:       1.8.15         2018-10-17  (465) 23MB -
  1.7/stable:     1.7.16         2018-06-06  (395) 24MB -
  1.7/candidate:  1.7.16         2018-10-17  (464) 24MB -
  1.7/beta:       1.7.16         2018-10-17  (464) 24MB -
  1.7/edge:       1.7.16         2018-10-17  (464) 24MB -
  1.6/stable:     1.6.13         2017-11-30  (233) 21MB -
  1.6/candidate:  1.6.13         2018-10-17  (463) 21MB -
  1.6/beta:       1.6.13         2018-10-17  (463) 21MB -
  1.6/edge:       1.6.13         2018-10-17  (463) 21MB -
  1.5/stable:     1.5.5          2017-05-17    (3) 17MB -
  1.5/candidate:  1.5.5          2017-05-17    (3) 17MB -
  1.5/beta:       1.5.5          2017-05-17    (3) 17MB -
  1.5/edge:       1.5.5          2017-05-17    (3) 17MB
  ```

In the above output, the stable release is identified as 1.17, and so 1.16 and
1.15 are also currently supported.

## Professional support

If you are looking for additional support, find out about [Ubuntu Advantage][support].

Canonical can also provide [managed solutions][managed] for Kubernetes.

<!-- FEEDBACK -->
<div class="p-notification--information">
  <p class="p-notification__response">
    We appreciate your feedback on the documentation. You can
    <a href="https://github.com/charmed-kubernetes/kubernetes-docs/edit/master/pages/k8s/supported-versions.md" class="p-notification__action">edit this page</a>
    or
    <a href="https://github.com/charmed-kubernetes/kubernetes-docs/issues/new" class="p-notification__action">file a bug here</a>.
  </p>
</div>

<!-- LINKS -->

[support]: /support
[managed]: /kubernetes/managed
