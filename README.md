## Charmed Kubernetes documentation

This is a repository for iterating on new versions of the Charmed Kubernetes docs.
This official docs are published at :
[https://www.ubuntu.com/kubernetes/docs](https://www.ubuntu.com/kubernetes/docs)

This repository is set to live publish at:
[https://cdk-docs.netlify.com/](https://cdk-docs.netlify.com/)
This is published from the **current** branch

[![Netlify Status](https://api.netlify.com/api/v1/badges/a4e301cd-70c0-4945-bb09-7198cbdd4753/deploy-status)](https://app.netlify.com/sites/cdk-docs/deploys)

The development version (master) of docs is published at
[https://cdk-docs-next.netlify.com/](https://cdk-docs-next.netlify.com/)

[![Netlify Status](https://api.netlify.com/api/v1/badges/a4e301cd-70c0-4945-bb09-7198cbdd4753/deploy-status)](https://app.netlify.com/sites/cdk-docs-next/deploys)

## Licenses

The code-part of this repository is based on Jekyll. This code is covered by the MIT license which originally
applied to it. The Jekyll code is used only to provide a demo of the final site, not it the production site itself.

The Content of the documentation is licensed under the Creative Commons Attribution-ShareAlike 4.0 International Public
License [**CC-BY-SA-4.0**](licenses/CC-BY-SA-4.0). Any contributions or PRs to this repo containing documentation
content are accepted on the basis this license can and will still apply.
 
## Contributing

If you want to contribute to docs, you can just follow the links at the bottom of any published docs page and edit 
them straight away. For a more detailed guide to style, Markdown format, conventions in docs and similar
material, please see the contributing page.

## Layout

The content is contained in one main place:

1.  The **pages/k8s/** folder, which contains markdown files mapping to individual pages of the docs.

## Testing docs

If you have cloned this repo and wish to build it locally to test changes, the easiest way is to use ruby/jekyll

      bundle exec jekyll serve

If you make a PR, the netlify tests will atuomatically generate a demo website (click on 'Details' in the deployments section)
