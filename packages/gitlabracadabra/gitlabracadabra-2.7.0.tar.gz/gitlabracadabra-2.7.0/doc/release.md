# Releasing GitLabracadabra

## Requirements

:package: Ensure required dependencies are installed:

```shell
sudo apt-get update
sudo apt-get install -y --no-install-recommends \
  debhelper \
  dh-python \
  dput \
  git-buildpackage \
  python3-build
# You also need a recent npm
npm install \
  semantic-release \
  @semantic-release/changelog \
  @semantic-release/exec \
  @semantic-release/git \
  conventional-changelog-conventionalcommits \
  @google/semantic-release-replace-plugin
```

:white_check_mark: Ensure last pipeline for `main` passed

:up: Ensure your Git repository is up to date:

```shell
git checkout main
git pull --rebase --prune
git status
```

:arrow_up: Ensure you can push to `main` branch :

```shell
git push
```

:book: Ensure doc is up to date :

```shell
rm -rf venv .venv
virtualenv .venv
. .venv/bin/activate
pip install hatch hatch-pip-compile
for t in project group user application_settings; do
  hatch run gitlabracadabra --doc-markdown $t > doc/$t.md
done
```

## Pre-release tests

:todo: Test the build:

```shell
hatch fmt && \
hatch run types:check && \
hatch test --cover -vv && \
hatch run hatch-test.py3.11:coverage html
```

:gear: Build the PYPI package:

```shell
pip install -r build-requirements.txt
python3 -m build
```

:gear: Build the Debian source package:

```shell
gbp buildpackage -S -d
```

## Release

:todo: Run `semantic-release`:

```shell
npx semantic-release --no-ci
git push
```

:gear: Build the PYPI package:

```shell
pip install -r build-requirements.txt
python3 -m build
```

:gear: Build the Debian source package:

```shell
gbp buildpackage -S -d
```

<!--
:arrow_up: Upload to test.pypi.org

```shell
version="$(grep __version__ gitlabracadabra/__init__.py  | awk -F "'" '{print $2}')"
twine upload --repository-url https://test.pypi.org/legacy/ "dist/gitlabracadabra-$version"*
```
-->

:arrow_up: Upload artifacts to PyPI and Debian:

```shell
version="$(grep __version__ src/gitlabracadabra/__init__.py  | awk -F '"' '{print $2}')"
hatch publish
dput "../gitlabracadabra_${version}_source.changes"
```
