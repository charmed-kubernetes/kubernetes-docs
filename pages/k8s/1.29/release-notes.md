
---
wrapper_template: "templates/docs/markdown.html"
markdown_includes:
  nav: "kubernetes/docs/shared/_side-navigation.md"
context:
  title: "1.29 Release notes"
  description: Release notes for Charmed Kubernetes
keywords: kubernetes, release, notes
tags: [news]
sidebar: k8smain-sidebar
permalink: 1.29/release-notes.html
layout: [base, ubuntu-com]
toc: False
---
# 1.29

### February 12, 2024 - `charmed-kubernetes --channel 1.29/stable`

The release bundle can also be [downloaded here](https://raw.githubusercontent.com/charmed-kubernetes/bundle/main/releases/1.29/bundle.yaml).

## What's new
### aws-integrator
Test storage and provider-id via integration testing
s/juju scp/juju ssh/ for fetching kubeconfig
Update tests/data/bind_pvc.yaml
Co-authored-by: Kevin W Monroe <kevin.monroe@canonical.com>
Update tests/data/charm.yaml
Co-authored-by: Kevin W Monroe <kevin.monroe@canonical.com>
Merge pull request #50 from juju-solutions/akd/modernize-integration-tests
Test storage and provider-id via integration testing
### calico
LP#2037236 Calico is ignoring juju network binding for cni (#104)
* Address IP autodetection method
* Fix unit tests
* Fix lint
* Update src/charm.py
Co-authored-by: Adam Dyess <adam.dyess@canonical.com>
---------
Co-authored-by: Adam Dyess <adam.dyess@canonical.com>
### canal
Update build-canal-resources.sh (#82)
### coredns
Disallow charm from being deployed to non-k8s models (#37)
Update referenced coredns image to 1.11.1 (#38)
* Update referenced coredns image to 1.11.1
* switch to using rocks image as the upstream source
* Use rocks.canonical.com for k8s model images
* Produces a tox env to update the charm's image resource
* default image uploads to rocks.canonical.com using local credentials
Use isort, codespell, and ruff for linting (#39)
* Use isort, codespell, and ruff for linting
* Add pyproject.toml to configure ruff
---------
Co-authored-by: Mateo Florido <mateo.florido@canonical.com>
Co-authored-by: Mateo Florido <32885896+mateoflorido@users.noreply.github.com>
### docker-registry
Use Python 3.6 for tests
The test suite currently uses an f-string, which are only supported
beginning with Python 3.6. On some systems, tox attempts to run the
tests using Python 3.5, causing a test failure from invalid syntax. This
change fixes the issue by ensuring that tox always uses Python 3.6.
Add wheelhouse.txt
This is required for building and deploying the charm on newer versions
of charmcraft and/or Ubuntu.
Allow enabling prometheus metrics
The docker registry can be configured to provide prometheus metrics, but
the charm currently does not have the option to enable this option. This
change adds the ability to enable this option, using the
`prometheus-metrics` and `debug-port` charm configuration options. There
is no way to only enable prometheus metrics, so enabling the
configuration option also enables other debug URLs such as /debug/vars.
It is expected that the other debugging URLs will be less relevant to
users of this charm, and so `prometheus-metrics` was chosen as the name
of the configuration option.
This change also adds a small bit of fanciness by updating the ports
displayed in the output of `juju status` dynamically based on their
values and the value of the `prometheus-metrics` option.
Fixes https://bugs.launchpad.net/layer-docker-registry/+bug/2034475
Use python3 for tests
The unit tests for this project use GitHub Actions, which install a
single version of Python during execution. The previous change to use
python 3.6 for tests does not work in such an environment, and so this
commit undos that one.
Fix issues from review
Merge pull request #67 from shanepelletier/allow-enabling-prometheus-metrics
Allow enabling prometheus metrics
Merge remote-tracking branch 'upstream/master' into main
### etcd
Upgrade tests to juju 3.1 (#211)
* Upgrade tests to juju 3.1
* Update test_etcd.py
use model destroy_unit()
* Stop listening on 127.0.0.1:4001 with http (#212)
* Stop listening on 127.0.0.1:4001 with http
* Ensure the restore action uses the secure endpoint as well
* linting
* Update config.yaml
Co-authored-by: Kevin W Monroe <kevin.monroe@canonical.com>
---------
Co-authored-by: Kevin W Monroe <kevin.monroe@canonical.com>
---------
Co-authored-by: Kevin W Monroe <kevin.monroe@canonical.com>
### kube-ovn
Reenable grafana (#42)
* Reenable grafana
* Move grafana/prom tests to end to see if that helps
* Put multus as last test
* quiet the progress bars from curl
* swap to stable charms for prometheus-k8s and grafana-k8s
* reduced complexity of integration tests setup to install the entire k8s-model at once
* simplify tear down of tests
* speed up deployment of k8s and machine models
* Copy charmcraft log to debug artifact
---------
Co-authored-by: Stone Preston <stone.preston@canonical.com>
Co-authored-by: Mateo Florido <32885896+mateoflorido@users.noreply.github.com>
Co-authored-by: Adam Dyess <adam.dyess@canonical.com>
Update to kube-ovn v1.11.10 (#47)
Update to kube-ovn v1.12.0 (#48)
Upgrade kube-ovn via update script (and tox env) (#49)
Update to kube-ovn v1.12.2 (#50)
Update to kube-ovn v1.12.3 (#51)
### kubeapi-load-balancer
Convert KubeAPI Load Balancer to the ops framework (#26)
* Convert KubeAPI Load Balancer to ops
* Add .wokeignore
* Fix lint
* Update .gitignore
Co-authored-by: Adam Dyess <adam.dyess@canonical.com>
* Update tests/integration/test_charm.py
Co-authored-by: Adam Dyess <adam.dyess@canonical.com>
* Address code review comments
* `/s/architecture/architectures`
* Use `kubernetes-core` bundle in integration tests
* Address code review comments
---------
Co-authored-by: Adam Dyess <adam.dyess@canonical.com>
remove layer.yaml (#27)
Enhance `certificates` relation check. (#28)
Fix LoadBalancer addresses (#29)
[LP#1948019] Add configuration options for Nginx directives (#31)
* Add configuration options for directives
* Update config.yaml
* Apply suggestions from code review
Co-authored-by: Adam Dyess <adam.dyess@canonical.com>
* Refactor `nginx` syntax logic
* Fix Format
* Fix docstrings
* Use new configs
---------
Co-authored-by: Adam Dyess <adam.dyess@canonical.com>
Install `nginx-prometheus-exporter`  and export metrics over `cos` (#30)
* Install nginx-prometheus-exporter to collect nxginx metrics and export over cos relation
* Simplify unit tests
* add nginx alert rules
Add `ConfigurationContext` class (#32)
* Add ConfigurationContext class
* Apply suggestions from code review
Co-authored-by: Adam Dyess <adam.dyess@canonical.com>
* Fix oddities
---------
Co-authored-by: Adam Dyess <adam.dyess@canonical.com>
use http context keys in config description (#33)
Fix failure in hacluster integration (#34)
### kubernetes-control-plane
Throw it all away
Initial ops charm (#292)
* charmcraft init
* Initial implementation
* make linters happy
* Fix unit tests
* Add github actions
* Use the right folder for github actions lol
* Pin python versions
* Fix mangled github action
* Test with juju 3.1
* Allow builds on 20.04
* Collect charmcraft logs
* Update requirements
Handle certificates relation (#293)
* Handle certificates relation
* Fix integration juju3 snap confinement issue
* Fix requirements
Configure control plane services (#297)
* Configure control plane services
* Update requirements.txt
* Update auth-webhook API version
Co-authored-by: Kevin W Monroe <kevin.monroe@canonical.com>
---------
Co-authored-by: Kevin W Monroe <kevin.monroe@canonical.com>
Add container-runtime and cni endpoints (#299)
* Add container-runtime interface
* Add cni interface
* Update requirements.txt
Configure node services (#303)
* Add sysctl config
* Add kubelet and kube-proxy
* Update requirements.txt
Implement kube-control and loadbalancer relations (#304)
* Add kube-control relation
* Add loadbalancer relations, refactor endpoint handling
* Fix lint issue
* Fix bug in no-loadbalancer case
* Update requirements.txt
Add cdk-addons and kube-dns relation (#305)
* Add cdk-addons
* Add kube-dns relation
* Clean up per review
Co-authored-by: Adam Dyess <adam.dyess@canonical.com>
* Update requirements.txt
---------
Co-authored-by: Adam Dyess <adam.dyess@canonical.com>
provide support for the external-cloud-provider relation (#307)
* provide support for the external-cloud-provider relation
* use pending branch for kubernetes-snaps
* use fqdn hostname for aws instances
* use latest charm-lib-kubernetes-snaps
Implement COS integration (#306)
* Implement Observability
* Cleanup
* Add `cosl` to `requirements.txt`
* Improve CR/CRB
* Remove unused tokens
* Change COS Token user:group
* Fix lint
* Create new `cos_integration` module
* Add docstrings
Add `cni-plugins` resource (#309)
* Add `cni-plugins` resource
* Remove script_commit from build-cni-resources
* Download releases from GH instead of local building them
* Fix resource naming
* Address code review
Label control-plane nodes (#310)
* Label control-plane nodes
* Apply node-labels to the control-plane nodes
* Unit tests should be agnostic from which cloud they are run
* Update requirements.txt
Update AlertManager rules (#312)
Change Kubeconfig for LabelMaker (#314)
Fix Metrics Endpoints (#313)
* Fix Metrics Endpoints
* Update src/cos_integration.py
* Fix endpoints and metrics relabeling
* Use cluster-name
* Rollback `kubernetes-snaps` pin
---------
Co-authored-by: Adam Dyess <adam.dyess@canonical.com>
Implement controlled upgrades (#311)
* Implement controlled upgrades
* Offload upgrade handler
* Update requirements
---------
Co-authored-by: Adam Dyess <adam.dyess@canonical.com>
Fix apiserver forbidden to access kubelet API (#315)
Add hacluster integration (#308)
* Add hacluster integration
* Use interface-hacluster from fork
Co-authored-by: Adam Dyess <adam.dyess@canonical.com>
* Ensure config_addrs values are never falsey
Co-authored-by: Adam Dyess <adam.dyess@canonical.com>
---------
Co-authored-by: Adam Dyess <adam.dyess@canonical.com>
Fix AlertManager expr (#316)
* Fix AlertManager expr
* Create Diff Patch
Pin config to 1.29/stable snaps and tests to 1.29/stable charms (#319)
Add Prometheus Rule (#320)
Pin requirements to release_1.29 branches
[LP#2046508]  Set application workload version based on the version of kubelet (#324)
* Set application workload version based on the version of kubelet installed
* Update tests/integration/test_k8s_control_plane_charm.py
* move set_workload_status to update_status hook
Adds kube-system unit status when the unit is stable (#325)
* Adds kube-system unit status when the unit is stable
* fix regex in kube-system check to look for digits followed by a single space
[LP#2048683] Only use FQDN node names on AWS when using its cloud-provider (#326)
* Only use FQDN node names on AWS when using its cloud-provider
* Add deprecated aws integration, can be unrelated after upgrade
LP 2049953: adding coordinator peer interface (#328)
* adding coordinator peer interface
* lint fix; refactor peer interfaces
Include lb-consumer relation's addresses when requesting certificates (#327)
* Include lb-consumer relation's addresses when requesting certificate sans
* Resolve linting issues
* Apply review comments
* instrument better logs for a reconciled control-plane that still has failures
Don't call snap list on the machine running unit tests (#323)
enforce juju >= 3.1 (#329)
lp:2049953 include relations needed for upgrade from < 1.29
lp:2048692 include relations needed for upgrade from < 1.29 (wrong bug previously)
### kubernetes-dashboard
Integrate Ingress v2
Change certificate structure
Change svc port
Change fqdns
Add strip prefix
Add Integration test
Add MetalLB addon
Change ClusterIP test port
Assert Value for both possible fqdns
Fix FMT
Rollback Port changes
Merge pull request #81 from charmed-kubernetes/m/ingress
Implement Ingress integration
### kubernetes-e2e
Upgrade tests to use juju 3.1 (#30)
* Upgrade tests to use juju 3.1
* Use upgraded juju action
### kubernetes-worker
Throw it all away
Initial ops charm (#145)
* charmcraft init
* Initial implementation
* Make linters happy
* Fix unit test
* Add github actions
* Fix mangled github action
* Test with juju 3.1
* Allow builds on 20.04
* Revert "Allow builds on 20.04"
This reverts commit f3aeec081d66704fc7084e5211cdfc7957a87dd2.
* Update requirements links
Synchronize `Kubernetes Worker` with `Kubernetes Control Plane` (#150)
* Implement integrations
* Update integration test
* Update config.yaml
* Apply suggestions from code review
Co-authored-by: Adam Dyess <adam.dyess@canonical.com>
---------
Co-authored-by: Adam Dyess <adam.dyess@canonical.com>
Support for external-cloud-providers (#152)
Implement COS integration (#151)
* Implement COS integration
* Add `cosl` to `requirements.txt`
* Use new COS RBAC group
* Better handle `tokens` integration
* Make `tokens` integration optional
* Use \`get_node_name\`
Add `cni-plugins` resource (#153)
* Add `cni-plugins`
* Fix overlay
* Address code review
* Remove `prime`
Fix Metrics Endpoints (#155)
* Fix Metrics Endpoints
* Update src/charm.py
---------
Co-authored-by: Adam Dyess <adam.dyess@canonical.com>
Add `cluster` name label (#156)
* Fix metrics labels
* Use cluster-name
Implement controlled upgrades (#154)
* Implement controlled upgrades
* Offload upgrade handler
* Update requirements
Add ingress and labels configs (#157)
* Add nginx-ingress-controller
* Add labels config
Pin requirements to release_1.29 branches
Pin config to 1.29/stable snaps and tests to 1.29/stable charms
[LP#2046508] Set application workload version based on the version of kubelet (#159)
* Set application workload version based on the version of kubelet installed
* Update tests/integration/test_k8s_worker_charm.py
update the unit's workload version on update status (#160)
[LP#2048683] Only use FQDN node names on AWS when using its cloud-provider (#161)
* Only use FQDN node names on AWS when using its cloud-provider
* Add deprecated aws integration, can be unrelated after upgrade
adding coordinator peer interface (#162)
enforce juju >= 3.1 (#163)
blacken src
### metallb
Pull from functional Diataxis Discourse posts back to source of truth from repo (#38)
### openstack-integrator
[LP#1940328] Add loadbalancer relation named lb-consumers (#5)
* Replace loadbalancer relation with lb-consumers relation
* re-introduce deprecated loadbalancer relation for upgrades
* Stop testing on py37
* Successfully testing loadbalancers on serverstack
* Update integration tests to test new relations
* updated charmhub docs link
* Adjust docs to clarify return type
### vsphere-cloud-provider
[LP#2039667] Provide charm config parameters on the default storage class (#31)
* Provide charm config parameters on the default storage class
* Drive by linting fix
* Handle invalid storage parameters
* re-add asyncio_mode=auto for integration tests
### vsphere-integrator
upgrade integration tests to test storage and provider_ids
Merge pull request #14 from charmed-kubernetes/akd/modernize-integration-tests
upgrade integration tests to test storage and provider_ids
Just Blacken
Merge pull request #15 from charmed-kubernetes/akd/just-black
Just Black ⚫ 🐈‍⬛ 🏴 🖤

## Component Versions

### Charm/Addons pinned versions
- kube-ovn ?????
- calico ?????
- cephcsi ?????
- cinder-csi-plugin ?????
- coredns ?????
- ingress-nginx ?????
- k8s-keystone-auth ?????
- kube-state-metrics ?????
- kubernetes-dashboard ?????
- openstack-cloud-controller-manager ?????

### Charm default versions
- cloud-provider-vsphere ?????
- vsphere-csi-driver ?????
- cloud-provider-azure ?????
- azuredisk-csi-driver ?????
- cloud-provider-aws ?????
- aws-ebs-csi-driver ?????
- gcp-compute-persistent-disk-csi-driver ?????


## Fixes

A list of bug fixes and other minor feature updates in this release can be found at
[the launchpad milestone page for 1.29](https://launchpad.net/charmed-kubernetes/+milestone/1.29).


## Notes and Known Issues


## Deprecations and API changes

- Upstream

For details of other deprecation notices and API changes for Kubernetes 1.29, please see the
relevant sections of the [upstream release notes][upstream-changelog-1.29].

[upstream-changelog-1.29]: https://github.com/kubernetes/kubernetes/blob/master/CHANGELOG/CHANGELOG-1.29.md#deprecation

<!-- AUTOGENERATED RELEASE 1.29 ABOVE -->


<!--LINKS-->

[rel]: /kubernetes/docs/release-notes
