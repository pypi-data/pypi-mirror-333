# Table of Contents <!-- omit in toc -->

- [Group lifecycle](#group-lifecycle)
- [Manage](#manage)
  - [Members](#members)
  - [Labels](#labels)
- [Plan](#plan)
  - [Issue boards](#issue-boards)
  - [Milestones](#milestones)
- [General Settings](#general-settings)
  - [Naming, visibility](#naming-visibility)
  - [Permissions and group features](#permissions-and-group-features)
  - [GitLab Duo features](#gitlab-duo-features)
  - [Repository Settings](#repository-settings)
    - [Default branch](#default-branch)
  - [CI / CD Settings](#ci-cd-settings)
    - [Variables](#variables)
    - [Runners](#runners)
    - [Auto DevOps](#auto-devops)
- [Deprecated](#deprecated)
- [Undocumented](#undocumented)

# Group lifecycle

`gitlab_id` GitLab id:
```yaml
mygroup/:
  gitlab_id: gitlab
```

More information can be found [here](action_file.md#gitlab_id)

`create_object` Create object if it does not exists:
```yaml
mygroup/:
  create_object: true # or false
```

`delete_object` Delete object if it exists:
```yaml
mygroup/:
  delete_object: true # or false
```

# Manage

## Members

`members` Members:
```yaml
mygroup/:
  members:
    foo: developer
    bar: maintainer # one of guest, reporter, developer, maintainer, owner

```

`unknown_members` What to do with unknown members (`warn` by default):
```yaml
mygroup/:
  unknown_members: warn # one of warn, delete, remove, ignore, skip
```

`groups` Groups:
```yaml
mygroup/:
  groups:
    group/foo: guest
    group/bar: reporter # one of guest, reporter, developer, maintainer

```

`unknown_groups` What to do with unknown groups (`warn` by default):
```yaml
mygroup/:
  unknown_groups: warn # one of warn, delete, remove, ignore, skip
```

## Labels

`labels` The list of group's labels:
```yaml
mygroup/:
  labels:
    - name: bug
      color: '#d9534f'
      description: ''
    - name: confirmed
      color: '#d9534f'
      description: ''
    - name: critical
      color: '#d9534f'
      description: ''
    - name: discussion
      color: '#428bca'
      description: ''
    - name: documentation
      color: '#f0ad4e'
      description: ''
    - name: enhancement
      color: '#5cb85c'
      description: ''
    - name: suggestion
      color: '#428bca'
      description: ''
    - name: support
      color: '#f0ad4e'
      description: ''

```

`unknown_labels` What to do with unknown labels (`warn` by default):
```yaml
mygroup/:
  unknown_labels: warn # one of warn, delete, remove, ignore, skip
```

# Plan

## Issue boards

`boards` The list of group's boards:
```yaml
mygroup/:
  boards:
    - name: My group board
      # old_name: Development # Use this to rename a board
      hide_backlog_list: false
      hide_closed_list: false
      lists:
        - label: TODO
        - label: WIP

```

`unknown_boards` What to do with unknown boards (`warn` by default):
```yaml
mygroup/:
  unknown_boards: warn # one of warn, delete, remove, ignore, skip
```

`unknown_board_lists` What to do with unknown board lists (`delete` by default):
```yaml
mygroup/:
  unknown_board_lists: warn # one of warn, delete, remove, ignore, skip
```

## Milestones

`milestones` The list of group's milestones:
```yaml
mygroup/:
  milestones:
    - title: '1.0'
      description: Version 1.0
      due_date: '2021-01-23' # Quotes are mandatory
      start_date: '2020-01-23' # Quotes are mandatory
      state: active # or closed

```

`unknown_milestones` What to do with unknown milestones (`warn` by default):
```yaml
mygroup/:
  unknown_milestones: warn # one of warn, delete, remove, ignore, skip
```

# General Settings

## Naming, visibility

`name` The name of the group:
```yaml
mygroup/:
  name: My name
```

`description` The group's description:
```yaml
mygroup/:
  description: My description
```

`visibility` The group's visibility. Can be private, internal, or public:
```yaml
mygroup/:
  visibility: private # one of private, internal, public
```

## Permissions and group features

`prevent_sharing_groups_outside_hierarchy` Prevent group sharing outside the group hierarchy. This attribute is only available on top-level groups:
```yaml
mygroup/:
  prevent_sharing_groups_outside_hierarchy: true # or false
```

`share_with_group_lock` Prevent sharing a project with another group within this group:
```yaml
mygroup/:
  share_with_group_lock: true # or false
```

`mentions_disabled` Disable the capability of a group from getting mentioned:
```yaml
mygroup/:
  mentions_disabled: true # or false
```

`emails_enabled` Enable email notifications:
```yaml
mygroup/:
  emails_enabled: true # or false
```

`ip_restriction_ranges` Comma-separated list of IP addresses or subnet masks to restrict group access:
```yaml
mygroup/:
  ip_restriction_ranges: My ip restriction ranges
```

`allowed_email_domains_list` Comma-separated list of email address domains to allow group access:
```yaml
mygroup/:
  allowed_email_domains_list: My allowed email domains list
```

`wiki_access_level` The wiki access level:
```yaml
mygroup/:
  wiki_access_level: disabled # one of disabled, private, enabled
```

`lfs_enabled` Enable/disable Large File Storage (LFS) for the projects in this group:
```yaml
mygroup/:
  lfs_enabled: true # or false
```

`enabled_git_access_protocol` Enabled protocols for Git access:
```yaml
mygroup/:
  enabled_git_access_protocol: ssh # one of ssh, http, all
```

`project_creation_level` Determine if developers can create projects in the group:
```yaml
mygroup/:
  project_creation_level: noone # one of noone, maintainer, developer
```

`subgroup_creation_level` Allowed to create subgroups:
```yaml
mygroup/:
  subgroup_creation_level: owner # one of owner, maintainer
```

`prevent_forking_outside_group` When enabled, users can not fork projects from this group to external namespaces:
```yaml
mygroup/:
  prevent_forking_outside_group: true # or false
```

`require_two_factor_authentication` Require all users in this group to setup Two-factor authentication:
```yaml
mygroup/:
  require_two_factor_authentication: true # or false
```

`two_factor_grace_period` Time before Two-factor authentication is enforced (in hours):
```yaml
mygroup/:
  two_factor_grace_period: 42
```

`request_access_enabled` Allow users to request member access:
```yaml
mygroup/:
  request_access_enabled: true # or false
```

`membership_lock` Prevent adding new members to project membership within this group:
```yaml
mygroup/:
  membership_lock: true # or false
```

## GitLab Duo features

`duo_features_enabled` ndicates whether GitLab Duo features are enabled for this group:
```yaml
mygroup/:
  duo_features_enabled: true # or false
```

`lock_duo_features_enabled` Indicates whether the GitLab Duo features enabled setting is enforced for all subgroups:
```yaml
mygroup/:
  lock_duo_features_enabled: true # or false
```

## Repository Settings

### Default branch

`default_branch` The default branch name for group's projects:
```yaml
mygroup/:
  default_branch: My default branch
```

## CI / CD Settings

### Variables

`variables` The list of group's variables:
```yaml
mygroup/:
  variables:
    - key: DAST_DISABLED
      value: '1'
      description: Disabled SAST
      masked: false
      protected: false
      raw: false  # Expand variables
      environment_scope: '*'
      variable_type: env_var

```

`unknown_variables` What to do with unknown variables (`warn` by default):
```yaml
mygroup/:
  unknown_variables: warn # one of warn, delete, remove, ignore, skip
```

### Runners

`shared_runners_setting` Enable or disable shared runners for a group's subgroups and projects:
```yaml
mygroup/:
  shared_runners_setting: enabled # one of enabled, disabled_and_overridable, disabled_and_unoverridable
```

### Auto DevOps

`auto_devops_enabled` Default to Auto DevOps pipeline for all projects within this group:
```yaml
mygroup/:
  auto_devops_enabled: true # or false
```

# Deprecated

`emails_disabled` Disable email notifications:
```yaml
mygroup/:
  emails_disabled: true # or false
```

# Undocumented

`extra_shared_runners_minutes_limit` (admin-only) Extra pipeline minutes quota for this group:
```yaml
mygroup/:
  extra_shared_runners_minutes_limit: 42
```

`file_template_project_id` (Premium) The ID of a project to load custom file templates from:
```yaml
mygroup/:
  file_template_project_id: 42
```

`shared_runners_minutes_limit` (admin-only) Pipeline minutes quota for this group:
```yaml
mygroup/:
  shared_runners_minutes_limit: 42
```


