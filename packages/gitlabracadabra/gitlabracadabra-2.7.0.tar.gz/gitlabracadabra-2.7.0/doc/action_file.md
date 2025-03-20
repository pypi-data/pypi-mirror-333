# Table of Contents <!-- omit in toc -->

- [General syntax](#general-syntax)
- [`gitlab_id`](#gitlab_id)
- [`extends`](#extends)
- [`include`](#include)
- [Using `extends` and `include` together](#using-extends-and-include-together)

# General syntax

Action files are [YAML](https://yaml.org/) files.
It’s possible to use special YAML features like anchors (`&`),
aliases (`*`) and map merging (`<<`), which will allow you to
greatly reduce the complexity of action files.

Read more about the various [YAML features](https://learnxinyminutes.com/docs/yaml/).

Each key of an action file defines an object to manage.
If the key starts with a dot (`.`), it will not be processed,
but can be used in the [`extends`](#extends) directive.

The default object type is [`project`](project.md)
or [`group`](group.md) (if it's key ends with slash `/`).

# `gitlab_id`

GitLabracadabra can manage several GitLab connections at once.

With this `~/.python-gitlab.cfg` :

```ini
[global]
default = gitlab

[gitlab]
url = https://gitlab.com
private_token = S0mT0ken

[gnome]
url = https://gitlab.gnome.org/
private_token = S0mT0ken

[salsa]
url = https://salsa.debian.org
private_token = S0mT0ken
```

And this `gitlabracadabra.yml` :

```yaml
# Will create the following project on https://gitlab.gnome.org/
gnome-group/gnome-project:
  gitlab_id: gnome
  create_object: true

# Will create the following project on default, i.e. gitlab
# unless gitlab_id is passed to CLI
other-group/other-project:
  create_object: true
```


# `extends`

An object can inherit from another one using the `extends` keyword.

For example :
```yaml
.default-project:
  create_object: true
  default_branch: main
  description: ''
  issues_access_level: enabled
  repository_access_level: enabled
  merge_requests_access_level: enabled
  protected_branches:
    main:
      merge_access_level: maintainer
      push_access_level: noone
  unknown_protected_branches: delete

group1/project1:
  extends: .default-project

group1/project2:
  extends: .default-project
  protected_branches:
    develop:
      merge_access_level: developer
      push_access_level: noone

```

The resulting object will be deeply merged on top of the referenced object (i.e.
`group1/project2` will have both `main` and `develop` branches protected).
This was not the case [before version 0.4.1a0](https://gitlab.com/gitlabracadabra/gitlabracadabra/issues/10).

Multiple parents for extends and other merging strategies are also possible :
```yaml
.small-team:
  members:
    john: maintainer

group1/project3:
  extends:
    - .default-project: replace # We don't want the main branch to be protected
    - .small-team # default merge strategy is "deep"
  protected_branches:
    develop:
      merge_access_level: developer
      push_access_level: noone
```

The available merging strategies are:

- `replace` : each parameters from the current object override the ones from the
  referenced object
- `deep` (the default) : like `replace`, but dictionaries are deeply
  merged
- `aggregate` : like `deep`, with lists also aggregated

# `include`

Using the `include` keyword, you can allow the inclusion of external YAML files.

Example :
```yaml
include:
  - gitlabracadabra.yml
```

Notes:
- The file path is relative to current working directory
- Absolute path (starting with slash `/`) and
  path from adjacent directories (containing double-dot `..`)
  are forbidden.
- The including file will be deeply merged (`deep`) on top of the included file

# Using `extends` and `include` together

`extends` works across configuration files combined with `include`.
