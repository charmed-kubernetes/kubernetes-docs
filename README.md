## Charmed Kubernetes documentation

This is a repository for iterating on new versions of the Charmed Kubernetes docs.
This official docs are published at :
[https://www.ubuntu.com/kubernetes/docs](https://www.ubuntu.com/kubernetes/docs)

This repository is set to live publish at:
[https://cdk-docs.netlify.app/](https://cdk-docs.netlify.app/)
This is published from the **current** branch, which is kept in sync with the published docs at ubuntu.com. 

[![Netlify Status](https://api.netlify.com/api/v1/badges/a4e301cd-70c0-4945-bb09-7198cbdd4753/deploy-status)](https://app.netlify.com/sites/cdk-docs/deploys)

The development version (main) of docs is published at
[https://cdk-docs-next.netlify.app/](https://cdk-docs-next.netlify.app/)

[![Netlify Status](https://api.netlify.com/api/v1/badges/a4e301cd-70c0-4945-bb09-7198cbdd4753/deploy-status)](https://app.netlify.com/sites/cdk-docs-next/deploys)

Any tweaks or contributions should be targetted at the **main** branch. The current branch is regenerated frequently and largely automated.

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

If you make a PR, the netlify tests will automatically generate a demo website (click on 'Details' in the deployments section)

## Code of conduct

Charmed Kubernetes has adopted the [Ubuntu Code of Conduct v2.0](https://ubuntu.com/community/ethos/code-of-conduct).
