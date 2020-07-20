---
wrapper_template: "kubernetes/docs/base_docs.html"
markdown_includes:
  nav: "kubernetes/docs/shared/_side-navigation.md"
context:
  title: "IPv6"
  description: Using IPv6 with Charmed Kubernetes.
keywords: juju, network, networking
tags: [operating]
sidebar: k8smain-sidebar
permalink: ipv6.html
layout: [base, ubuntu-com]
toc: False
---

As of Kubernetes 1.19, support for IPv6 is in beta and dual-stack is in alpha.
Charmed Kubernetes can enable these by including IPv6 CIDRs in the `cidr`
config for the Calico charm and the `service-cidr` config for the Kubernetes
Master charm.  These can contain up to two comma-separated values, with the
first CIDR in the list being the preferred family for pods, or the default for
services.  You can override the `IPFamily` for a service when creating it.

<div class="p-notification--positive"><p markdown="1" class="p-notification__response">
<span class="p-notification__status">Note:</span>
Calico is the only CNI which supports IPv6 at this time.
</p></div>

## Example

You can use the following overlay file ([download it here](asset-ipv4-ipv6-overlay])
to enable IPv4 preferred dual-stack to the [charmed-kubernetes-calico][] bundle:

```yaml
description: Charmed Kubernetes overlay to enable IPv4-IPv6 dual-stack.
applications:
  calico:
    options:
      cidr: "192.168.0.0/16,fd00:c00b:1::/112"
  kubernetes-master:
    options:
      service-cidr: "10.152.183.0/24,fd00:c00b:2::/112"
  kubernetes-worker:
    resources: null
```

Once that is deployed, you can use the following spec ([download it
here](asset-nginx-dual-stack)) to run a dual-stack enabled nginx pod with an
IPv6 service in front of it:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginxdualstack
spec:
  selector:
    matchLabels:
      run: nginxdualstack
  replicas: 2
  template:
    metadata:
      labels:
        run: nginxdualstack
    spec:
      containers:
      - name: nginxdualstack
        image: rocks.canonical.com/cdk/diverdane/nginxdualstack:1.0.0
        ports:
        - containerPort: 80
---
apiVersion: v1
kind: Service
metadata:
  name: nginx6
  labels:
    run: nginxdualstack
spec:
  type: NodePort
  ipFamily: IPv6
  ports:
  - port: 80
    protocol: TCP
  selector:
    run: nginxdualstack
```

## Known Issues

Because of the beta / alpha feature status for IPv6 / dual-stack in Kubernetes,
and because of the fact that Juju does not officially support IPv6, there are
some things that don't work 100% and some limitations on how you can configure
IPv6. These will also vary depending on the underlying cloud provider.

### Juju

The following arise because Juju does not fully support IPv6:

* The charms require IPv4 on the underlying hosts, even when running a cluster
  in IPv6-only mode.

* By default, connections to the API server will use the IPv4 address even when
  running a cluster in IPv6-preferred or IPv6-only mode. This can be modified
  in the client config by hand or overridden via the `loadbalancer-ips` config.

* IPv6 NodePort listeners won't function on the master, though they will work
  on the worker units.

* Juju's `open-port` cannot be used to allow NodePort connections for IPv6.

### AWS

The following arise when using AWS as the underlying cloud provider:

* Kubernetes creates classic load balancers for LoadBalancer-type services,
  which do not support IPv6.

* Juju does not honor the "automatically assign IPv6 address" setting and
  creates instances without IPv6 addresses. You can attach IPv6 addresses
  after deploying with something like:

  ```bash
  for machine in $(juju status --format=json | jq -r '.machines|keys[]' | sort -n); do
      echo -n "Machine $machine: "
      instance="pending"
      while [[ "$instance" == "pending" ]]; do
          instance=$(juju status --format=json | jq -r '.machines["'"$machine"'"]."instance-id"')
      done
      interface=$(aws ec2 describe-instances --instance-id "$instance" --output text --query 'Reservations[*].Instances[*].NetworkInterfaces[*].NetworkInterfaceId')
      aws ec2 modify-instance-attribute --instance-id "$instance" --no-source-dest-check
      ipv6_addresses=$(aws ec2 describe-instances --instance-id "$instance" --output text --query 'Reservations[*].Instances[*].NetworkInterfaces[*].Ipv6Addresses')
      if [[ -n "$ipv6_addresses" ]]; then
          echo "$ipv6_addresses"
      else
          aws ec2 assign-ipv6-addresses --network-interface-id "$interface" --ipv6-address-count 1 --output text --query 'AssignedIpv6Addresses'
      fi
  done
  ```

### OpenStack

Overall OpenStack is pretty straightforward.  I only encountered one issue
which may be resolvable with some tweaks to the OpenStack environment:

* Neutron LBaaS didn't seem to work well with an IPv6 LB, but this may have
  been a configuration issue.


### MAAS

TBD
