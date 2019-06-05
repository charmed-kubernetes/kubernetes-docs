---
wrapper_template: "base_docs.html"
markdown_includes:
  nav: "shared/_side-navigation.md"
context:
  title: "Configuration"
  description: How to configure various settings on your CDK cluster.
keywords: juju, config
tags: [reference]
sidebar: k8smain-sidebar
permalink: config.html
layout: [base, ubuntu-com]
toc: False
---

The **Charmed Distribution of Kubernetes<sup>&reg;</sup>** ships with a default
configuration that will "just work" in the majority of cases. However, it
remains highly configurable to suit use case.

The commonly used settings are more completely discussed in other relevant
parts of the documentation, but this page contains complete listings of the
configuration options, including their default values and descriptive notes.
Any additional information will be included beneath each table of settings.

<div class="p-notification--caution">
  <p markdown="1" class="p-notification__response">
    <span class="p-notification__status">Caution:</span>
Always be sure to read the description before changing a configurations value.
Some settings may require an application to be restarted, causing downtime or disruption
to your cluster.
  </p>
</div>

## Checking the current configuration

To check the current configuration settings for a charm, just run `juju config`
followed by the name of the charm. For example, to see the current
configuration for etcd, run:

```bash
juju config etcd
```

## Setting a config option

To set an option, simply run the config command as above, with an additional
`<key>=<value>` argument. For example, to change the network CIDR for flannel:

```bash
juju config flannel cidr=10.5.0.0/16
```


## Core components

### etcd

|Name                    | Type    | Default   | Description                    |
|========================|=========|===========|================================|
| bind_to_all_interfaces | boolean | True      |The service binds to all network interfaces if true. The service binds only to the first found bind address of each relation if false |
| channel                | string  | 2.3/stable|The snap channel to install from|
| management_port        | int     | 2380      |Port to run the ETCD Management service|
| nagios_context         | string  | juju      |Used by the nrpe subordinate charms. A string that will be prepended to instance name to set the host name in nagios. So for instance the hostname would be something like:     juju-myservice-0 If you're running multiple environments with the same services in them this allows you to differentiate between them. |
| nagios_servicegroups   | string  |           |A comma-separated list of nagios servicegroups. If left empty, the nagios_context will be used as the servicegroup |
| port                   | int     | 2379      |Port to run the public ETCD service on|
| snap_proxy             | string  |           |DEPRECATED. Use snap-http-proxy and snap-https-proxy model configuration settings. HTTP/HTTPS web proxy for Snappy to use when accessing the snap store. |
| snap_proxy_url         | string  |           |DEPRECATED. Use snap-store-proxy model configuration setting. The address of a Snap Store Proxy to use for snaps e.g. http://snap-proxy.example.com |
| snapd_refresh          | string  | max       |How often snapd handles updates for installed snaps. Set to an empty string to check 4x per day. Set to "max" (the default) to check once per month based on the charm deployment date. You may also set a custom string as described in the 'refresh.timer' section here:   https://forum.snapcraft.io/t/system-options/87 |

### kubernetes-master

