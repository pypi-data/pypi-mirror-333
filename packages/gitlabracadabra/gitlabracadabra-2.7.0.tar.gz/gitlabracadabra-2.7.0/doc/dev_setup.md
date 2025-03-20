# Development environment <!-- omit in toc -->

- [Install Docker](#install-docker)
- [Install GitLab](#install-gitlab)
- [Configure GitLab](#configure-gitlab)
- [Setup virtual environment](#setup-virtual-environment)
- [Run tests](#run-tests)

## Install Docker

See [official installation documentation](https://docs.docker.com/install/).

## Install GitLab

From gitlabracadabra directory:

```console
$ export GITLAB_HOME=$PWD/../gitlab
$ sudo docker pull gitlab/gitlab-ee:latest
$ sudo docker run --detach \
  --hostname gitlab.example.com \
  --env GITLAB_OMNIBUS_CONFIG="registry_external_url 'http://gitlab-registry.example.com';" \
  --publish 443:443 --publish 80:80 --publish 22:22 \
  --name gitlab \
  --restart always \
  --volume $GITLAB_HOME/config:/etc/gitlab \
  --volume $GITLAB_HOME/logs:/var/log/gitlab \
  --volume $GITLAB_HOME/data:/var/opt/gitlab \
  --shm-size 256m \
  gitlab/gitlab-ee:latest
Unable to find image 'gitlab/gitlab-ee:latest' locally
latest: Pulling from gitlab/gitlab-ee
d7bfe07ed847: Pull complete
b8e827cd9b7e: Pull complete
b0ce00ffca81: Pull complete
e2ab8f994ad2: Pull complete
117b4f9caa08: Pull complete
41336762b8d0: Pull complete
9e7d5afc634f: Pull complete
d86eca3ad7c4: Pull complete
Digest: sha256:940a728f448f0f03281e9b6da86ebfb4fddac10225f7a7f8fc2b145efddacdad
Status: Downloaded newer image for gitlab/gitlab-ee:latest
b0e06ee9b4918398b35d4ee5e5f6e281471d9927a54be10ca67efb04ddfb6e5c
```

See [official installation documentation](https://docs.gitlab.com/ee/install/docker.html#install-gitlab-using-docker-engine)
for detailed instructions.

Ensure your `/etc/hosts` has the following aliases for `127.0.0.1`:

```pre
127.0.0.1       localhost       gitlab.example.com gitlab-registry.example.com
```

## Configure GitLab

Get initial root password:

```console
$ sudo docker exec -it gitlab grep 'Password:' /etc/gitlab/initial_root_password
Password: abcd
```

Visit <http://gitlab.example.com> (or <http://localhost>), go to *Edit profile*,
*[Access Tokens](http://localhost/-/profile/personal_access_tokens)*, and create a
new token with the `api` scope. Paste this token in
[`tests/python-gitlab.cfg`](../gitlabracadabra/tests/python-gitlab.cfg), and change `url`.

Depending on your tests, you may need to create additional resources in GitLab
(groups, projects, ...).

## Setup virtual environment

```shell
rm -rf venv .venv
virtualenv .venv
. .venv/bin/activate
pip install hatch hatch-pip-compile
```

## Run tests

```shell
. .venv/bin/activate

hatch fmt && \
hatch run types:check && \
hatch test --cover -vv && \
hatch run hatch-test.py3.11:coverage html
```

When recording a new cassette, change `record_mode` in [`tests/vcrfuncs.py`](../gitlabracadabra/tests/vcrfuncs.py).
