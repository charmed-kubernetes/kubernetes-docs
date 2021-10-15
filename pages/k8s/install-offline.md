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
In order to access the apt package repository, it is common to set up a local 
mirror or allow traffic through a proxy to the main archive.

There are many ways of setting up a local mirror. The repository is essentially just
a directory of files and some means of serving them (http, ftp, etc). It is common to
use tools such as **rsync**, **apt-mirror** or **aptly** to create the mirror.

If a proxy is already in use for the APT repository, it can be configured
according to the instructions under the heading 
[Configuring Charmed Kubernetes to work with proxies][]

### Series and architectures

Note that the mirror should contain packages for the required series (e.g. focal 
(Ubuntu 20.04), bionic) and architectures (e.g. `amd64`, `i386`) expected to be used
in the deployment. The core Charmed Kubernetes components all use the `focal` series,
but some additional charms may be based on other series.

### Setting up a proxy

- Tutorial on setting up a mirror with Rsync from [ubuntu community docs][rsync].
- Tutorial on setting up a mirror with apt-mirror from [HowtoForge][apt-mirror].
- Using aptly to mirror APT repositories from the [aptly documentation][aptly].

## Snap packages

The majority of charms, including all the core Charmed Kubernetes charms, rely on
[snap][] packages to deliver applications. Snaps are packages for desktop, cloud and
IoT that are easy to install, secure, cross‐platform and dependency‐free.

While it is _possible_ to download a snap package from the store, each snap will then
need to be authenticated, and subsequent updates, even in the case of security
updates, will require manual intervention. To avoid this, the recommended
solution is to install a to use the [snap-store-proxy][] software.

The snap store proxy can also be configured to run in an "air-gap" mode, which 
disconnects it from the upstream store and allows  

## Juju 

Since `Charmed Kubernetes` requires Juju, the Juju environment will also 
need to be deployed in an offline-mode. Details of how to install and run Juju
are in the relevant section of the [Juju documentation][offline mode].

## Container images

`Charmed Kubernetes` relies on pulling container images to function. Canonical provides a 
list of images required for each release at [github container images][github-container-images]. 
During configuration of the kubernetes cluster, configure the cloud to pull images from the
private container registry via the [containerd][] charm.  

1. Determine the latest image list for the selected bundle/kubernetes release (eg. `1.21.5.txt`)
1. Download the image list
1. Create an archive of all the container images
```bash
cd /tmp
sudo snap install docker  # used to pull and save container images
RELEASE=v1.21.5
rm -rf $RELEASE.txt
wget "https://raw.githubusercontent.com/charmed-kubernetes/bundle/master/container-images/$RELEASE.txt"
for container_image in $(cat $RELEASE.txt); do
  sudo docker pull $container_image
  mkdir -p $(dirname cdk-containers/$container_image)
  sudo docker save $container_image | gzip > cdk-containers/${container_image}.tgz
done
tar -czvf cdk-containers.tgz cdk-containers/  # Create a tar.gz file with the container images
```


## Python packages and PyPI

`Charmed Kubernetes` base charms all come with the pip wheels necessary to deploy the cloud.
Other charms (such as subordinate charms) used to monitor or provide metric data of those
machines may require pip packages to install into their virtual environments which aren't
bundled as wheels, and expect to install those dependencies from pypi. There is no
guarantee that any non-standard `Charmed Kubernetes` charm won't attempt to reach out to pypi
during it's install hooks. Any charm attempting to do so, will need to handle pip installing
from a different pypi-server using the `extra-index-url` argument and charm configs.

## Livepatch Proxy

The Linux Kernel supports realtime updates to the running kernel without restarting
the existing kernel. In normal use this requires network access to pull the kernel 
patches and apply to the running kernel. However, with [On Prem Livepatch][on-prem-livepatch],
patches  can be published to a locally available livepatch hosting server.


## Charmed Kubernetes 

### Bundle and charms
The specific bundle and charms which fulfill those bundles must be first retrieved, then locally installed
into Juju. One can retrieve the [bundles][], [overlays][], and charms to install locally
from the charmstore. 

from a connected machine:

1. Download the installable bundle
1. [Customize][customize-bundle] the bundle.yaml
1. Pull the charms for the bundle
1. Create archive of the deployment

```bash
cd /tmp
sudo snap install charm                # this app can pull from the charm store
rm -rf local-charmed-k8s/              # temporary directory to hold the entire bundle
BUNDLE=cs:charmed-kubernetes-733       # Choose a deployment bundle (example is 1.21.x)
charm pull $BUNDLE local-charmed-k8s/  # pull the bundle
# complete customization of the local-charmed-k8s/bundle.yaml
for CHARM in $(cat local-charmed-k8s/bundle.yaml | grep 'cs:' | cut -d":" -f2- | sort | uniq); do
  charm pull $CHARM local-charmed-k8s/$CHARM  # pull each charm of the bundle
  sed -i s#$CHARM#\"./$CHARM\"#g local-charmed-k8s/bundle.yaml
done
tar -czvf local-charmed-k8s.tgz local-charmed-k8s/  # Create a tar.gz file with the bundle
```

on air-gapped machine with access to the juju controller, 
1. Copy the local-charmed-k8s.tgz
1. Deploy
```bash
tar -xvf local-charmed-k8s.tgz
cd local-charmed-k8s/
juju deploy ./bundle.yaml  # deploys local charms into the model
```



## Configuring Charmed Kubernetes to work with proxies


## Additional considerations


### Ubuntu SSO
<!-- Not needed for CK, but needed on the snap store proxy... !-->

## Useful links


<!-- IMAGES -->



<!-- LINKS -->

[aptly]: https://www.aptly.info/
[bundles]: /kubernetes/docs/supported-versions
[apt-mirror]: https://apt-mirror.github.io/
[containerd]: https://ubuntu.com/kubernetes/docs/1.21/charm-containerd
[controller-config]: https://juju.is/docs/olm/create-controllers
[credentials]: https://juju.is/docs/olm/credentials
[customize-bundle]: /kubernetes/docs/install-manual#customising-the-bundle-install
[github-container-images]: https://github.com/charmed-kubernetes/bundle/tree/master/container-images
[juju-bundle]: https://juju.is/docs/sdk/bundles
[juju-constraints]: https://juju.is/docs/olm/constraints
[juju-docs]: https://juju.is/docs/olm/installing-juju
[juju-gui]: https://juju.is/docs/olm/accessing-juju%E2%80%99s-web-interface
[offline-mode]: https://juju.is/docs/t/offline-mode-strategies/1071
[on-prem-livepatch]: https://ubuntu.com/security/livepatch/docs/on_prem
[overlays]: /kubernetes/docs/install-manual#overlay
[quickstart]: /kubernetes/docs/quickstart
[snap]: https://snapcraft.io
[snaps]: https://docs.snapcraft.io/snap-documentation
[snap-store-proxy]: https://docs.ubuntu.com/snap-store-proxy
[rsync]: https://help.ubuntu.com/community/Rsyncmirror
[apt-mirror]: https://www.howtoforge.com/local_debian_ubuntu_mirror
[aptly]: https://www.aptly.info/doc/overview/

<!-- FEEDBACK -->
<div class="p-notification--information">
  <p class="p-notification__response">
    We appreciate your feedback on the documentation. You can
    <a href="https://github.com/charmed-kubernetes/kubernetes-docs/edit/master/pages/k8s/install-offline.md" class="p-notification__action">edit this page</a>
    or
    <a href="https://github.com/charmed-kubernetes/kubernetes-docs/issues/new" class="p-notification__action">file a bug here</a>.
  </p>
</div>
