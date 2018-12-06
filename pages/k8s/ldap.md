---
title: "LDAP | Canonical Distribution of Kubernetes&reg;"
keywords: quickstart
tags: [getting_started]
sidebar: k8smain-sidebar
permalink: ldap.html
layout: base
toc: False
summary: How to get Keystone deployed and related to Kubernetes in order to have a LDAP integration.
---
# Basic Authentication
By default, CDK will use basic authentication for client communications. This is just simple username and password authentication.
# Keystone
Keystone can be used for authentication and authorization if desired. This involves a few steps.

## Quickstart
### Keystone setup
Note that Keystone v3 is required by the webhook. It will NOT work with v2 of the Keystone auth.
If you just want to kick the tires, it's simple to get Keystone setup with juju.
Steps:
1) install Keystone, MySQL, and the openstack dashboard.
2) create a domain for Kubernetes
3) create a role for Kubernetes admins/users/viewers
4) create a Kubernetes project
5) create Kubernetes users

#### Install Keystone
Note that these instructions assume you are installing Queens, which comes by default in Ubuntu Bionic. If your login dashboard looks different than what is displayed, check the distribution of your install.

To deploy with Juju, you can use the following bundle(taken from [openstack base bundle](https://jujucharms.com/openstack-base):

```yaml
series: bionic
applications:
  keystone:
    charm: cs:keystone-283
    num_units: 1
    options:
      openstack-origin: cloud:bionic-rocky
      worker-multiplier: 0.25
      preferred-api-version: 3
  mysql:I wouldn't be against a config option for 
    charm: cs:percona-cluster-269
    num_units: 1
    options:
      innodb-buffer-pool-size: 256M
      max-connections: 1000
  openstack-dashboard:
    charm: cs:openstack-dashboard-266
    num_units: 1
    expose: true
    options:
      openstack-origin: cloud:bionic-rocky
relations:
- - keystone:shared-db
  - mysql:shared-db
- - openstack-dashboard:identity-service
  - keystone:identity-service
- - openstack-dashboard:shared-db
  - mysql:shared-db
- - keystone:identity-credentials
  - kubernetes-master:keystone-credentials
```

Save this as `keystone.yaml` and deploy with:

```bash
juju deploy ./keystone.yaml
```

Note that Keystone will need to be reachable from the machine you're running kubectl on in order for the Keystone auth to work. The client binary reaches out to the Keystone server directly to authenticate and get an authorization token, which is presented to the Kubernetes API server. On a public cloud provider, this is as easy as `juju expose keystone` and `juju expose openstack-dashboard`, but please consider the security implications of exposing your production servers.

#### Create the domain for Kubernetes
[[https://github.com/juju-solutions/bundle-canonical-kubernetes/blob/mwilson/adding-keystone-images/docs/images/add_domain.png]]
After creating, be sure to set the domain context so users and roles are added to the proper domain
[[https://github.com/juju-solutions/bundle-canonical-kubernetes/blob/mwilson/adding-keystone-images/docs/images/set_domain_context.png]]

#### Create a role for Kubernetes
[[https://github.com/juju-solutions/bundle-canonical-kubernetes/blob/mwilson/adding-keystone-images/docs/images/create_role.png]]
Repeat the process for `k8s-viewers` and `k8s-users` if desired. These values match with the `keystone-policy` configuration option on the kubernetes-master charm.

#### Create project for Kubernetes
[[https://github.com/juju-solutions/bundle-canonical-kubernetes/blob/mwilson/adding-keystone-images/docs/images/create_project.png]]
As with the roles, the project name must match the value in the `keystone-policy` configuration option on the kubernetes-master charm.

#### Create a user for Kubernetes
[[https://github.com/juju-solutions/bundle-canonical-kubernetes/blob/mwilson/adding-keystone-images/docs/images/create_user.png]]
Ensure the user is added to the project created above.

### Kubernetes setup
1. `juju deploy canonical-kubernetes`
2. `juju relate kubernetes-master keystone`
3. Grab a coffee if you deployed Kubernetes. If just relating, it will only take a few minutes to settle. This can be monitored with `watch --color juju status --color`.
4. `juju scp kubernetes-master/0:config ~/.kube/config`
5. `juju scp kubernetes-master/0:kube-keystone.sh ~/kube-keystone.sh`
6. Edit ~/kube-keystone.sh to suit the user.
7. `source ~/kube-keystone.sh`
8. `sudo snap install kubectl` (1.11 or greater is needed)
8. `sudo snap install client-keystone-auth`

Keystone should now be working for Kubernetes.

## Notes
The kubectl config created by the kubernetes-master charm will have the address it uses to connect to Keystone. If the machine that is used with kubectl is unable to reach that address, the file ~/.kube/config will require editing to alter the public address of the Keystone server.

The client binary client-keystone-auth is currently only available as a snap. Another option is to build from the source located in the [cloud-provider-openstack](https://github.com/kubernetes/cloud-provider-openstack/releases) github repository.

## Details
External webhook auth on Kubernetes involves the API server contacting a REST endpoint. In Keystone's case, this is a pod running in the Kubernetes cluster. That pod then contacts the Keystone server to authenticate the user and returns information back to the API server.

### Authentication vs Authorization
There is a distinction between authentication and authorization and it is worth some discussion. Authentication is all about who a user is. Authorization deals with what a user is allowed to do on the cluster. Keystone can handle authentication only or both authentication and authorization.

By default, CDK will setup only authentication with Keystone. This allows the use of other methods such as RBAC for authorization but using Keystone for authentication. In other words, usernames will come from Keystone, but what they can do in the cluster is controlled by another system. This can be changed to also use Keystone for authorization in the configuration for kubernetes-master with the command `juju config kubernetes-master enable-keystone-authorization=true`. When authorization is enabled, the policy is defined in the config. The easiest thing to do is to create a file with the policy desired and then run `juju config kubernetes-master keystone-policy=$(cat policy.yaml)` The default policy is:
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
The format is very similar to RBAC and is a mapping of Keystone users and groups to permissions on the cluster. The options for the match portion of the policy file are user, project, role, and group. More information can be found on the [cloud-provider-openstack documentation](https://github.com/kubernetes/cloud-provider-openstack/blob/master/docs/using-keystone-webhook-authenticator-and-authorizer.md).

#### A note on authorization

Kubernetes uses multiple authorization plugins. They are defined with `juju config kubernetes-master authorization-mode='Option1,Option2,Option3'` and Kubernetes will ask each plugin in order about the incoming request. The plugins can return authorized, denied, or unknown. The first plugin that returns authorized or denied will be the result for the incoming request. This means that order matters for the plugin list and that multiple authorization plugins can be used to define the entire policy for the cluster. For most deployments, it is impractical to create user accounts for all the services, so RBAC pairs well with Keystone. Specifically, the typical deployment including Keystone will use `juju config kubernetes-master authorization-mode='Node,Webhook,RBAC'`.

Node is necessary to ensure kubelet can communicate to the API server, Keystone for most user authentication, and finally, RBAC to pick up accounts for things like the metrics server and the keystone authorization pod itself. Note that the token-based authentication will still work as well. The original context in the kubeconfig, juju-cluster, will still work to communicate with the cluster.

## Dashboard access with Keystone users.
Since the Kubernetes API server can only validate tokens, the dashboard login requires a token. A token can be retrieved with the function embedded in the kube-keystone.sh script. After sourcing the script from the  instructions above, simply type `get_keystone_token` on the command prompt and a login token will be printed.
Login would then be done via the token option:

[[https://github.com/juju-solutions/bundle-canonical-kubernetes/blob/mwilson/adding-keystone-images/docs/images/kubernetes_dash.png]]
# LDAP via Keystone
Keystone has the ability to use LDAP for authentication. The Keystone charm is related to the Keystone-LDAP subordinate charm in order to support LDAP. Read about the steps involved on the [keystone-ldap charm page](https://jujucharms.com/keystone-ldap)

# Troubleshooting

If things don't work, there usually isn't an obvious cause. Testing the steps is important to determine the cause of the problem.

## Can you communicate with Keystone and get an authorization token.
First is to verify that Keystone communication works from both your client and the kubernetes-worker machines. The easiest thing to do here is to copy the kube-keystone.sh script to the machines of interest from kubernetes-master with `juju scp kubernetes-master/0:kube-keystone.sh .`, edit the script to include you credentials, `source kube-keystone.sh` and then run `get_keystone_token`. This will produce a token from the Keystone server. If that isn't working, check firewalls settings and your Keystone server. Note that the kube-keystone.sh script could be overwritten, so it is a best practice to make a copy somewhere and use that.

## Are the pods for Keystone authentication up and running properly
The Keystone pods live in the kube-system namespace and read a configmap from Kubernetes for the policy. Check to make sure they are running:

```bash
$ kubectl -n kube-system get po
NAME                                              READY   STATUS    RESTARTS   AGE
k8s-keystone-auth-5c6b7f9b7c-mvvkx                1/1     Running   0          21m
k8s-keystone-auth-5c6b7f9b7c-q2jfq                1/1     Running   0          21m
```

Check the logs of the pods for errors:

```bash
$ kubectl -n kube-system logs k8s-keystone-auth-5c6b7f9b7c-mvvkx
W1121 05:02:02.878988       1 config.go:73] Argument --sync-config-file or --sync-configmap-name missing. Data synchronization between Keystone and Kubernetes is disabled.
I1121 05:02:02.879139       1 keystone.go:527] Creating kubernetes API client.
W1121 05:02:02.879151       1 client_config.go:548] Neither --kubeconfig nor --master was specified.  Using the inClusterConfig.  This might not work.
I1121 05:02:02.893499       1 keystone.go:544] Kubernetes API client created, server version v1.12
I1121 05:02:02.998944       1 keystone.go:93] ConfigMaps synced and ready
I1121 05:02:02.999045       1 keystone.go:101] Starting webhook server...
I1121 05:02:02.999262       1 keystone.go:155] ConfigMap created or updated, will update the authorization policy.
I1121 05:02:02.999459       1 keystone.go:171] Authorization policy updated.
```

## Is the configmap with the policy correct

Check the configmap contents. The pods logs above would complain if the yaml isn't valid, but make sure it matches what you expect.

```bash
$ kubectl -n kube-system get configmap k8s-auth-policy -o=yaml
apiVersion: v1
data:
  policies: |
    [
      {
        "resource": {
          "verbs": ["get", "list", "watch"],
          "resources": ["pods"],
          "version": "*",
          "namespace": "default"
        },
        "match": [
          {
            "type": "user",
            "values": ["admin"]
          },
        ]
      }
    ]
kind: ConfigMap
metadata:
  annotations:
    kubectl.kubernetes.io/last-applied-configuration: |
      {"apiVersion":"v1","data":{"policies":"[\n  {\n    \"resource\": {\n      \"verbs\": [\"get\", \"list\", \"watch\"],\n      \"resources\": [\"pods\"],\n      \"version\": \"*\",\n      \"namespace\": \"default\"\n    },\n    \"match\": [\n      {\n        \"type\": \"user\",\n        \"values\": [\"admin\"]\n      },\n    ]\n  }\n]\n"},"kind":"ConfigMap","metadata":{"annotations":{},"labels":{"k8s-app":"k8s-keystone-auth"},"name":"k8s-auth-policy","namespace":"kube-system"}}
  creationTimestamp: 2018-11-21T02:38:12Z
  labels:
    k8s-app: k8s-keystone-auth
  name: k8s-auth-policy
  namespace: kube-system
  resourceVersion: "16736"
  selfLink: /api/v1/namespaces/kube-system/configmaps/k8s-auth-policy
  uid: 7dc0842b-ed36-11e8-82e1-06d4a9ac9e06
```
## Check the service and endpoints

Verify the service exists and has endpoints

```bash
$ kubectl get svc -n kube-system
NAME                        TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)             AGE
heapster                    ClusterIP   10.152.183.49    <none>        80/TCP              136m
**k8s-keystone-auth-service   ClusterIP   10.152.183.200   <none>        8443/TCP            105m**
kube-dns                    ClusterIP   10.152.183.218   <none>        53/UDP,53/TCP       137m
kubernetes-dashboard        ClusterIP   10.152.183.142   <none>        443/TCP             136m
metrics-server              ClusterIP   10.152.183.245   <none>        443/TCP             136m
monitoring-grafana          ClusterIP   10.152.183.2     <none>        80/TCP              136m
monitoring-influxdb         ClusterIP   10.152.183.172   <none>        8083/TCP,8086/TCP   136m
$ kubectl -n kube-system get ep
NAME                        ENDPOINTS                       AGE
heapster                    10.1.20.4:8082                  136m
**k8s-keystone-auth-service   10.1.20.5:8443,10.1.32.4:8443   105m**
kube-controller-manager     <none>                          136m
kube-dns                    10.1.31.6:53,10.1.31.6:53       136m
kube-scheduler              <none>                          136m
kubernetes-dashboard        10.1.31.3:8443                  136m
metrics-server              10.1.32.2:443                   136m
monitoring-grafana          10.1.31.2:3000                  136m
monitoring-influxdb         10.1.31.2:8086,10.1.31.2:8083   136m
```

## Attempt to authenticate directly to the service

Use a token to auth with the Keystone service directly:
```bash
$ cat <<EOF | curl -ks -XPOST -d @- https://10.152.183.200:8443/webhook | python -mjson.tool
{
  "apiVersion": "authentication.k8s.io/v1beta1",
  "kind": "TokenReview",
  "metadata": {
    "creationTimestamp": null
  },
  "spec": {
    "token": "$(get_keystone_token)"
  }
}
EOF

{
    "apiVersion": "authentication.k8s.io/v1beta1",
    "kind": "TokenReview",
    "metadata": {
        "creationTimestamp": null
    },
    "spec": {
        "token": "gAAAAABb9Yeel_62KoSb_fAL6RPMpGZ4-4y5RLqXq5YdY3PcIKpuIcZ8PoVPhQtHOR7fiPYpFQX_pAUZJ4yngSE_WbJeuX8c-pl5WgStNImmkH3sEvQ5nSfimGhQSH-k5ydCBhcor87AeN7dOS-X6zHMRrcyvnZffQ"
    },
    "status": {
        "authenticated": true,
        "user": {
            "extra": {
                "alpha.kubernetes.io/identity/project/id": [
                    ""
                ],
                "alpha.kubernetes.io/identity/project/name": [
                    ""
                ],
                "alpha.kubernetes.io/identity/roles": [],
                "alpha.kubernetes.io/identity/user/domain/id": [
                    "e1cbddf1b75340499109f0b88b28d472"
                ],
                "alpha.kubernetes.io/identity/user/domain/name": [
                    "admin_domain"
                ]
            },
            "groups": [
                ""
            ],
            "uid": "432f311e7eb94689b10aee03293ab030",
            "username": "admin"
        }
    }
}

Note that you need to change the IP address above to the address of your k8s-keystone-auth-service. This will talk to the webhook and verify that the token is valid and return information about the user.

## API server

Finally, communication between the API server and the Keystone service is verified. The easiest thing to do here is to look at the log for the API server for interesting information such as timeouts or errors with the webhook. `juju run --unit kubernetes-master/0 -- journalctl -u snap.kube-apiserver.daemon.service`