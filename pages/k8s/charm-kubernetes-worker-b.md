---
wrapper_template: "kubernetes/docs/base_docs.html"
markdown_includes:
  nav: "kubernetes/docs/shared/_side-navigation.md"
context:
  title: "kubernetes-worker charm"
  description: Etcd Charm reference
keywords: kubernetes-worker, charm, config
tags: [reference]
sidebar: k8smain-sidebar
permalink: charm-kubernetes-worker-b.html
layout: [base, ubuntu-com]
toc: False
---

This charm deploys a container runtime, and additionally stands up the Kubernetes
worker applications: kubelet, and kube-proxy.

In order for this charm to be useful, it should be deployed with its companion
charm kubernetes-master and linked with an SDN-Plugin and a container runtime
such as containerd.

This charm has also been bundled up for your convenience so you can skip the
above steps, and deploy it with a single command:

```bash
juju deploy charmed-kubernetes
```

For more information about Charmed Kubernetes see the [overview documentation](/kubernetes/docs/overview)

## Scale out

To add additional compute capacity to your Kubernetes workers, you may
`juju add-unit` scale the cluster of applications. They will automatically
join any related kubernetes-master, and enlist themselves as ready once the
deployment is complete.

## Snap Configuration

The Kubernetes resources used by this charm are snap packages. When not
specified during deployment, these resources come from the public store. By
default, the snapd daemon will refresh all snaps installed from the store
four (4) times per day. A charm configuration option is provided for operators
to control this refresh frequency.

NOTE: this is a global configuration option and will affect the refresh
time for all snaps installed on a system.

### Examples:

##### refresh kubernetes-worker snaps every tuesday

```bash
juju config kubernetes-worker snapd_refresh="tue"
```

##### refresh snaps at 11pm on the last (5th) friday of the month

```bash
juju config kubernetes-worker snapd_refresh="fri5,23:00"
```
##### delay the refresh as long as possible

```bash
juju config kubernetes-worker snapd_refresh="max"
```

##### use the system default refresh timer

```bash
juju config kubernetes-worker snapd_refresh=""
```

For more information on the possible values for snapd_refresh, see the
refresh.timer section in the system options documentation.


## Configuration


