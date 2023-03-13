Kubernetes Docs Generator
--------------

Generate charmed-kubernetes documentation pages

```bash
pushd generator
RELEASE=1.26 tox -e generate
popd
```

After which the `pages/` directory should have differences ready for a PR