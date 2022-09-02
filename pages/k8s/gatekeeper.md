[OPA gatekeeper](https://open-policy-agent.github.io/gatekeeper/website/docs/) is an open source, general-purpose policy engine that enables unified, context-aware policy enforcement.

Gatekeeper is a validating webhook that enforces CRD-based policies executed by [Open Policy Agent](https://www.openpolicyagent.org/). [Policies](https://open-policy-agent.github.io/gatekeeper/website/docs/howto#constraint-templates) are defined in a language called [rego](https://www.openpolicyagent.org/docs/latest/policy-language/). Incoming requests that try to create or alter a resource that violates any of these policies will be rejected.

In addition to admission, Gatekeeper offers audit functionality, which allows administrators to see which resources are currently violating any given policy.

##  Deployment

The gatekeeper webhook and audit services exist in separate charms, you should deploy both of them. To deploy the operators you will first need a Kubernetes model in Juju. Add your Kubernetes as a cloud to your Juju controller:

```console
juju add-k8s k8s-cloud --controller $(juju switch | cut -d: -f1)
```

Next, create a new Kubernetes model:

```console
juju add-model gatekeeper-system k8s-cloud
```

Then you can deploy the Gatekeeper charms:

```console
juju deploy ch:gatekeeper-controller-manager
juju deploy ch:gatekeeper-audit
```

### Note: Using RBAC

If using RBAC, you must deploy the charms using the `--trust` flag as the charm needs permissions in order to create the necessary resources:

```console
juju deploy --trust ch:gatekeeper-controller-manager
juju deploy --trust ch:gatekeeper-audit
```

## Policies

[Policies](https://open-policy-agent.github.io/gatekeeper/website/docs/howto#constraint-templates) are defined as `ConstraintTemplate` CRDs in a language called [rego](https://www.openpolicyagent.org/docs/latest/policy-language/). Constraints are then used to inform Gatekeeper that the admin wants a ConstraintTemplate to be enforced, and how.

To get a list of the constraints run:

```console
kubectl get constraints
```

Or with the juju command:
```console
juju run-action {unit_name} -m {model_name} --wait list-violations
```

And then to get the violations for a specific constraint run:
```console
juju run-action {unit_name} -m {model_name} --wait get-violation constraint-template={constraint_template} constraint={constraint}
```

## Configuration

Not much needs to be configured when running OPA gatekeeper. All configurations available are related to optimizing the auditting:
```yaml
audit-chunk-size:
  default: 500
  description: |
    Lower chunk size can reduce memory consumption of the auditing Pod but
    can increase the number requests to the Kubernetes API server.
audit-interval:
  default: 60
  description: Interval between the audits, to disable the interval set `audit-interval=0`
constraint-violations-limit:
  default: 20
  description: |
    The number of violations that will be reported, If the number of current violations
    is greater than this cap, the excess violations will not be reported but they
    will be included in the totalViolations count
```

# Metrics
Both charms provide out of the box integration with the [prometheus-k8s](https://charmhub.io/prometheus-k8s) and the [grafana-agent-k8s](https://charmhub.io/grafana-agent-k8s) charms.

If you have those two charms deployed, you can integrate them with gatekeeper simply by running:

```bash
juju relate grafana-agent-k8s gatekeeper-controller-manager
juju relate grafana-agent-k8s:send-remote-write prometheus-k8s:receive-remote-write
```

This will provide you with metrics like how many requests were denied, how many were processed, how many violations exist in the cluster, etc.

## Reconciliation

The gatekeeper charms manage the same Kubernetes resources(roles, crds, etc.). If for some reason you wish to delete one of the two charms while keeping the other you should be very careful, as it will cause all of the resources to be deleted.

In that scenario you will need to reconcile (recreate) the resources by running:

```console
juju run-action {unit_name} -m {model_name} reconcile-resources --wait
```
> :warning:  This will cause all the policies to be deleted as well, which means you will have to reapply them.

## Test the Gatekeeper charm

To test the gatekeeper charms you can try applying the test policy available on the charms' repo:

```console
kubectl apply -f https://raw.githubusercontent.com/charmed-kubernetes/opa-gatekeeper-operators/main/docs/policy-example.yaml
kubectl apply -f https://raw.githubusercontent.com/charmed-kubernetes/opa-gatekeeper-operators/main/docs/policy-spec-example.yaml
```

This policy will require all namespaces to have the label `gatekeeper=True`, creating a new ns without that should fail:

```console
kubectl create ns test
```
...should return...

```bash
Error from server (Forbidden): admission webhook "validation.gatekeeper.sh" denied the request: [ns-must-have-gk] you must provide labels: {"gatekeeper"}
```

After a while you should also be able to see violations of the policy from the
existing resources. For example:

```console
kubectl get constraints
```
... will return something similar to:

```
NAME              ENFORCEMENT-ACTION   TOTAL-VIOLATIONS
ns-must-have-gk                                6
```