| property | type | default | descrption |
|----------|------|---------|------------|
|  allow-privileged | string  | True  |  This option is now deprecated and has no effect. |
| channel   | string  | 1.17/stable  | Snap channel to install Kubernetes worker services from  |
| default-backend-image  | string  | auto  | Docker image to use for the default backend. Auto will select an image based on architecture.  |
| ingress   | boolean  | True  | Deploy the default http backend and ingress controller to handle ingress requests.  |
| ingress-ssl-chain-completion   | boolean  | False  | [See notes](#config-description-ingress-ssl-chain-completion)   |
| ingress-ssl-passthrough  | boolean | False  | Enable ssl passthrough on ingress server. This allows passing the ssl connection through to the workloads and not terminating it at the ingress controller.  |
| kubelet-extra-args  |  string | _none_  | [See notes](#config-description-kubelet-extra-args)  |
| kubelet-extra-config  | string  | none   | [See notes](#config-description-kubelet-extra-config)  |
| labels   | string  | _none_  | Labels can be used to organize and to select subsets of nodes in the cluster. Declare node labels in key=value format, separated by spaces.  |
| nagios_context   | string  | 'juju'  |   |
| nagios_servicesgroups  | string  |   | A comma-separated list of nagios servicegroups. If left empty, the nagios_context will be used as the servicegroup  |
| nginx-image   | string  | auto  | Docker image to use for the nginx ingress controller. Auto will select an image based on architecture.  |
| proxy-extra-args   | string  |   | [See notes](#config-description-kubelet-extra-args)  |
| require-manual-upgrade   | boolean  | True  | When true, worker services will not be upgraded until the user triggers it manually by running the upgrade action.  |
| snap_proxy   | string  |   |  **DEPRECATED** Use snap-http-proxy and snap-https-proxy model configuration settings. HTTP/HTTPS web proxy for Snappy to use when accessing the snap store. |
| snap_proxy_url   | string  |   |  **DEPRECATED** Use snap-store-proxy model configuration setting.  |
| snapd_refresh   | string  | max  | [See notes](#config-description-snapd_refresh)  |
| sysctl   | string  | [See notes](#config-default-sysctl)  | [See notes](#config-description-sysctl)   |


### ingress-ssl-chain-completion

<a id='config-description-ingress-ssl-chain-completion'> </a>

#### Description

Enable chain completion for TLS certificates used by the nginx ingress
controller.  Set this to true if you would like the ingress controller
to attempt auto-retrieval of intermediate certificates.  The default
(false) is recommended for all production kubernetes installations, and
any environment which does not have outbound Internet access.



### kubelet-extra-args

<a id='config-description-kubelet-extra-args'> </a>
#### Description

Space separated list of flags and key=value pairs that will be passed as arguments to
kubelet. For example a value like this:
  runtime-config=batch/v2alpha1=true profiling=true
will result in kubelet being run with the following options:
  --runtime-config=batch/v2alpha1=true --profiling=true
Note: As of Kubernetes 1.10.x, many of Kubelet's args have been deprecated, and can
be set with kubelet-extra-config instead.

---

### kubelet-extra-config

<a id='config-description-kubelet-extra-config'> </a>
#### Description

Extra configuration to be passed to kubelet. Any values specified in this
config will be merged into a KubeletConfiguration file that is passed to
the kubelet service via the --config flag. This can be used to override
values provided by the charm.

Requires Kubernetes 1.10+.

The value for this config must be a YAML mapping that can be safely
merged with a KubeletConfiguration file. For example:
`{evictionHard: {memory.available: 200Mi}}`

For more information about KubeletConfiguration, see upstream docs:
<https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/>

---


### nagios_context

<a id='config-description-nagios_context'> </a>
#### Description

Used by the nrpe subordinate charms.
A string that will be prepended to instance name to set the host name
in nagios. So for instance the hostname would be something like:
`juju-myservice-0`

If you're running multiple environments with the same services in them
this allows you to differentiate between them.

---

### proxy-extra-args

**Type**: string &nbsp;&nbsp;&nbsp; **Default**:

<a id='config-description-kubelet-extra-args'> </a>
Space separated list of flags and key=value pairs that will be passed as arguments to
kube-proxy. For example a value like this:
  `runtime-config=batch/v2alpha1=true profiling=true`
will result in kube-apiserver being run with the following options:
  `--runtime-config=batch/v2alpha1=true --profiling=true`

---

### snapd_refresh

<a id='config-description-snapd_refresh'> </a>

How often snapd handles updates for installed snaps. Setting an empty
string will check 4x per day. Set to "max" to delay the refresh as long
as possible. You may also set a custom string as described in the
'refresh.timer' section here:
<https://forum.snapcraft.io/t/system-options/87>

---

### sysctl

<a id='config-default-sysctl'> </a>
#### Default
```
 { net.ipv4.conf.all.forwarding : 1, net.ipv4.neigh.default.gc_thresh1 : 128, net.ipv4.neigh.default.gc_thresh2 : 28672, net.ipv4.neigh.default.gc_thresh3 : 32768, net.ipv6.neigh.default.gc_thresh1 : 128, net.ipv6.neigh.default.gc_thresh2 : 28672, net.ipv6.neigh.default.gc_thresh3 : 32768, fs.inotify.max_user_instances : 8192, fs.inotify.max_user_watches: 1048576 }
```
<a id='config-description-sysctl'> </a>

#### Description
YAML formatted associative array of sysctl values, e.g.:
'{kernel.pid_max : 4194303 }'. Note that kube-proxy handles
the conntrack settings. The proper way to alter them is to
use the proxy-extra-args config to set them, e.g.:
```
  juju config kubernetes-master proxy-extra-args="conntrack-min=1000000 conntrack-max-per-core=250000"
  juju config kubernetes-worker proxy-extra-args="conntrack-min=1000000 conntrack-max-per-core=250000"
```
The proxy-extra-args conntrack-min and conntrack-max-per-core can be set to 0 to ignore
kube-proxy's settings and use the sysctl settings instead. Note the fundamental difference between
the setting of conntrack-max-per-core vs nf_conntrack_max.


---


<!-- CONFIG ENDS -->




## Operational actions

The kubernetes-worker charm supports the following Operational Actions:

### Pause

Pausing the workload enables administrators to both drain and cordon
a unit for maintenance.

### Resume

Resuming the workload will uncordon a paused unit. Workloads will automatically
migrate unless otherwise directed via their application declaration.

## Relations

<ul class="p-list">


                <li class="p-list__item">
                  <a href="https://jaas.ai/search?provides=aws-integration">aws: aws-integration</a>
                </li>

                <li class="p-list__item">
                  <a href="https://jaas.ai/search?provides=azure-integration">azure: azure-integration</a>
                </li>

                <li class="p-list__item">
                  <a href="https://jaas.ai/search?provides=tls-certificates">certificates: tls-certificates</a>
                </li>

                <li class="p-list__item">
                  <a href="https://jaas.ai/search?provides=docker-registry">docker-registry: docker-registry</a>
                </li>

                <li class="p-list__item">
                  <a href="https://jaas.ai/search?provides=gcp-integration">gcp: gcp-integration</a>
                </li>

                <li class="p-list__item">
                  <a href="https://jaas.ai/search?provides=http">kube-api-endpoint: http</a>
                </li>

                <li class="p-list__item">
                  <a href="https://jaas.ai/search?provides=kube-control">kube-control: kube-control</a>
                </li>

                <li class="p-list__item">
                  <a href="https://jaas.ai/search?provides=kube-dns">kube-dns: kube-dns</a>
                </li>

                <li class="p-list__item">
                  <a href="https://jaas.ai/search?provides=mount">nfs: mount</a>
                </li>

                <li class="p-list__item">
                  <a href="https://jaas.ai/search?provides=openstack-integration">openstack: openstack-integration</a>
                </li>

                <li class="p-list__item">
                  <a href="https://jaas.ai/search?provides=vsphere-integration">vsphere: vsphere-integration</a>
                </li>




                <li class="p-list__item">
                  <a href="https://jaas.ai/search?requires=kubernetes-cni">cni: kubernetes-cni</a>
                </li>

                <li class="p-list__item">
                  <a href="https://jaas.ai/search?requires=container-runtime">container-runtime: container-runtime</a>
                </li>

                <li class="p-list__item">
                  <a href="https://jaas.ai/search?requires=nrpe-external-master">nrpe-external-master: nrpe-external-master</a>
                </li>


          </ul>

## FAQ
