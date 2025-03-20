# Mirroring packages <!-- omit in toc -->

GitLabracadabra can mirror packages, of the following types :

- [Raw URLs to generic packages](#raw-urls-to-generic-packages)
- [GitHub releases to generic packages](#github-releases-to-generic-packages)
- [PyPI packages](#pypi-packages)
- [Helm charts](#helm-charts)

(In the following examples, `gitlab.example.org` is the GitLab's hostname).

## Raw URLs to generic packages

You can mirror one file:

```yaml
mygroup/myproject:
  package_mirrors:
    - raw:
        default_url: https://download.docker.com/linux/debian/gpg
        default_package_name: docker
        default_package_version: '0'
```

This will mirror `https://download.docker.com/linux/debian/gpg`
to file `gpg` in generic package `docker` version `0` of project `mygroup/myproject` (i.e to
`https://gitlab.example.org/api/v4/projects/mygroup%2Fmyproject/packages/generic/docker/0/gpg`). Note that destination `file_name` defaults to last part of source URL (after last `/`).

Only the `default_url` is mandatory, `default_package_name` defaults to `'unknown'`,
and `default_package_version` defaults to `'0'`.

You can mirror several files at once. Example :

```yaml
mygroup/myproject:
  package_mirrors:
    - raw:
        default_url: 'https://storage.googleapis.com/{package_name}-release/release/{package_version}/bin/linux/amd64/{file_name}'
        default_package_name: kubernetes
        default_package_version: 'v1.20.5'
        package_files:
        - file_name: kubectl
        - file_name: kubelet
        - file_name: kubeadm
```

This will mirror `https://storage.googleapis.com/kubernetes-release/release/v1.20.5/bin/linux/amd64/kubectl`, `kubelet`, and `kubeadm` to generic package `kubernetes` version `v1.20.5`.

The following example is another way to mirror the same files:

```yaml
mygroup/myproject:
  package_mirrors:
    - raw:
        default_url: 'https://storage.googleapis.com/{package_name}-release/release/{package_version}/bin/linux/amd64'
        default_package_name: kubernetes
        default_package_version: 'v1.20.5'
        package_files:
        - url: '{default_url}/kubectl'
        - url: '{default_url}/kubelet'
        - url: '{default_url}/kubeadm'
```

It's also possible to override `package_name` and `package_version` for specific
`package_file`s:

```yaml
mygroup/myproject:
  package_mirrors:
    - raw:
        default_url: 'https://example.org/{package_name}-{package_version}.tgz'
        default_package_name: pkg1 # defaults to 'unknown'
        default_package_version: 'v1.0.0' # defaults to '0'
        package_files:
        - {}
        - package_name: pkg2
          package_version: 'v2.0.0'
        - package_name: pkg3
          file_name: third_package.tgz
      # enabled: true # default
```

This will mirror :

- `https://example.org/pkg1-v1.0.0.tgz` to `pkg1` version `v1.0.0` (file `pkg1-v1.0.0.tgz`),
- `https://example.org/pkg2-v2.0.0.tgz` to `pkg2` version `v2.0.0` (file `pkg2-v2.0.0.tgz`),
- `https://example.org/pkg3-v1.0.0.tgz` to `pkg3` version `v1.0.0` (file `third_package.tgz`)

## GitHub releases to generic packages

You can mirror tarballs and zipballs of the git repository :

```yaml
mygroup/myproject:
  package_mirrors:
    - github:
        full_name: kubernetes-sigs/kubespray
        # package_name: (defaults to repository name = kubespray)
        latest_release: true
        tarball: true
        # zipball: false
```

This will mirror the latest stable release tarball as `'kubespray-v2.15.1.tar.gz'`
to generic package `'kubespray'` version `'v2.15.1'`.

You can also mirror assets by name.

You can use tag matching and [Semantic Versioning](https://semver.org/), like in:

```yaml
mygroup/myproject:
  package_mirrors:
    - github:
        full_name: operator-framework/operator-lifecycle-manager
        # package_name: (defaults to repository name = operator-lifecycle-manager)
        tags:
        - '/v.*/'
        semver: '>=0.18.0',
        latest_release: true
        # tarball: false
        # zipball: false
        assets:
        - install.sh
        - crds.yaml
        - olm.yaml
      # enabled: true # default
```

This will mirror `install.sh`, `crds.yaml` and `olm.yaml` from versions `'v0.18.0'` and `'v0.18.1'`
to generic packages `'operator-lifecycle-manager'` of the same versions.

Note:
[GitHub uses rate limiting to control API traffic](https://docs.github.com/en/rest/overview/resources-in-the-rest-api?apiVersion=2022-11-28#rate-limiting).
You can increase your quota by passing a GitHub token in the `GITHUB_TOKEN` environment variable.

## PyPI packages

You can mirror PyPI packages:

```yaml
mygroup/myproject:
  package_mirrors:
    - pypi:
        requirements:
        - python-gitlab>=1.6.0
        - PyYAML
```

`requirements` has the same syntax as a `requirements.txt` file,
the best match (i.e. newer version) is mirrored.

Wheels (`.whl`) and sources (`.tar.gz`) are mirrored, but not egg files (`.egg`).

An alternative index can be used with `index_url`:

```yaml
mygroup/myproject:
  package_mirrors:
    - pypi:
        index_url: https://pypi.example.com:8080
        requirements:
        - pypi
      # enabled: true # default
```

Note: `pypi` package mirroring requires `packaging >= 20.9`.

## Helm charts

You can mirror Helm charts:

```yaml
mygroup/myproject:
  package_mirrors:
    - helm:
        repo_url: https://charts.rook.io/release
        package_name: rook-ceph
        # channel: stable # Destination channel
```

This will mirror the latest `rook-ceph-vX.Y.Z.tgz` to the channel `'stable'`.

Additional parameters are available:

```yaml
mygroup/myproject:
  package_mirrors:
    - helm:
        repo_url: https://charts.rook.io/release
        package_name: /rook-ceph.*/  # Will also match rook-ceph-cluster
        versions:
        - '1.2.3'
        - '2.3.4'
        semver: '>=1.0'
        limit: 10 # default to 1
        channel: stable # default destination channel
      # enabled: true # default
```

Notes:

- By default, only stable versions are fetched (i.e. `versions: ['/.*/']` and
  `semver: '*'`). If, for example, you also want beta versions of `1.0`, use
  `semver: '* || >=1.0.0-b'`
- `limit: n` keeps the latest `n` charts
