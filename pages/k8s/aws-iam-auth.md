---
wrapper_template: "base_docs.html"
markdown_includes:
  nav: "shared/_side-navigation.md"
context:
  title: "AWS-IAM on Charmed Kubernetes"
  description: Using AWS credentials to authenticate and authorize on Charmed Kubernetes
keywords: aws, auth, iam
tags: [install]
sidebar: k8smain-sidebar
permalink: aws-iam-auth.html
layout: [base, ubuntu-com]
toc: False
---

## AWS IAM

[AWS IAM](https://aws.amazon.com/iam/) credentials can be used for
authentication and authorization on your Charmed Kubernetes cluster without
regard to where it is hosted. The only requirement is that the client
machine running `kubectl` and the master nodes are able to reach AWS in
order to get and validate tokens.


### Installing

The subordinate charm [aws-iam-authenticator](aws-iam-charm)
and some relations are all that are required. This can be added with the
following overlay([download it here][asset-aws-iam-overlay]):
```yaml
applications:
  aws-iam:
    charm: cs:~containers/aws-iam
relations:
  - ['aws-iam', 'kubernetes-master']
  - ['aws-iam', 'easyrsa']
```

To use this overlay with the **Charmed Kubernetes** bundle, it is specified
during deploy like this:

```bash
juju deploy charmed-kubernetes  --overlay ~/path/aws-iam-overlay.yaml
```

### User Configuration

The [aws-iam-authenticator](aws-iam-authenticator-github) is configured via
[Custom Resource Definition or CRD](k8s-crd-docs)s. These resource definitions map an AWS IAM role or user
to a [Kubernetes RBAC](k8s-rbac-docs) user or group. This means that
authentication happens via AWS IAM credentials, but authorization depends
on standard Kubernetes RBAC rules. The CRD for this mapping is called an
IAMIdentityMapping and looks something like this:
```yaml
apiVersion: iamauthenticator.k8s.aws/v1alpha1
kind: IAMIdentityMapping
metadata:
  name: kubernetes-admin
spec:
  # Arn of the User or Role to be allowed to authenticate
  arn: arn:aws:iam::xxxxx:role/k8s-view-role
  # Username that Kubernetes will see the user as, this is useful for setting
  # up allowed specific permissions for different users
  username: john
  # Groups to be attached to your users/roles. For example `system:masters` to
  # create cluster admin, or `view` for view only,
  groups:
  - view
```

### Using AWS-IAM with kubectl

#### Download aws-iam-authenticator

The aws-iam-authenticator binary needs to be installed on the machine that is
running kubectl. This is executed by kubectl in order to log in and get a token,
which is then passed to the Kubernetes API server. You can find the binary
on the (aws-iam-authenticator releases page)[aws-iam-authenticator-releases].

#### Updating kubectl config

In order to use the [aws-iam-authenticator](aws-iam-authenticator-github) with
kubectl, an updated config file is needed. The config file written to the
kubernetes-master unit will have a user named aws-iam-user that uses the
aws-iam-authenticator client binary and a context named aws-iam-authenticator.
First, copy the config:

```bash
juju scp kubernetes-master/0:config ~/.kube/config
```

The config file will need to be edited in order to add the desired arn
for authentication. Information about this can be found on the
[aws-iam-authenticator documentation](aws-iam-authenticator-config).

The context that uses aws-iam-authenticator can be selected with:

```bash
kubectl config use-context aws-iam-authenticator
```

### A note about authorization

The AWS-IAM charm can be used for authentication only or can be used in an
RBAC-enabled cluster to authorize users as well. If the charm is related to
a Charmed Kubernetes cluster without RBAC enabled, any valid AWS IAM
credential that can assume a role specified in the IAMIdentityMapping
CRD will be able to do any commands against the cluster. If RBAC is enabled,
the user will have the permissions of the user defined in the
IAMIdentityMapping CRD.

### Upgrading the AWS-IAM charm

The AWS IAM charm is not specifically tied to the version of
Charmed Kubernetes installed and may generally be upgraded at any
time with the following command:

```bash
juju upgrade-charm aws-iam
```

### Troubleshooting

If you have any specific problems with the aws-integrator, you can report bugs on
[Launchpad][bugs].

The aws-integrator charm makes use of IAM accounts in AWS to perform actions, so
useful information can be obtained from [Amazon's CloudTrail][cloudtrail], which logs
such activity.

<!-- LINKS -->

[asset-aws-iam-overlay]: https://raw.githubusercontent.com/charmed-kubernetes/kubernetes-docs/master/assets/aws-iam-overlay.yaml
[aws-iam-charm]: https://jaas.ai/u/containers/aws-iam-authenticator
[aws-aim-authenticator-github]: https://github.com/kubernetes-sigs/aws-iam-authenticator
[k8s-crd-docs]: https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/
[k8s-rbac-docs]: https://kubernetes.io/docs/reference/access-authn-authz/rbac/
[cloudtrail]: https://console.aws.amazon.com/cloudtrail/
[quickstart]: /kubernetes/docs/quickstart
[bugs]: https://bugs.launchpad.net/aws-iam
[aws-iam-authenticator-config]: https://github.com/kubernetes-sigs/aws-iam-authenticator#4-set-up-kubectl-to-use-authentication-tokens-provided-by-aws-iam-authenticator-for-kubernetes
