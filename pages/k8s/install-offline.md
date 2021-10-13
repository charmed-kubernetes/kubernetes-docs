---
wrapper_template: "templates/docs/markdown.html"
markdown_includes:
  nav: "kubernetes/docs/shared/_side-navigation.md"
context:
  title: "Installing Charmed Kubernetes offline"
  description: How to install Charmed Kubernetes in a restricted network
keywords: lxd, requirements, developer
tags: [install]
sidebar: k8smain-sidebar
permalink: install-offline.html
layout: [base, ubuntu-com]
toc: False
---

There are many reasons why it may be desirable to install Charmed Kubernetes
on a system which does not have unfettered access to the internet. To make
this possible, it is necessary to prepare the required resources, and configure
Charmed Kubernetes to make use of them.
As user needs may vary, this documentation does not present a proscriptive 
recipe, but outlines the types of resources which are required and some 
recommendations on how to provide them. If you are already installing 
services in a restricted environment you may already have some 'air-gap'
resources available, and may only need to configure Charmed Kubernetes to
make use of them.


## Apt package repository

Access to a repository is required for installing software which is not yet available 
as snap packages, as well as receiving updates for the underlying operating system. 
In normal use this requires network access to  `http://archive.ubuntu.com/` or one
of its localised mirrors.
In order to access the package package repository, it is common to set up a local 
mirror (for offline) or allow traffic through a proxy to the main archive.

There are many ways of setting up a local mirror. The repository is essentially just
a directory of files and some means of serving them (http, ftp, etc). It is common to
use tools such as [rsync][] or [apt-mirror][] to create the mirror. For greater 
control over the local archive, [aptly][] is also a good option.

If a proxy is already in use for the APT repository, it can be configured
according to the instructions under the heading 
[Configuring Charmed Kubernetes to work with proxies][]

### Series and architectures

Note that the mirror should contain packages for the required series (e.g. focal 
(Ubuntu 20.04), bionic) and architectures (e.g. `amd64`, `i386`) you expect to be using
in your deployment. The core Charmed Kubernetes components all use the `focal` series,
but some additional charms may be based on other series.

### Documentation for setting up a mirror

<!-- Links to tutorials for setting up mirrors - preferably ubuntu server docs? !-->

 * 
 * 
 * 

<!-- we should add tutorials for ones which don't exist !-->

## Snap packages

The majority of charms, including all of the core Charmed Kubernetes charms, rely on
[snap][] packages to deliver applications. Snaps are packages for desktop, cloud and
IoT that are easy to install, secure, cross‐platform and dependency‐free.

While it is _possible_ to download a snap package from the store, each snap will then
need to be authenticated, and subsequent updates, even in the case of security
updates, will require manual intervention. The recommended solution is to install and
configure a custom snap proxy.

### Documentation for setting up a snap proxy

<!-- 
Need to run through this and update the source docs if required
!-->

## Container images

<!-- Link to the list of required images. Perhaps there should be a script for
fetching these? !-->


## Juju 

<!-- Notes and links to Juju accessing OS images e.g. for MAAS, LXD etc
These shouldn't be documented here as they are cloud specific, but we should
point to the relevant docs !-->

## Bundle and charms
<!--
Fetching bundle - should we get it directly from git since Charmhub doesn't list it?

fetching individual charms - perhaps a script

Notes about charm upgrades/updates
!-->

## Configuring Charmed Kubernetes to work with proxies



## Additional considerations

### Python packages and PyPI

### LXD images
<!-- Even if deploying to a different cloud, LXD image access may still be required
e.g. when deploying to LXD containers as part of Kubernetes Core bundle !-->

### Ubuntu SSO
<!-- Not needed for CK, but needed on the snap store proxy... !-->

## Useful links


<!-- IMAGES -->



<!-- LINKS -->

[snap]: https://snapcraft.io
[rsync]:
[apt-mirror]:
[juju-docs]: https://juju.is/docs/olm/installing-juju
[controller-config]: https://juju.is/docs/olm/create-controllers
[credentials]: https://juju.is/docs/olm/credentials
[quickstart]: /kubernetes/docs/quickstart
[juju-bundle]: https://juju.is/docs/sdk/bundles
[juju-gui]: https://juju.is/docs/olm/accessing-juju%E2%80%99s-web-interface
[juju-constraints]: https://juju.is/docs/olm/constraints
[snaps]: https://docs.snapcraft.io/snap-documentation


<!-- FEEDBACK -->
<div class="p-notification--information">
  <p class="p-notification__response">
    We appreciate your feedback on the documentation. You can
    <a href="https://github.com/charmed-kubernetes/kubernetes-docs/edit/master/pages/k8s/install-offline.md" class="p-notification__action">edit this page</a>
    or
    <a href="https://github.com/charmed-kubernetes/kubernetes-docs/issues/new" class="p-notification__action">file a bug here</a>.
  </p>
</div>
