---
title: "Documentation for The Canonical Distribution of Kubernetes <sup>&reg;</sup>"
keywords: homepage
tags: [getting_started]
sidebar: k8smain-sidebar
permalink: index.html
layout: base
toc: False
summary: This page is currently a work in progress. For existing documentation, please visit <a href="https://kubernetes.io/docs/getting-started-guides/ubuntu/"> https://kubernetes.io/docs/getting-started-guides/ubuntu/ </a>
---
## Introducing the Canonical Distribution of Kubernetes<sup>&reg;</sup>

The Canonical Distribution of Kubernetes<sup>&reg;</sup> (CDK), is pure Kubernetes tested across
the widest range of clouds with modern metrics and monitoring, brought to you by the people who
deliver Ubuntu.
<hr class="is-deep">
<div class="p-strip">
    <div class="p-content__row">
        <div class="u-equal-height">
            <div class="col-6">
                <h2>Getting started</h2>
                <p></p>
                <p><a href="/getting-started">Getting started with the Canonical Distribution of Kubernetes<sup>&reg;</sup> &nbsp;&rsaquo;</a></p>
            </div>
            <div class="col-6 u-align--right">
                <img style="border: 0" src="https://assets.ubuntu.com/v1/843c77b6-juju-at-a-glace.svg">
            </div>
        </div>
        <hr class="is-deep">
        <div class="u-equal-height">
            <div class="col-6">
                <h2>What's new</h2>
                <ul class="p-list">
                     {% for post in site.posts  limit:3 %}
                     <li class="p-list__item"><a class="post-link" href="{{ post.url | prepend: site.baseurl }}">{{ post.title }}&nbsp;&rsaquo;</a></li>
                        {% endfor %}
                </ul>
            </div>
            <div class="col-6">
                <h2>Tutorials</h2>
                <ul class="p-list">
                    <li class="p-list__item"><a href="https://tutorials.ubuntu.com/tutorial/get-started-kubeflow#0">get started with Kubeflow&nbsp;&rsaquo;</a></li>
                </ul>
            </div>
        </div>
        <hr class="is-deep">
  </div>
</div>


{% include links.html %}
