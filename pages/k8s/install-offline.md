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

<div class="p-notification--positive"><p markdown="1" class="p-notification__response">
<span class="p-notification__status">Snap resources</span>
Many current charms include snaps as bundled resources. The inclusion of
snaps as charm resources is deprecated, and these will be removed in future
versions of these charms. Deployments will need to be able to access the 
official Snap Store or use the Snap Store Proxy to gain access to the required
snaps. </a>
</p></div>

The majority of charms, including all the core Charmed Kubernetes charms, rely on
[snap][] packages to deliver applications. Snaps are packages for desktop, cloud and
IoT that are easy to install, secure, cross‐platform and dependency‐free.

The list of snaps required by Charmed Kubernetes is detailed in the "components"
page for each release. For example, for 1.22, the 
[snaps are listed here][1.22-components].

While it is _possible_ to download a snap package from the store, each snap will then
need to be authenticated, and subsequent updates, even in the case of security
updates, will require manual intervention. To avoid this, the recommended
solution is to use the [snap-store-proxy][] software.

The snap store proxy can also be configured to run in an "air-gap" mode, which 
disconnects it from the upstream store and allows snaps to be "sideloaded" into
the local store. Information on how to do this is in the 
[snap store proxy documentation][sideload].


Note: Running the Snap Store Proxy also requires access to a PostgreSQL database,
and an Ubuntu SSO account.

## Juju 

Since `Charmed Kubernetes` requires Juju, the Juju environment will also 
need to be deployed in an offline-mode. Details of how to install and run Juju
are in the relevant section of the [Juju documentation][offline mode].

## Container images

`Charmed Kubernetes` relies on container images for many of its components. To
run an air-gap or offline installation, it will be necessary to make these 
images available to Juju, which is usually achieved by running a local 
image registry, such as Docker.

### Creating a private registry

The registry is simply a store for managing and serving up the requested images. 
Many public clouds (Azure, AWS, Google etc) also have registry components which
could be used, but for the small number of images required for Charmed Kubernetes
it is sufficient to run a local repository using Docker.

The recommended method is to use Juju to deploy a Docker registry and use that to 
serve the required images. See the [Docker registry documentation][] for more
details. 

Note that if you wish to deploy the registry in the same Juju model (recommended) as
Charmed Kubernetes, you should populate the registry with the images before
deploying the rest of Charmed Kubernetes.

### Fetching the required images

A list of the required images for each supported release is made available as part of
the Charmed Kubernetes bundle repository on github. You can inspect or download the 
lists from the [container images][] directory.  

Using this list, it is possible to fetch the desired images locally on a system which 
has access to public repositories. 

For example, to do this with Docker you could run:

```bash
docker login
RELEASE=v1.21.5
wget "https://raw.githubusercontent.com/charmed-kubernetes/bundle/master/container-images/$RELEASE.txt"
for container_image in $(cat $RELEASE.txt); do
  docker pull rocks.canonical.com/cdk/$container_image
  docker save $container_image | gzip > ${container_image//[^A-Za-z0-9-]/.}.tgz
done
rm -rf $RELEASE.txt 
```

When using the Juju docker-registry charm, the image archives can be copied to the running unit
added to the registry. Note that if the `docker-registry` charm itself has been deployed offline,
you will also need to fetch the registry image:

```bash
docker pull registry
docker save registry | gzip > registry.tgz
```

The local image files can then be copied to the unit running the docker-registry and loaded:

```bash
juju scp *.tgz docker-registry/0:
juju ssh docker-registry/0
ls -1 *.tgz | xargs --no-run-if-empty -L 1 docker load -i
rm -rf *.tgz
exit
```

You can confirm the images are present by running the action:

```bash
juju run-action --wait docker-registry/0 images
```

## Python packages and PyPI

**Charmed Kubernetes** base charms all come with the pip wheels necessary.
Other charms used to monitor or provide metric data of those machines may require pip 
packages to install into their virtual environments which aren't
bundled as wheels, and expect to install those dependencies from PyPI. There is no
guarantee that any non-standard Charmed Kubernetes charm won't attempt to reach out to PyPI
during installation. Any charm attempting to do so, will need to handle pip installing
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
sudo snap install charm                
rm -rf local-charmed-k8s/              
BUNDLE=cs:charmed-kubernetes-733       # Choose a deployment bundle (example is 1.21.x)
charm pull $BUNDLE local-charmed-k8s/  # pull the bundle

for CHARM in $(cat local-charmed-k8s/bundle.yaml | grep 'cs:' | cut -d":" -f2- | sort | uniq); do
  charm pull $CHARM local-charmed-k8s/$CHARM  # pull each charm of the bundle
  sed -i s#$CHARM#\"./$CHARM\"#g local-charmed-k8s/bundle.yaml
done
tar -czvf local-charmed-k8s.tgz local-charmed-k8s/  # Create a tar.gz file with the bundle
```

<!-- any additional charms not part of core bundle !-->

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
[bundles]: /kubernetes/docs/supported-versions
[containerd]: https://ubuntu.com/kubernetes/docs/1.21/charm-containerd
[1.22-components]: https://ubuntu.com/kubernetes/docs/1.22/components#snaps
[controller-config]: https://juju.is/docs/olm/create-controllers
[credentials]: https://juju.is/docs/olm/credentials
[customize-bundle]: /kubernetes/docs/install-manual#customising-the-bundle-install
[container images]: https://github.com/charmed-kubernetes/bundle/tree/master/container-images
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
[sideload]: https://docs.ubuntu.com/snap-store-proxy/en/airgap#usage

<!-- FEEDBACK -->
<div class="p-notification--information">
  <p class="p-notification__response">
    We appreciate your feedback on the documentation. You can
    <a href="https://github.com/charmed-kubernetes/kubernetes-docs/edit/master/pages/k8s/install-offline.md" class="p-notification__action">edit this page</a>
    or
    <a href="https://github.com/charmed-kubernetes/kubernetes-docs/issues/new" class="p-notification__action">file a bug here</a>.
  </p>
</div>
