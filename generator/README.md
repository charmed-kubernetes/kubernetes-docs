Kubernetes Docs Generator
--------------

Generate charmed-kubernetes documentation pages

```bash
pushd generator
RELEASE=1.24 tox -e run
popd
```

After which the `pages/` directory should have differences ready for a PR