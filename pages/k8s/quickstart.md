---
wrapper_template: "base_docs.html"
markdown_includes:
  nav: "shared/_side-navigation.md"
context:
  title: "Quick start"
  description: With this quick start guide and some tools from Canonical, you'll have a Kubernetes cluster running on the cloud of your choice in minutes!
keywords: quickstart
tags: [getting_started]
sidebar: k8smain-sidebar
permalink: quickstart.html
layout: [base, ubuntu-com]
toc: False
---

Charmed Kubernetes<sup>&reg;</sup> delivers a ‘pure K8s’ experience, tested across a wide range of clouds and integrated with modern metrics and monitoring. It works across all major public clouds and private infrastructure, enabling your teams to operate Kubernetes clusters on demand, anywhere.

With this quick start guide and some tools from Canonical, you'll have a
Kubernetes cluster running on the cloud of your choice in minutes!

## What you'll need

- An Ubuntu 18.04 LTS or 16.04 LTS environment to run the commands (or another operating system which supports `snapd` - see the [snapd documentation][snapd-docs])
- Account credentials for one of the following public clouds:
  - [Amazon Web Services][cloud-aws], including AWS-China and AWS-gov
  - [CloudSigma][cloud-cloudsigma]
  - [Google Cloud platform ][cloud-google]
  - [Joyent][cloud-joyent]
  - [Microsoft Azure][cloud-azure], including Azure-China
  - [Oracle Cloud][cloud-oracle]
  - [Rackspace][cloud-rackspace]

<div class="p-notification--positive"><p markdown="1" class="p-notification__response">
<span class="p-notification__status">Note:</span> If you don't meet these requirements, there are additional ways of installing the <emphasis>Charmed Distribution of Kubernetes<sup>&reg;</sup></emphasis>, inluding additional OS support and an entirely local deploy. Please see the more general <a href="/kubernetes/install">Installing Charmed Kubernetes</a> page for details. </p></div>


<section class="p-strip--light is-bordered">
  <div class="row">
    <div class="col-12">
      <ol class="p-stepped-list--detailed">

        <li class="p-list-step__item col-12">
          <h3 class="p-list-step__title col-12"><span class="p-list-step__bullet">1</span>Install Juju</h3>
          <div class="p-list-step__content">

<a class="p-link--external" href="https://jaas.ai" > Juju </a> is a tool for
deploying, configuring, and operating complex software on public or private
clouds. It can be installed with a snap:

            <div class="p-code-snippet">
              <input class="p-code-snippet__input" value="sudo snap install juju --classic" readonly="readonly">
              <button class="p-code-snippet__action">Copy to clipboard</button>
            </div>
            <script id="asciicast-254739" src="https://asciinema.org/a/254739.js" async data-autoplay="true" data-rows="4"></script>
          </div>
        </li>

        <li class="p-list-step__item col-12">
          <h3 class="p-list-step__title"><span class="p-list-step__bullet">2</span>Find your cloud</h3>
          <div class="p-list-step__content">

Juju has baked in knowledge of many public clouds such as AWS, Azure and
Google. You can see which ones are ready to use by running this command:

            <div class="p-code-snippet">
              <input class="p-code-snippet__input" value="juju clouds" readonly="readonly">
              <button class="p-code-snippet__action">Copy to clipboard</button>
            </div>
            <script id="asciicast-254740" src="https://asciinema.org/a/254740.js" async data-rows="18"></script>

            <p><a class="p-link--external" href="https://docs.jujucharms.com/clouds">Find out more about Clouds in Juju</a></p>
          </div>
        </li>

        <li class="p-list-step__item col-12">
          <h3 class="p-list-step__title"><span class="p-list-step__bullet">3</span>Add Credentials</h3>
          <div class="p-list-step__content">
            <p>Most clouds require credentials so that the cloud knows which operations are authorised and on which account. If you choose to use AWS, for example, you would run <code>juju add-credential aws</code></p>
            <div class="p-code-snippet">
              <input class="p-code-snippet__input" value="juju add-credential aws" readonly="readonly">
              <button class="p-code-snippet__action">Copy to clipboard</button>
            </div>
          </div>
        </li>

        <li class="p-list-step__item col-12">
          <h3 class="p-list-step__title"><span class="p-list-step__bullet">4</span>Add Controller</h3>
          <div class="p-list-step__content">
            <p>The Juju controller is used to manage the software deployed through Juju, from deployment to upgrades to day-two operations.</p>
            <div class="p-code-snippet">
              <input class="p-code-snippet__input" value="juju bootstrap aws my-controller" readonly="readonly">
              <button class="p-code-snippet__action">Copy to clipboard</button>
            </div>
          </div>
        </li>

        <li class="p-list-step__item col-12">
          <h3 class="p-list-step__title"><span class="p-list-step__bullet">5</span>Add Model</h3>
          <div class="p-list-step__content">
            <p>The model holds a specific deployment, like Kubernetes, which includes all necessary applications and the number of instances of each one. This is where the number of Kubernetes worker nodes are scaled up or down.</p>
            <div class="p-code-snippet">
              <input class="p-code-snippet__input" value="juju add-model k8s-test" readonly="readonly">
              <button class="p-code-snippet__action">Copy to clipboard</button>
            </div>
          </div>
        </li>

        <li class="p-list-step__item col-12">
          <h3 class="p-list-step__title"><span class="p-list-step__bullet">6</span>Deploy Kubernetes</h3>
          <div class="p-list-step__content">
            <p>Add the Kubernetes bundle to the model and deploy the components, including the default number of components, like worker nodes.</p>
            <div class="p-code-snippet">
              <input class="p-code-snippet__input" value="juju deploy charmed-kubernetes" readonly="readonly">
              <button class="p-code-snippet__action">Copy to clipboard</button>
            </div>
          </div>
        </li>

        <li class="p-list-step__item col-12">
          <h3 class="p-list-step__title"><span class="p-list-step__bullet">&#9734;</span>Useful tips</h3>
          <div class="p-list-step__content">
            <p><strong>Observe installation progress:</strong> Watch the deployment process in real-time:</p>
            <div class="p-code-snippet">
              <input class="p-code-snippet__input" value="watch -c juju status --color" readonly="readonly">
              <button class="p-code-snippet__action">Copy to clipboard</button>
            </div>
            <p><strong>Observe log messages:</strong> To  view the last twenty log messages for the “k8s-test” model:</p>
            <div class="p-code-snippet">
              <input class="p-code-snippet__input" value="juju debug-log -m k8s-test -n 20" readonly="readonly">
              <button class="p-code-snippet__action">Copy to clipboard</button>
            </div>
            <p><strong>Accessing Kubernetes:</strong> Juju creates a .kubeconfig file that is required  for accessing the Kubernetes cluster it created. Follow these instructions to install kubectl (if needed) and export the configuration file: (use kubectl to run commands against Kubernetes clusters)</p>
            <pre><code>$ mkdir -p ~/.kube
