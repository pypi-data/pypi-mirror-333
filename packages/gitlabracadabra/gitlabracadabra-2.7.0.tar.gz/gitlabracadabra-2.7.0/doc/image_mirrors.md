# Mirroring container images <!-- omit in toc -->

GitLabracadabra can mirror Docker images from any compatible registry to
a GitLab's registry.

In the following examples, `gitlab-registry.example.org` is the GitLab's
registry hostname.

- [Basic mirroring](#basic-mirroring)
- [Destination](#destination)
- [SemVer](#semver)
- [Advanced mirroring](#advanced-mirroring)
- [Advanced destination](#advanced-destination)
- [Tag matching](#tag-matching)
- [Digest](#digest)
- [Other options](#other-options)

## Basic mirroring

The simplest configuration:

```yaml
mygroup/myproject:
  image_mirrors:
    - from: 'debian:bookworm'
```

This will mirror `debian:bookworm` (which is the short reference for
`docker.io/library/debian:bookworm`) to `gitlab-registry.example.org/mygroup/myproject/library/debian:bookworm`.

## Destination

By default, the full source reference without the hostname is used as destination name. You can override the destination by setting `to`:

```yaml
mygroup/myproject:
  image_mirrors:
    - from: 'debian:bookworm'
      to: 'debian:stable'
    - from: 'debian:bullseye'
      to: 'debian:oldstable'
```

This will mirror:

- `debian:bookworm` to `gitlab-registry.example.org/mygroup/myproject/debian:stable`, and
- `debian:bullseye` to `gitlab-registry.example.org/mygroup/myproject/debian:oldstable`.

If the destination has no tag, the source tag is preserved. Example:

```yaml
mygroup/myproject:
  image_mirrors:
    - from: 'debian:bookworm'
      to: ''
```

This will mirror `debian:bookworm` to `gitlab-registry.example.org/mygroup/myproject:bookworm`.

## SemVer

For repositories using [Semantic Versioning](https://semver.org/) for tags
(with optional leading `v`),
you can use [NPM ranges](https://semver.npmjs.com/), like in:

```yaml
mygroup/myproject:
  image_mirrors:
    - from: 'k8s.gcr.io/kubernetes/kube-apiserver'
      semver: '>=1.20.5'
```

This will mirror:

- `k8s.gcr.io/kubernetes/kube-apiserver:v1.20.5` to `mygroup/myproject/kubernetes/kube-apiserver:v1.20.5`
- `k8s.gcr.io/kubernetes/kube-apiserver:v1.21.0` to `mygroup/myproject/kubernetes/kube-apiserver:v1.21.0`
- ...

Notes:

- Based on [python-semanticversion](https://python-semanticversion.readthedocs.io/en/latest/#npm-based-ranges)
- If using `python-semanticversion` `<2.7`, only
  a [reduced range syntax](https://python-semanticversion.readthedocs.io/en/v1.0.0/#requirement-specification)
  is available

## Advanced mirroring

You can mirror several images at once:

```yaml
mygroup/myproject:
  image_mirrors:
    - from:
        base: k8s.gcr.io/kubernetes
        repositories:
          - kube-apiserver
          - kube-proxy
        tags:
          - v1.20.4
          - v1.20.6
```

This will loop on each `repositories` within `base`, and loop on each `tags` within
those repositories. Result:

- `k8s.gcr.io/kubernetes/kube-apiserver:v1.20.4`
- `k8s.gcr.io/kubernetes/kube-apiserver:v1.20.6`
- `k8s.gcr.io/kubernetes/kube-proxy:v1.20.4`
- `k8s.gcr.io/kubernetes/kube-proxy:v1.20.6`

The destination images names follow the same rule as explained in
[Basic mirroring](#basic-mirroring), i.e :

- `k8s.gcr.io/kubernetes/kube-apiserver:v1.20.4` to `mygroup/myproject/kubernetes/kube-apiserver:v1.20.4`
- `k8s.gcr.io/kubernetes/kube-apiserver:v1.20.6` to `mygroup/myproject/kubernetes/kube-apiserver:v1.20.6`
- `k8s.gcr.io/kubernetes/kube-proxy:v1.20.4` to `mygroup/myproject/kubernetes/kube-proxy:v1.20.4`
- `k8s.gcr.io/kubernetes/kube-proxy:v1.20.6` to `mygroup/myproject/kubernetes/kube-proxy:v1.20.6`

## Advanced destination

The `to` parameter can further customize the destination.

Example :

```yaml
mygroup/myproject:
  image_mirrors:
    - from:
        base: k8s.gcr.io/kubernetes
        repositories:
          - kube-apiserver
        tags:
          - v1.20.6
      to:
        base: k8s
        repository: apiserver
        tag: latest
```

This will mirror:

- `k8s.gcr.io/kubernetes/kube-apiserver:v1.20.6` to `mygroup/myproject/k8s/apiserver:latest`

If not specified, `base`, `repository` and `tag` default to their `from` counterparts.

As such:

```yaml
mygroup/myproject:
  image_mirrors:
    - from:
        base: k8s.gcr.io/kubernetes
        repositories:
          - kube-apiserver
          - kube-proxy
        tags:
          - v1.20.4
          - v1.20.6
      to: {}
```

This will import:

- `k8s.gcr.io/kubernetes/kube-apiserver:v1.20.4` as `mygroup/myproject/k8s.gcr.io/kubernetes/kube-apiserver:v1.20.4`
- `k8s.gcr.io/kubernetes/kube-apiserver:v1.20.6` as `mygroup/myproject/k8s.gcr.io/kubernetes/kube-apiserver:v1.20.6`
- `k8s.gcr.io/kubernetes/kube-proxy:v1.20.4` as `mygroup/myproject/k8s.gcr.io/kubernetes/kube-proxy:v1.20.4`
- `k8s.gcr.io/kubernetes/kube-proxy:v1.20.6` as `mygroup/myproject/k8s.gcr.io/kubernetes/kube-proxy:v1.20.6`

## Tag matching

Tags can be regular expressions too. Crazy example:

```yaml
mygroup/myproject:
  image_mirrors:
    - from:
        repositories:
          - busybox
          - debian
        tags:
          - '/(uns|s)(id|table)/'
      to:
        tag: 'how-\1-\2'
```

This will import:

- `docker.io/library/busybox:stable` as `mygroup/myproject/busybox:how-s-table`
- `docker.io/library/busybox:unstable` as `mygroup/myproject/busybox:how-uns-table`
- `docker.io/library/debian:sid` as `mygroup/myproject/debian:how-s-id`
- `docker.io/library/debian:stable` as `mygroup/myproject/debian:how-s-table`
- `docker.io/library/debian:unstable` as `mygroup/myproject/debian:how-uns-table`

This works for string-form `from` too:

```yaml
mygroup/myproject:
  image_mirrors:
    - from: 'busybox:/(uns|s)(id|table)/'
```

This will import:

- `docker.io/library/busybox:stable` as `mygroup/myproject/library/busybox:stable`
- `docker.io/library/busybox:unstable` as `mygroup/myproject/library/busybox:unstable`

This works for string-form `from` and dict-form `to` too:

```yaml
mygroup/myproject:
  image_mirrors:
    - from: 'busybox:/(uns|s)(id|table)/'
      to:
        tag: 'how-\1-\2'
```

This will import:

- `docker.io/library/busybox:stable` as `mygroup/myproject/docker.io/library/busybox:how-s-table`
- `docker.io/library/busybox:unstable` as `mygroup/myproject/docker.io/library/busybox:how-uns-table`

## Digest

Source tag can also be matched by digest. Example:

```yaml
mygroup/myproject:
  image_mirrors:
    - from: quay.io/operator-framework/olm@sha256:de396b540b82219812061d0d753440d5655250c621c753ed1dc67d6154741607
```

This will mirror `quay.io/operator-framework/olm@sha256:de396b540b82219812061d0d753440d5655250c621c753ed1dc67d6154741607`)
to `gitlab-registry.example.org/mygroup/myproject/operator-framework/olm:latest`.

## Other options

Each image mirror can be enabled or disabled. Example:

```yaml
mygroup/myproject:
  image_mirrors:
    - from: debian:trixie
      enabled: true
    - from: debian:bullseye
      enabled: false
```
