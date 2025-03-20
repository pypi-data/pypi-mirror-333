# Mirroring Git repositories

GitLabracadabra can mirror Git repositories into a GitLab project.

## Basic mirroring

The simplest configuration:

```yaml
mygroup/myproject:
  mirrors:
    - url: https://gitlab.com/gitlabracadabra/gitlabracadabra.git
```

This will pull from `https://gitlab.com/gitlabracadabra/gitlabracadabra.git` and push into `mygroup/myproject`.

By default all branches and tags are mirrored.

## Branches and tag matching

If needed, only a subset of branches and tags can be mirrored:

```yaml
mygroup/myproject:
  mirrors:
    - url: https://gitlab.com/gitlabracadabra/gitlabracadabra.git
      branches: # if you omit this parameter, all branches are mirrored
        - from: '/wip-.*/'
          to: '' # This will skip branches starting with wip-
        - from: main
          # to: main # implicitly equal to source branch
        - from: '/(.*)/' # Using regexps
          to: 'upstream/\1'
      tags: # if you omit this parameter, all tags are mirrored
        - from: '/v(.*)/i'
          to: 'upstream-\1' # you can access match groups
  builds_access_level: disabled # If you want to prevent triggering pipelines on push
```

To mirror only `main`, and no tag:

```yaml
mygroup/myproject:
  mirrors:
    - url: https://gitlab.com/gitlabracadabra/gitlabracadabra.git
      branches:
        - from: main
      tags: []
```

## Authentication

If authentication is needed, `auth_id` can be used to read the credentials from `.python-gitlab.cfg`.

For example :

```yaml
mygroup/myproject:
  mirrors:
    - url: https://github.com/some_group/private_project.git
      auth_id: github
```

With the related `~/.python-gitlab.cfg`:

```ini
[global]
default = internal

[internal]
url = https://gitlab.example.org/
private_token = T0K3N1

[github]
url = https://github.com
http_username = MyUser
http_password = MyP@ss
```

See also [`gitlab_id`](action_file.md#gitlab_id).