$ juju scp kubernetes-master/0:config ~/.kube/config
$ snap install kubectl --classic
$ kubectl cluster-info</code></pre>
              <p><strong>Useful Links:</strong> Find out more about Charmed Kubernetes.</p>
              <ul style="list-style-type: disc;">
                <li><a href="/kubernetes/docs/install-manual">Manual Install&nbsp;&rsaquo;</a></li>
                <li><a class="p-link--external" href="https://docs.jujucharms.com/maas-cloud">Find out more about MAAS as a Cloud in Juju</a></li>
                <li><a class="p-link--external" href="https://docs.jujucharms.com/">Full Juju documentation</a></li>
                <li><a href="/kubernetes/docs">Full Kubernetes documentation&nbsp;&rsaquo;</a></li>
              </ul>
            </div>
          </li>

        </ol>

      </div>
    </div>
  </section>

Congratulations! You now have a cluster up and running with the **Charmed Distribution of Kubernetes**&nbsp;<sup>&reg;</sup>

You can now check the status of the cluster yourself by running the command:

```bash
kubectl cluster-info
```

The output should look similar to this:

![cli output](https://assets.ubuntu.com/v1/d5519ed3-CDK-clusterinfo.png)

This shows the relevant IP addresses for operating your cluster.

### Access the dashboard

To check that everything is actually working, you may want to log in to the Kubernetes Dashboard.

The recommended way to do this is to use the built-in proxy service, run with the following:

```bash
kubectl proxy
```

The URL for the dashboard will then be [http://localhost:8001/api/v1/namespaces/kube-system/services/https:kubernetes-dashboard:/proxy/](http://localhost:8001/api/v1/namespaces/kube-system/services/https:kubernetes-dashboard:/proxy/)

Open a browser at the address for the Dashboard. You will see an authentication screen:

![dashboard image](https://assets.ubuntu.com/v1/80980265-dashboard_login.png)

You will need to log in to the Dashboard with a valid user. The easiest thing to do is to select your kubeconfig file, but for future administration, you should set up _role based access control_.

![dashboard image](https://assets.ubuntu.com/v1/37ee63d6-CDK-008.png)

## Next steps

Now that you have your cluster, you can put it to work! Here are a few recommended starting points:

- [Add persistent storage&nbsp;&rsaquo;][storage]

<sub>Kubernetes<sup>&reg;</sup> is a registered trademark of The Linux Foundation in the United States and other countries, and is used pursuant to a license from The Linux Foundation. </sub>

<!-- LINKS -->

[jujucharms-com]: https://jujucharms.com
[conjure-up-io]: https://conjure-up.io
[install]: /kubernetes/install
[overview]: /kubernetes/docs/overview
[snapd-docs]: https://docs.snapcraft.io/core/install
[cloud-aws]: https://aws.amazon.com
[cloud-cloudsigma]: https://www.cloudsigma.com
[cloud-google]: https://cloud.google.com/
[cloud-oracle]: https://cloud.oracle.com/home
[cloud-rackspace]: https://www.rackspace.com/cloud/
[cloud-azure]: https://azure.microsoft.com/
[cloud-joyent]: https://www.joyent.com/
[how-login]: /kubernetes/docs/howto-login
[how-helm]: /kubernetes/docs/howto-helm
[how-juju]: /kubernetes/docs/howto-juju
[storage]: /kubernetes/docs/storage