|Name                              | Type    | Default   | Description          |
|==================================|=========|===========|======================|
| addons-registry                  | string  |           |Specify the docker registry to use when applying addons|
| allow-privileged                 | string  | auto      |Allow kube-apiserver to run in privileged mode. Supported values are "true", "false", and "auto". If "true", kube-apiserver will run in privileged mode by default. If "false", kube-apiserver will never run in privileged mode. If "auto", kube-apiserver will not run in privileged mode by default, but will switch to privileged mode if gpu hardware is detected on a worker node. |
| api-extra-args                   | string  |           |Space separated list of flags and key=value pairs that will be passed as arguments to kube-apiserver. For example a value like this:   runtime-config=batch/v2alpha1=true profiling=true will result in kube-apiserver being run with the following options:   --runtime-config=batch/v2alpha1=true --profiling=true |
| apt-key-server                   | string  | hkp://keyserver.ubuntu.com:80|APT Key Server|
| audit-policy                     | string  | [See notes below](#audit-policy) |Audit policy passed to kube-apiserver via --audit-policy-file. For more info, please refer to the upstream documentation at https://kubernetes.io/docs/tasks/debug-application-cluster/audit/ |
| audit-webhook-config             | string  |           |Audit webhook config passed to kube-apiserver via --audit-webhook-config-file. For more info, please refer to the upstream documentation at https://kubernetes.io/docs/tasks/debug-application-cluster/audit/ |
| authorization-mode               | string  | AlwaysAllow|Comma separated authorization modes. Allowed values are "RBAC", "Node", "Webhook", "ABAC", "AlwaysDeny" and "AlwaysAllow". |
| channel                          | string  | 1.14/stable|Snap channel to install Kubernetes master services from |
| client_password                  | string  |           |Password to be used for admin user (leave empty for random password). |
| controller-manager-extra-args    | string  |           |Space separated list of flags and key=value pairs that will be passed as arguments to kube-controller-manager. For example a value like this:   runtime-config=batch/v2alpha1=true profiling=true will result in kube-controller-manager being run with the following options:   --runtime-config=batch/v2alpha1=true --profiling=true |
| cuda_repo                        | string  | 10.0.130-1|The cuda-repo package version to install. |
| dashboard-auth                   | string  | auto      |Method of authentication for the Kubernetes dashboard. Allowed values are "auto",  "basic", and "token". If set to "auto", basic auth is used unless Keystone is  related to kubernetes-master, in which case token auth is used. |
| default-storage                  | string  | auto      |The storage class to make the default storage class. Allowed values are "auto", "none", "ceph-xfs", "ceph-ext4". Note: Only works in Kubernetes >= 1.10 |
| dns-provider                     | string  | auto      |DNS provider addon to use. Can be "auto", "core-dns", "kube-dns", or "none".  CoreDNS is only supported on Kubernetes 1.14+.  When set to "auto", the behavior is as follows: - New deployments of Kubernetes 1.14+ will use CoreDNS - New deployments of Kubernetes 1.13 or older will use KubeDNS - Upgraded deployments will continue to use whichever provider was previously used. |
| dns_domain                       | string  | cluster.local|The local domain for cluster dns|
| docker-ce-package                | string  | docker-ce=5:18.09.1~3-0~ubuntu-bionic|The pinned version of docker-ce package installed with nvidia-docker. |
| docker-opts                      | string  |           |Extra options to pass to the Docker daemon. e.g. --insecure-registry. |
| docker_runtime                   | string  | auto      |Docker runtime to install valid values are "upstream" (Docker PPA), "nvidia" (Nvidia PPA), "apt" (Ubuntu archive), "auto" (Nvidia PPA or Ubuntu archive, based on your hardware), or "custom" (must have set `docker_runtime_repo` URL, `docker_runtime_key_url` URL and `docker_runtime_package` name). |
| docker_runtime_key_url           | string  |           |Custom Docker repository validation key URL. |
| docker_runtime_package           | string  |           |Custom Docker repository package name. |
| docker_runtime_repo              | string  |           |Custom Docker repository, given in deb format.  Use `{ARCH}` to determine architecture at runtime.  Use `{CODE}` to set release codename.  E.g. `deb [arch={ARCH}] https://download.docker.com/linux/ubuntu {CODE} stable`. |
| enable-cgroups                   | boolean | False     |Enable GRUB cgroup overrides cgroup_enable=memory swapaccount=1. WARNING changing this option will reboot the host - use with caution on production services. |
| enable-dashboard-addons          | boolean | True      |Deploy the Kubernetes Dashboard and Heapster addons|
| enable-keystone-authorization    | boolean | False     |If true and the Keystone charm is related, users will authorize against the Keystone server. Note that if related, users will always authenticate against Keystone. |
| enable-metrics                   | boolean | True      |If true the metrics server for Kubernetes will be deployed onto the cluster. |
| enable-nvidia-plugin             | string  | auto      |Load the nvidia device plugin daemonset. Supported values are "auto" and "false". When "auto", the daemonset will be loaded only if GPUs are detected. When "false" the nvidia device plugin will not be loaded. |
| extra_packages                   | string  |           |Space separated list of extra deb packages to install. |
| extra_sans                       | string  |           |Space-separated list of extra SAN entries to add to the x509 certificate created for the master nodes. |
| ha-cluster-dns                   | string  |           |DNS entry to use with the HA Cluster subordinate charm. Mutually exclusive with ha-cluster-vip. |
| ha-cluster-vip                   | string  |           |Virtual IP for the charm to use with the HA Cluster subordinate charm Mutually exclusive with ha-cluster-dns. Multiple virtual IPs are separated by spaces. |
| http_proxy                       | string  |           |URL to use for HTTP_PROXY to be used by Docker. Useful in egress-filtered environments where a proxy is the only option for accessing the registry to pull images. |
| https_proxy                      | string  |           |URL to use for HTTPS_PROXY to be used by Docker. Useful in egress-filtered environments where a proxy is the only option for accessing the registry to pull images. |
| install_from_upstream            | boolean | False     |Toggle installation from Ubuntu archive vs the Docker PPA (DEPRECATED; please use docker_runtime instead). |
| install_keys                     | string  |           |List of signing keys for install_sources package sources, per charmhelpers standard format (a yaml list of strings encoded as a string). The keys should be the full ASCII armoured GPG public keys. While GPG key ids are also supported and looked up on a keyserver, operators should be aware that this mechanism is insecure. null can be used if a standard package signing key is used that will already be installed on the machine, and for PPA sources where the package signing key is securely retrieved from Launchpad. |
| install_sources                  | string  |           |List of extra apt sources, per charm-helpers standard format (a yaml list of strings encoded as a string). Each source may be either a line that can be added directly to sources.list(5), or in the form ppa:<user>/<ppa-name> for adding Personal Package Archives, or a distribution component to enable. |
| keystone-policy                  | string  |  [see notes below](#keystone-policy) |Policy for Keystone authentication. This is used when a Keystone charm is related to kubernetes-master in order to provide authentication and authorization for Keystone users on the Kubernetes cluster. |
| keystone-ssl-ca                  | string  |           |Keystone certificate authority encoded in base64 for securing communications to Keystone. For example: `juju config kubernetes-master keystone-ssl-ca=$(base64 /path/to/ca.crt)` |
| nagios_context                   | string  | juju      |Used by the nrpe subordinate charms. A string that will be prepended to instance name to set the host name in nagios. So for instance the hostname would be something like:     juju-myservice-0 If you're running multiple environments with the same services in them this allows you to differentiate between them. |
| nagios_servicegroups             | string  |           |A comma-separated list of nagios servicegroups. If left empty, the nagios_context will be used as the servicegroup |
| no_proxy                         | string  |           |Comma-separated list of destinations (either domain names or IP addresses) which should be accessed directly, rather than through the proxy defined in http_proxy or https_proxy. Must be less than 2023 characters long. |
| nvidia-container-runtime-package | string  | nvidia-container-runtime=2.0.0+docker18.09.1-1|The pinned version of nvidia-container-runtime package. |
| nvidia-docker-package            | string  | nvidia-docker2=2.0.3+docker18.09.1-1|The pinned version of nvidia-docker2 package. |
| package_status                   | string  | install   |The status of service-affecting packages will be set to this value in the dpkg database. Valid values are "install" and "hold". |
| require-manual-upgrade           | boolean | True      |When true, master nodes will not be upgraded until the user triggers it manually by running the upgrade action. |
| scheduler-extra-args             | string  |           |Space separated list of flags and key=value pairs that will be passed as arguments to kube-scheduler. For example a value like this:   runtime-config=batch/v2alpha1=true profiling=true will result in kube-scheduler being run with the following options:   --runtime-config=batch/v2alpha1=true --profiling=true |
| service-cidr                     | string  | 10.152.183.0/24|CIDR to user for Kubernetes services. Cannot be changed after deployment.|
| snap_proxy                       | string  |           |DEPRECATED. Use snap-http-proxy and snap-https-proxy model configuration settings. HTTP/HTTPS web proxy for Snappy to use when accessing the snap store. |
| snap_proxy_url                   | string  |           |DEPRECATED. Use snap-store-proxy model configuration setting. The address of a Snap Store Proxy to use for snaps e.g. http://snap-proxy.example.com |
| snapd_refresh                    | string  | max       |How often snapd handles updates for installed snaps. Setting an empty string will check 4x per day. Set to "max" to delay the refresh as long as possible. You may also set a custom string as described in the 'refresh.timer' section here:   https://forum.snapcraft.io/t/system-options/87 |
| storage-backend                  | string  | auto      |The storage backend for kube-apiserver persistence. Can be "etcd2", "etcd3", or "auto". Auto mode will select etcd3 on new installations, or etcd2 on upgrades. |


#### keystone-policy

```
apiVersion: v1
kind: ConfigMap
metadata:
  name: k8s-auth-policy
  namespace: kube-system
  labels:
    k8s-app: k8s-keystone-auth
data:
  policies: |
    [
      {
       "resource": {
          "verbs": ["get", "list", "watch"],
          "resources": ["*"],
          "version": "*",
          "namespace": "*"
        },
        "match": [
          {
            "type": "role",
            "values": ["k8s-viewers"]
          },
          {
            "type": "project",
            "values": ["k8s"]
          }
        ]
      },
      {
       "resource": {
          "verbs": ["*"],
          "resources": ["*"],
          "version": "*",
          "namespace": "default"
        },
        "match": [
          {
            "type": "role",
            "values": ["k8s-users"]
          },
          {
            "type": "project",
            "values": ["k8s"]
          }
        ]
      },
      {
       "resource": {
          "verbs": ["*"],
          "resources": ["*"],
          "version": "*",
          "namespace": "*"
        },
        "match": [
          {
            "type": "role",
            "values": ["k8s-admins"]
          },
          {
            "type": "project",
            "values": ["k8s"]
          }
        ]
      }
    ]
```

#### audit policy

```yaml
apiVersion: audit.k8s.io/v1beta1
kind: Policy
rules:
# Don't log read-only requests from the apiserver
- level: None
  users: ["system:apiserver"]
  verbs: ["get", "list", "watch"]
# Don't log kube-proxy watches
- level: None
  users: ["system:kube-proxy"]
  verbs: ["watch"]
  resources:
  - resources: ["endpoints", "services"]
# Don't log nodes getting their own status
- level: None
  userGroups: ["system:nodes"]
  verbs: ["get"]
  resources:
  - resources: ["nodes"]
# Don't log kube-controller-manager and kube-scheduler getting endpoints
- level: None
  users: ["system:unsecured"]
  namespaces: ["kube-system"]
  verbs: ["get"]
  resources:
  - resources: ["endpoints"]
# Log everything else at the Request level.
- level: Request
  omitStages:
  - RequestReceived
```

### kubernetes-worker

kubernetes-worker
|Name                              | Type    | Default   | Description          |
|==================================|=========|===========|======================|
| allow-privileged                 | string  | true      |This option is now deprecated and has no effect. |
| apt-key-server                   | string  | hkp://keyserver.ubuntu.com:80|APT Key Server|
| channel                          | string  | 1.14/stable|Snap channel to install Kubernetes worker services from |
| cuda_repo                        | string  | 10.0.130-1|The cuda-repo package version to install. |
| default-backend-image            | string  | auto      |Docker image to use for the default backend. Auto will select an image based on architecture. |
| docker-ce-package                | string  | docker-ce=5:18.09.1~3-0~ubuntu-bionic|The pinned version of docker-ce package installed with nvidia-docker. |
| docker-logins                    | string  | []        |Docker login credentials. Setting this config allows Kubelet to pull images from registries where auth is required.  The value for this config must be a JSON array of credential objects, like this:   [{"server": "my.registry", "username": "myUser", "password": "myPass"}] |
| docker-opts                      | string  |           |Extra options to pass to the Docker daemon. e.g. --insecure-registry. |
| docker_runtime                   | string  | auto      |Docker runtime to install valid values are "upstream" (Docker PPA), "nvidia" (Nvidia PPA), "apt" (Ubuntu archive), "auto" (Nvidia PPA or Ubuntu archive, based on your hardware), or "custom" (must have set `docker_runtime_repo` URL, `docker_runtime_key_url` URL and `docker_runtime_package` name). |
| docker_runtime_key_url           | string  |           |Custom Docker repository validation key URL. |
| docker_runtime_package           | string  |           |Custom Docker repository package name. |
| docker_runtime_repo              | string  |           |Custom Docker repository, given in deb format.  Use `{ARCH}` to determine architecture at runtime.  Use `{CODE}` to set release codename.  E.g. `deb [arch={ARCH}] https://download.docker.com/linux/ubuntu {CODE} stable`. |
| enable-cgroups                   | boolean | False     |Enable GRUB cgroup overrides cgroup_enable=memory swapaccount=1. WARNING changing this option will reboot the host - use with caution on production services. |
| http_proxy                       | string  |           |URL to use for HTTP_PROXY to be used by Docker. Useful in egress-filtered environments where a proxy is the only option for accessing the registry to pull images. |
| https_proxy                      | string  |           |URL to use for HTTPS_PROXY to be used by Docker. Useful in egress-filtered environments where a proxy is the only option for accessing the registry to pull images. |
| ingress                          | boolean | True      |Deploy the default http backend and ingress controller to handle ingress requests. |
| ingress-ssl-chain-completion     | boolean | False     |Enable chain completion for TLS certificates used by the nginx ingress controller.  Set this to true if you would like the ingress controller to attempt auto-retrieval of intermediate certificates.  The default (false) is recommended for all production kubernetes installations, and any environment which does not have outbound Internet access. |
| kubelet-extra-args               | string  |           |Space separated list of flags and key=value pairs that will be passed as arguments to kubelet. For example a value like this:   runtime-config=batch/v2alpha1=true profiling=true will result in kube-apiserver being run with the following options:   --runtime-config=batch/v2alpha1=true --profiling=true Note: As of Kubernetes 1.10.x, many of Kubelet's args have been deprecated, and can be set with kubelet-extra-config instead. |
| kubelet-extra-config             | string  | {}        |Extra configuration to be passed to kubelet. Any values specified in this config will be merged into a KubeletConfiguration file that is passed to the kubelet service via the --config flag. This can be used to override values provided by the charm.  Requires Kubernetes 1.10+.  The value for this config must be a YAML mapping that can be safely merged with a KubeletConfiguration file. For example:   {evictionHard: {memory.available: 200Mi}}  For more information about KubeletConfiguration, see upstream docs: https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ |
| labels                           | string  |           |Labels can be used to organize and to select subsets of nodes in the cluster. Declare node labels in key=value format, separated by spaces. |
| nagios_context                   | string  | juju      |Used by the nrpe subordinate charms. A string that will be prepended to instance name to set the host name in nagios. So for instance the hostname would be something like:     juju-myservice-0 If you're running multiple environments with the same services in them this allows you to differentiate between them. |
| nagios_servicegroups             | string  |           |A comma-separated list of nagios servicegroups. If left empty, the nagios_context will be used as the servicegroup |
| nginx-image                      | string  | auto      |Docker image to use for the nginx ingress controller. Auto will select an image based on architecture. |
| no_proxy                         | string  |           |Comma-separated list of destinations (either domain names or IP addresses) which should be accessed directly, rather than through the proxy defined in http_proxy or https_proxy. Must be less than 2023 characters long. |
| nvidia-container-runtime-package | string  | nvidia-container-runtime=2.0.0+docker18.09.1-1|The pinned version of nvidia-container-runtime package. |
| nvidia-docker-package            | string  | nvidia-docker2=2.0.3+docker18.09.1-1|The pinned version of nvidia-docker2 package. |
| proxy-extra-args                 | string  |           |Space separated list of flags and key=value pairs that will be passed as arguments to kube-proxy. For example a value like this:   runtime-config=batch/v2alpha1=true profiling=true will result in kube-apiserver being run with the following options:   --runtime-config=batch/v2alpha1=true --profiling=true |
| require-manual-upgrade           | boolean | True      |When true, worker services will not be upgraded until the user triggers it manually by running the upgrade action. |
| snap_proxy                       | string  |           |DEPRECATED. Use snap-http-proxy and snap-https-proxy model configuration settings. HTTP/HTTPS web proxy for Snappy to use when accessing the snap store. |
| snap_proxy_url                   | string  |           |DEPRECATED. Use snap-store-proxy model configuration setting. The address of a Snap Store Proxy to use for snaps e.g. http://snap-proxy.example.com |
| snapd_refresh                    | string  | max       |How often snapd handles updates for installed snaps. Setting an empty string will check 4x per day. Set to "max" to delay the refresh as long as possible. You may also set a custom string as described in the 'refresh.timer' section here:   https://forum.snapcraft.io/t/system-options/87 |



##CNI

### flannel

|Name                  | Type    | Default   | Description                      |
|======================|=========|===========|==================================|
| cidr                 | string  | 10.1.0.0/16|Network CIDR to assign to Flannel |
| iface                | string  |           |The interface to bind flannel overlay networking. The default value is the interface bound to the cni endpoint. |
| nagios_context       | string  | juju      |Used by the nrpe subordinate charms. A string that will be prepended to instance name to set the host name in nagios. So for instance the hostname would be something like:     juju-myservice-0 If you're running multiple environments with the same services in them this allows you to differentiate between them. |
| nagios_servicegroups | string  |           |A comma-separated list of nagios servicegroups. If left empty, the nagios_context will be used as the servicegroup |


### canal
|Name                  | Type    | Default   | Description                      |
|======================|=========|===========|==================================|
| calico-node-image    | string  | quay.io/calico/node:v2.6.12|The image id to use for calico/node. |
| calico-policy-image  | string  | quay.io/calico/kube-controllers:v1.0.5|The image id to use for calico/kube-controllers. |
| cidr                 | string  | 10.1.0.0/16|Network CIDR to assign to Flannel |
| iface                | string  |           |The interface to bind flannel overlay networking. The default value is the interface bound to the cni endpoint. |
| nagios_context       | string  | juju      |Used by the nrpe subordinate charms. A string that will be prepended to instance name to set the host name in nagios. So for instance the hostname would be something like:     juju-myservice-0 If you're running multiple environments with the same services in them this allows you to differentiate between them. |
| nagios_servicegroups | string  |           |A comma-separated list of nagios servicegroups. If left empty, the nagios_context will be used as the servicegroup |

### calico
|Name                 | Type    | Default   | Description                       |
|=====================|=========|===========|===================================|
| calico-node-image   | string  | quay.io/calico/node:v2.6.12|The image id to use for calico/node. |
| calico-policy-image | string  | quay.io/calico/kube-controllers:v1.0.5|The image id to use for calico/kube-controllers. |
| ipip                | boolean | False     |Enable IP tunneling |
| nat-outgoing        | boolean | True      |NAT outgoing traffic |

### tigera-secure-EE

|Name                           | Type    | Default   | Description             |
|===============================|=========|===========|=========================|
| enable-elasticsearch-operator | boolean | True      |Enable deployment of elasticsearch-operator into Kubernetes. This provides a monitoring and metrics solution for use with Tigera EE that is suitable for proof-of-concept purposes, but is not recommended for production use. |
| ipip                          | string  | Never     |IPIP mode. Must be one of "Always", "CrossSubnet", or "Never". |
| license-key                   | string  |           |Tigera EE license key, base64-encoded. Example:  juju config tigera-secure-ee license-key=$(base64 -w0 license.yaml) |
| nat-outgoing                  | boolean | True      |NAT outgoing traffic |
| registry                      | string  |           |Registry to use for images. If unspecified, defaults will be used: docker.io, quay.io, docker.elastic.co |
| registry-credentials          | string  |           |Private docker registry credentials, in the form of a base64-encoded docker config.json file. Example:  juju config tigera-secure-ee registry-credentials=$(base64 -w0 config.json) |

## High Availability

### keepalived

|Name                  | Type    | Default   | Description                      |
|======================|=========|===========|==================================|
| healthcheck_interval | int     | 2         |vrrp_script-based health-check interval, in seconds |
| network_interface    | string  |           |Network interface name for the VIP. The default value is the result of running the following command: `route | grep default | head -n 1 | awk {'print $8'}`. |
| port                 | int     | 443       |A port to pass to clients. |
| router_id            | int     | 23        |Virtual router identifier - a number between 1 and 255 that's unique within the network segment |
| vip_hostname         | string  |           |A VIP hostname to pass to clients. |
| virtual_ip           | string  |           |Virtual IP/netmask that will be moved between instances, e.g.: 10.1.2.3/16 |



## Integrators

### aws-integrator

|Name            | Type    | Default   | Description                            |
|================|=========|===========|========================================|
| access-key     | string  |           |An IAM access key.  It is strongly recommended that you use 'juju trust' instead, if available. |
| credentials    | string  |           |The base64-encoded contents of an AWS credentials file, which must include both 'aws_access_key_id' and 'aws_secret_access_key' fields.  This can be used from bundles with 'include-base64://' (see https://jujucharms.com/docs/stable/charms-bundles#setting-charm-configurations-options-in-a-bundle), or from the command-line with 'juju config aws credentials="$(base64 /path/to/file)"'.  It is strongly recommended that you use 'juju trust' instead, if available. This will take precedence over the 'access-key' / 'secret-key' config options. |
| secret-key     | string  |           |An IAM secret key.  It is strongly recommended that you use 'juju trust' instead, if available. |
| snap_proxy     | string  |           |DEPRECATED. Use snap-http-proxy and snap-https-proxy model configuration settings. HTTP/HTTPS web proxy for Snappy to use when accessing the snap store. |
| snap_proxy_url | string  |           |DEPRECATED. Use snap-store-proxy model configuration setting. The address of a Snap Store Proxy to use for snaps e.g. http://snap-proxy.example.com |
| snapd_refresh  | string  |           |How often snapd handles updates for installed snaps. The default (an empty string) is 4x per day. Set to "max" to check once per month based on the charm deployment date. You may also set a custom string as described in the 'refresh.timer' section here:   https://forum.snapcraft.io/t/system-options/87 |

###gcp-integrator

|Name            | Type    | Default   | Description                            |
|================|=========|===========|========================================|
| credentials    | string  |           |The base64-encoded contents of an GCP credentials JSON file.  This can be used from bundles with 'include-base64://' (see https://jujucharms.com/docs/stable/charms-bundles#setting-charm-configurations-options-in-a-bundle), or from the command-line with 'juju config gcp credentials="$(base64 /path/to/file)"'.  It is strongly recommended that you use 'juju trust' instead, if available. |
| snap_proxy     | string  |           |HTTP/HTTPS web proxy for Snappy to use when accessing the snap store. |
| snap_proxy_url | string  |           |The address of a Snap Store Proxy to use for snaps e.g. http://snap-proxy.example.com |
| snapd_refresh  | string  |           |How often snapd handles updates for installed snaps. The default (an empty string) is 4x per day. Set to "max" to check once per month based on the charm deployment date. You may also set a custom string as described in the 'refresh.timer' section here:   https://forum.snapcraft.io/t/system-options/87 |


### openstack-integrator

|Name                    | Type    | Default   | Description                    |
|========================|=========|===========|================================|
| auth-url               | string  |           |The URL of the keystone API used to authenticate. On OpenStack control panels, this can be found at Access and Security > API Access > Credentials. |
| bs-version             | string  | unset     |Used to override automatic version detection. Valid values are v1, v2, v3 and auto. When auto is specified automatic detection will select the highest supported version exposed by the underlying OpenStack cloud. If not set, will use the upstream default. |
| credentials            | string  |           |The base64-encoded contents of a JSON file containing OpenStack credentials.  The credentials must contain the following keys: auth-url, username, password, project-name, user-domain-name, and project-domain-name.  It could also contain a base64-encoded CA certificate in endpoint-tls-ca key value.  This can be used from bundles with 'include-base64://' (see https://jujucharms.com/docs/stable/charms-bundles#setting-charm-configurations-options-in-a-bundle), or from the command-line with 'juju config openstack credentials="$(base64 /path/to/file)"'.  It is strongly recommended that you use 'juju trust' instead, if available. |
| endpoint-tls-ca        | string  |           |A CA certificate that can be used to verify the target cloud API endpoints. Use 'include-base64://' in a bundle to include a certificate. Otherwise, pass a base64-encoded certificate (base64 of "-----BEGIN" to "-----END") as a config option in a Juju CLI invocation. |
| floating-network-id    | string  |           |Floating IP network ID that should be used to set FIPs for load balancers. |
| ignore-volume-az       | boolean | unset     |Used to influence availability zone use when attaching Cinder volumes. When Nova and Cinder have different availability zones, this should be set to true. This is most commonly the case where there are many Nova availability zones but only one Cinder availability zone. If not set, will use the upstream default. |
| lb-method              | string  |           |Specifies an algorithm load balancer, that should be one between ROUND_ROBIN, LEAST_CONNECTIONS, SOURCE_IP. |
| manage-security-groups | boolean | False     |Whether or not the Load Balancer should automatically manage security groups rule. In case it is set to false, Load Balancer rules will be added to project (tenant) default security-group. In case it is set to true, a new security-group will be created for each Load Balancer, as well as its corresponding rules. It is advised to set appropriate number of security-groups and rules. |
| password               | string  |           |Password of a valid user set in keystone.|
| project-domain-name    | string  |           |Name of the project domain where you want to create your resources.|
| project-name           | string  |           |Name of project where you want to create your resources.|
| region                 | string  |           |Name of the region where you want to create your resources.|
| subnet-id              | string  |           |Subnet ID from OpenStack that will be used to setup Load Balancers. Flag LoadBalancer becomes active on cloud.conf file only if this config is set. |
| trust-device-path      | boolean | unset     |In most scenarios the block device names provided by Cinder (e.g. /dev/vda) can not be trusted. This boolean toggles this behavior. Setting it to true results in trusting the block device names provided by Cinder. The value of false results in the discovery of the device path based on its serial number and /dev/disk/by-id mapping and is the recommended approach.  If not set, will use the upstream default. |
| user-domain-name       | string  |           |Name of the user domain where you want to create your resources.|
| username               | string  |           |Username of a valid user set in keystone.|
