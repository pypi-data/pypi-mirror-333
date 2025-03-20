# Table of Contents <!-- omit in toc -->

- [Project lifecycle](#project-lifecycle)
- [Manage](#manage)
  - [Members](#members)
  - [Labels](#labels)
- [Plan](#plan)
  - [Issue boards](#issue-boards)
  - [Milestones](#milestones)
- [Code](#code)
  - [Branches](#branches)
- [Build](#build)
  - [Pipeline schedules](#pipeline-schedules)
- [Settings](#settings)
  - [General Settings](#general-settings)
    - [Naming, description, topics](#naming-description-topics)
    - [Visibility, project features, permissions](#visibility-project-features-permissions)
    - [Default description template for issues](#default-description-template-for-issues)
    - [Service Desk](#service-desk)
    - [Advanced](#advanced)
  - [Webhooks](#webhooks)
  - [Repository](#repository)
    - [Branch defaults](#branch-defaults)
    - [Mirroring repositories](#mirroring-repositories)
    - [Protected Branches](#protected-branches)
    - [Protected Tags](#protected-tags)
  - [Merge requests](#merge-requests)
    - [Merge requests](#merge-requests)
    - [Merge request approvals](#merge-request-approvals)
  - [CI / CD Settings](#ci-cd-settings)
    - [General pipelines](#general-pipelines)
    - [Auto DevOps](#auto-devops)
    - [Protected Environments](#protected-environments)
    - [Runners](#runners)
    - [Artifacts](#artifacts)
    - [Variables](#variables)
  - [Packages and registries](#packages-and-registries)
    - [Cleanup policies](#cleanup-policies)
- [Mirroring repositories, packages and container images](#mirroring-repositories-packages-and-container-images)
- [Deprecated](#deprecated)
- [Undocumented](#undocumented)

# Project lifecycle

`gitlab_id` GitLab id:
```yaml
mygroup/myproject:
  gitlab_id: gitlab
```

More information can be found [here](action_file.md#gitlab_id)

`create_object` Create object if it does not exists:
```yaml
mygroup/myproject:
  create_object: true # or false
```

`delete_object` Delete object if it exists:
```yaml
mygroup/myproject:
  delete_object: true # or false
```

`initialize_with_readme` false by default:
```yaml
mygroup/myproject:
  initialize_with_readme: true # or false
```

`repository_object_format` Repository object format:
```yaml
mygroup/myproject:
  repository_object_format: sha1 # one of sha1, sha256
```

# Manage

## Members

`members` Members:
```yaml
mygroup/myproject:
  members:
    foo: developer
    bar: maintainer # one of guest, reporter, developer, maintainer, owner

```

`unknown_members` What to do with unknown members (`warn` by default):
```yaml
mygroup/myproject:
  unknown_members: warn # one of warn, delete, remove, ignore, skip
```

`groups` Groups:
```yaml
mygroup/myproject:
  groups:
    group/foo: guest
    group/bar: reporter # one of guest, reporter, developer, maintainer

```

`unknown_groups` What to do with unknown groups (`warn` by default):
```yaml
mygroup/myproject:
  unknown_groups: warn # one of warn, delete, remove, ignore, skip
```

## Labels

`labels` The list of project's labels:
```yaml
mygroup/myproject:
  labels:
    - name: critical
      priority: 0
    - name: bug
      priority: 1
    - name: confirmed
      priority: 2

```

`unknown_labels` What to do with unknown labels (`warn` by default):
```yaml
mygroup/myproject:
  unknown_labels: warn # one of warn, delete, remove, ignore, skip
```

# Plan

## Issue boards

`boards` The list of project's boards:
```yaml
mygroup/myproject:
  boards:
    - name: My Board
      # old_name: Development # Use this to rename a board
      hide_backlog_list: false
      hide_closed_list: false
      lists:
        - label: TODO
        - label: WIP

```

`unknown_boards` What to do with unknown boards (`warn` by default):
```yaml
mygroup/myproject:
  unknown_boards: warn # one of warn, delete, remove, ignore, skip
```

`unknown_board_lists` What to do with unknown board lists (`delete` by default):
```yaml
mygroup/myproject:
  unknown_board_lists: warn # one of warn, delete, remove, ignore, skip
```

## Milestones

`milestones` The list of project's milestones:
```yaml
mygroup/myproject:
  milestones:
    - title: '1.0'
      description: Version 1.0
      due_date: '2021-01-23' # Quotes are mandatory
      start_date: '2020-01-23' # Quotes are mandatory
      state: active # or closed

```

`unknown_milestones` What to do with unknown milestones (`warn` by default):
```yaml
mygroup/myproject:
  unknown_milestones: warn # one of warn, delete, remove, ignore, skip
```

# Code

## Branches

`branches` The list of branches for a project. Branches are created in order:
```yaml
mygroup/myproject:
  branches:
    - main
    - develop
```

`rename_branches` Rename branches of a project. Rename pairs (old_name: new_name) are processed in order:
```yaml
mygroup/myproject:
  rename_branches:
    - old_name: new_name
    # To Rename consecutive branches:
    - branch2: branch3
    - branch1: branch2
```

# Build

## Pipeline schedules

`pipeline_schedules` The list of project's pipeline schedules:
```yaml
mygroup/myproject:
  pipeline_schedules:
    - description: Build packages
      ref: main
      cron: '0 1 * * 5'
      # cron_timezone: UTC
      # active: true
      variables:
        - key: MY_VAR
          value: my value
          # variable_type: env_var # or file
      # unknown_variables: warn # one of warn, delete, remove, ignore, skip

```

`unknown_pipeline_schedules` What to do with unknown pipeline schedules (`warn` by default):
```yaml
mygroup/myproject:
  unknown_pipeline_schedules: warn # one of warn, delete, remove, ignore, skip
```

`unknown_pipeline_schedule_variables` What to do with unknown pipeline schedule variables (`warn` by default):
```yaml
mygroup/myproject:
  unknown_pipeline_schedule_variables: warn # one of warn, delete, remove, ignore, skip
```

# Settings

## General Settings

### Naming, description, topics

`name` Project name:
```yaml
mygroup/myproject:
  name: My name
```

`description` Project description:
```yaml
mygroup/myproject:
  description: |-
    🧹 GitLabracadabra 🧙

    :alembic: Adds some magic to GitLab :crystal\_ball:
```

`topics` Topics:
```yaml
mygroup/myproject:
  topics: [GitLab, API, YAML]
```

### Visibility, project features, permissions

`visibility` Project visibility:
```yaml
mygroup/myproject:
  visibility: private # one of private, internal, public
```

`request_access_enabled` Allow users to request access:
```yaml
mygroup/myproject:
  request_access_enabled: true # or false
```

`issues_access_level` Set visibility of issues:
```yaml
mygroup/myproject:
  issues_access_level: disabled # one of disabled, private, enabled
```

`repository_access_level` Set visibility of repository:
```yaml
mygroup/myproject:
  repository_access_level: disabled # one of disabled, private, enabled
```

`merge_requests_access_level` Set visibility of merge requests:
```yaml
mygroup/myproject:
  merge_requests_access_level: disabled # one of disabled, private, enabled
```

`forking_access_level` Set visibility of forks:
```yaml
mygroup/myproject:
  forking_access_level: disabled # one of disabled, private, enabled
```

`lfs_enabled` Enable LFS:
```yaml
mygroup/myproject:
  lfs_enabled: true # or false
```

`builds_access_level` Set visibility of pipelines:
```yaml
mygroup/myproject:
  builds_access_level: disabled # one of disabled, private, enabled
```

`container_registry_access_level` Set visibility of container registry:
```yaml
mygroup/myproject:
  container_registry_access_level: disabled # one of disabled, private, enabled
```

`analytics_access_level` Set visibility of analytics:
```yaml
mygroup/myproject:
  analytics_access_level: disabled # one of disabled, private, enabled
```

`requirements_access_level` Set visibility of requirements management:
```yaml
mygroup/myproject:
  requirements_access_level: disabled # one of disabled, private, enabled
```

`security_and_compliance_access_level` Set visibility of security and compliance:
```yaml
mygroup/myproject:
  security_and_compliance_access_level: disabled # one of disabled, private, enabled
```

`wiki_access_level` Set visibility of wiki:
```yaml
mygroup/myproject:
  wiki_access_level: disabled # one of disabled, private, enabled
```

`snippets_access_level` Set visibility of snippets:
```yaml
mygroup/myproject:
  snippets_access_level: disabled # one of disabled, private, enabled
```

`packages_enabled` Enable or disable packages repository feature:
```yaml
mygroup/myproject:
  packages_enabled: true # or false
```

`model_experiments_access_level` Set visibility of machine learning model experiments:
```yaml
mygroup/myproject:
  model_experiments_access_level: disabled # one of disabled, private, enabled
```

`model_registry_access_level` Set visibility of machine learning model registry:
```yaml
mygroup/myproject:
  model_registry_access_level: disabled # one of disabled, private, enabled
```

`pages_access_level` Set visibility of GitLab Pages:
```yaml
mygroup/myproject:
  pages_access_level: disabled # one of disabled, private, enabled, public
```

`monitor_access_level` Set visibility of application performance monitoring:
```yaml
mygroup/myproject:
  monitor_access_level: disabled # one of disabled, private, enabled
```

`environments_access_level` Set visibility of environments:
```yaml
mygroup/myproject:
  environments_access_level: disabled # one of disabled, private, enabled
```

`feature_flags_access_level` Set visibility of feature flags:
```yaml
mygroup/myproject:
  feature_flags_access_level: disabled # one of disabled, private, enabled
```

`infrastructure_access_level` Set visibility of infrastructure management:
```yaml
mygroup/myproject:
  infrastructure_access_level: disabled # one of disabled, private, enabled
```

`releases_access_level` Set visibility of releases:
```yaml
mygroup/myproject:
  releases_access_level: disabled # one of disabled, private, enabled
```

`emails_enabled` Enable email notifications:
```yaml
mygroup/myproject:
  emails_enabled: true # or false
```

### Default description template for issues

`issues_template` Default description for Issues:
```yaml
mygroup/myproject:
  issues_template: My issues template
```

### Service Desk

`service_desk_enabled` Enable or disable Service Desk feature:
```yaml
mygroup/myproject:
  service_desk_enabled: true # or false
```

### Advanced

`archived` Archive or unarchive project:
```yaml
mygroup/myproject:
  archived: true # or false
```

## Webhooks

`webhooks` The list of project's webhooks:
```yaml
mygroup/myproject:
  webhooks:
    - url: http://example.com/api/trigger
      push_events: true
      push_events_branch_filter: ''
      issues_events: true
      confidential_issues_events: true
      merge_requests_events: true
      tag_push_events: true
      note_events: true
      confidential_note_events: true
      job_events: true
      pipeline_events: true
      wiki_page_events: true
      enable_ssl_verification: true
      # token: T0k3N

```

`unknown_webhooks` What to do with unknown webhooks (`warn` by default):
```yaml
mygroup/myproject:
  unknown_webhooks: warn # one of warn, delete, remove, ignore, skip
```

## Repository

### Branch defaults

`default_branch` The default branch name:
```yaml
mygroup/myproject:
  default_branch: My default branch
```

`autoclose_referenced_issues` Set whether auto-closing referenced issues on default branch:
```yaml
mygroup/myproject:
  autoclose_referenced_issues: true # or false
```

`issue_branch_template` Template used to suggest names for branches created from issues:
```yaml
mygroup/myproject:
  issue_branch_template: My issue branch template
```

### Mirroring repositories

`mirror` Enables pull mirroring in a project:
```yaml
mygroup/myproject:
  mirror: true # or false
```

`import_url` URL to import repository from:
```yaml
mygroup/myproject:
  import_url: My import url
```

`mirror_user_id` User responsible for all the activity surrounding a pull mirror event:
```yaml
mygroup/myproject:
  mirror_user_id: 42
```

`mirror_overwrites_diverged_branches` Pull mirror overwrites diverged branches:
```yaml
mygroup/myproject:
  mirror_overwrites_diverged_branches: true # or false
```

`mirror_trigger_builds` Pull mirroring triggers builds:
```yaml
mygroup/myproject:
  mirror_trigger_builds: true # or false
```

`only_mirror_protected_branches` Only mirror protected branches:
```yaml
mygroup/myproject:
  only_mirror_protected_branches: true # or false
```

### Protected Branches

`protected_branches` Protected branches:
```yaml
mygroup/myproject:
  protected_branches:
    main:
      allowed_to_merge::
        - role: developer  # one of noone, developer, maintainer, admin
        - user: my_username  # EE only
        - group: my_group  # EE only
      allowed_to_push::
        - role: noone  # one of noone, developer, maintainer, admin
        - user: my_username  # EE only
        - group: my_group  # EE only
        - deploy_key: Deploy Key Title  # EE only
      allow_force_push: false
      code_owner_approval_required: false  # EE only
      allowed_to_unprotect:  # EE only
        - role: maintainer  # one of developer, maintainer, admin
        - user: my_username
        - group: my_group
    develop:
      merge_access_level: developer
      push_access_level: developer

```

`unknown_protected_branches` What to do with unknown protected branches (`warn` by default):
```yaml
mygroup/myproject:
  unknown_protected_branches: warn # one of warn, delete, remove, ignore, skip
```

### Protected Tags

`protected_tags` Protected tags:
```yaml
mygroup/myproject:
  protected_tags:
    v*: maintainer # one of noone, developer, maintainer
    *: developer # one of noone, developer, maintainer

```

`unknown_protected_tags` What to do with unknown protected tags (`warn` by default):
```yaml
mygroup/myproject:
  unknown_protected_tags: warn # one of warn, delete, remove, ignore, skip
```

## Merge requests

### Merge requests

`merge_method` Set the merge method used:
```yaml
mygroup/myproject:
  merge_method: merge # one of merge, rebase_merge, ff
```

`merge_pipelines_enabled` Enable or disable merged results pipelines:
```yaml
mygroup/myproject:
  merge_pipelines_enabled: true # or false
```

`merge_trains_enabled` Enable or disable merge trains:
```yaml
mygroup/myproject:
  merge_trains_enabled: true # or false
```

`resolve_outdated_diff_discussions` Automatically resolve merge request diffs discussions on lines changed with a push:
```yaml
mygroup/myproject:
  resolve_outdated_diff_discussions: true # or false
```

`printing_merge_request_link_enabled` Show link to create/view merge request when pushing from the command line:
```yaml
mygroup/myproject:
  printing_merge_request_link_enabled: true # or false
```

`remove_source_branch_after_merge` Enable Delete source branch option by default for all new merge requests:
```yaml
mygroup/myproject:
  remove_source_branch_after_merge: true # or false
```

`squash_option` Squash option:
```yaml
mygroup/myproject:
  squash_option: never # one of never, always, default_on, default_off
```

`only_allow_merge_if_pipeline_succeeds` Set whether merge requests can only be merged with successful jobs:
```yaml
mygroup/myproject:
  only_allow_merge_if_pipeline_succeeds: true # or false
```

`allow_merge_on_skipped_pipeline` Set whether or not merge requests can be merged with skipped jobs:
```yaml
mygroup/myproject:
  allow_merge_on_skipped_pipeline: true # or false
```

`only_allow_merge_if_all_discussions_are_resolved` Set whether merge requests can only be merged when all the discussions are resolved:
```yaml
mygroup/myproject:
  only_allow_merge_if_all_discussions_are_resolved: true # or false
```

`only_allow_merge_if_all_status_checks_passed` Indicates that merges of merge requestsshould be blocked unless all status checks have passed:
```yaml
mygroup/myproject:
  only_allow_merge_if_all_status_checks_passed: true # or false
```

`suggestion_commit_message` The commit message used to apply merge request suggestions:
```yaml
mygroup/myproject:
  suggestion_commit_message: My suggestion commit message
```

`merge_commit_template` Template used to create merge commit message in merge requests:
```yaml
mygroup/myproject:
  merge_commit_template: My merge commit template
```

`squash_commit_template` Template used to create squash commit message in merge requests:
```yaml
mygroup/myproject:
  squash_commit_template: My squash commit template
```

`merge_requests_template` Default description for merge requests:
```yaml
mygroup/myproject:
  merge_requests_template: My merge requests template
```

### Merge request approvals

`approvals_before_merge` How many approvers should approve merge request by default:
```yaml
mygroup/myproject:
  approvals_before_merge: 42
```

## CI / CD Settings

### General pipelines

`public_jobs` If true, jobs can be viewed by non-project members:
```yaml
mygroup/myproject:
  public_jobs: true # or false
```

`auto_cancel_pending_pipelines` Auto-cancel pending pipelines:
```yaml
mygroup/myproject:
  auto_cancel_pending_pipelines: enabled # one of enabled, disabled
```

`ci_forward_deployment_enabled` Enable or disable prevent outdated deployment jobs:
```yaml
mygroup/myproject:
  ci_forward_deployment_enabled: true # or false
```

`ci_forward_deployment_rollback_allowed` Enable or disable allow job retries for rollback deployments:
```yaml
mygroup/myproject:
  ci_forward_deployment_rollback_allowed: true # or false
```

`ci_separated_caches` Set whether or not caches should be separated by branch protection status:
```yaml
mygroup/myproject:
  ci_separated_caches: true # or false
```

`ci_restrict_pipeline_cancellation_role` Set the role required to cancel a pipeline or job:
```yaml
mygroup/myproject:
  ci_restrict_pipeline_cancellation_role: developer # one of developer, maintainer, no_one
```

`ci_config_path` The path to CI config file:
```yaml
mygroup/myproject:
  ci_config_path: debian/salsa-ci.yml
```

`build_git_strategy` The Git strategy:
```yaml
mygroup/myproject:
  build_git_strategy: fetch # one of fetch, clone
```

`ci_default_git_depth` Default number of revisions for shallow cloning:
```yaml
mygroup/myproject:
  ci_default_git_depth: 42
```

`build_timeout` The maximum amount of time in minutes that a job is able run (in seconds):
```yaml
mygroup/myproject:
  build_timeout: 42
```

`ci_allow_fork_pipelines_to_run_in_parent_project` Enable or disable running pipelines in the parent project for merge requests from forks:
```yaml
mygroup/myproject:
  ci_allow_fork_pipelines_to_run_in_parent_project: true # or false
```

### Auto DevOps

`auto_devops_enabled` Enable Auto DevOps for this project:
```yaml
mygroup/myproject:
  auto_devops_enabled: true # or false
```

`auto_devops_deploy_strategy` Auto Deploy strategy:
```yaml
mygroup/myproject:
  auto_devops_deploy_strategy: continuous # one of continuous, manual, timed_incremental
```

### Protected Environments

`allow_pipeline_trigger_approve_deployment` Set whether or not a pipeline triggerer is allowed to approve deployments:
```yaml
mygroup/myproject:
  allow_pipeline_trigger_approve_deployment: true # or false
```

### Runners

`shared_runners_enabled` Enable shared runners for this project:
```yaml
mygroup/myproject:
  shared_runners_enabled: true # or false
```

`group_runners_enabled` Enable group runners for this project:
```yaml
mygroup/myproject:
  group_runners_enabled: true # or false
```

### Artifacts

`keep_latest_artifact` Disable or enable the ability to keep the latest artifact for this project:
```yaml
mygroup/myproject:
  keep_latest_artifact: true # or false
```

### Variables

`variables` The list of project's variables:
```yaml
mygroup/myproject:
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
mygroup/myproject:
  unknown_variables: warn # one of warn, delete, remove, ignore, skip
```

## Packages and registries

### Cleanup policies

`container_expiration_policy` Update the image cleanup policy for this project:
```yaml
mygroup/myproject:
  container_expiration_policy:
    enabled: true
    cadence: 7d  # 1d, 7d, 14d, 1month, 3month
    keep_n: 10  # 1, 5, 10, 25, 50, 100
    name_regex_keep: '.*main|.*release|release-.*|main-.*'
    older_than: 90d  # 7d, 14d, 30d, 90d
    name_regex_delete: '.*'

```

# Mirroring repositories, packages and container images

`mirrors` The list of project's mirrors:
```yaml
mygroup/myproject:
  mirrors:
    - url: https://gitlab.com/gitlabracadabra/gitlabracadabra.git
      # auth_id: gitlab # Section from .python-gitlab.cfg for authentication
      direction: pull # one of pull, push ; only first pull mirror is processed
      push_options: [ci.skip]
      branches: # if you omit this parameter, all branches are mirrored
        - from: '/wip-.*/'
          to: '' # This will skip those branches
        - from: main
          # to: main # implicitly equal to source branch
          # push_options: [] # inherited by default
        # Using regexps
        - from: '/(.*)/'
          to: 'upstream/\1'
      tags: # if you omit this parameter, all tags are mirrored
        - from: '/v(.*)/i'
          to: 'upstream-\1'
          # push_options: [] # inherited by default
  builds_access_level: disabled # If you want to prevent triggering pipelines on push
```

More information can be found [here](mirrors.md)

`package_mirrors` Package image mirrors:
```yaml
mygroup/myproject:
  package_mirrors:
    - raw:
        default_url: https://download.docker.com/linux/debian/gpg
        default_package_name: docker
        default_package_version: '0'

```

More information can be found [here](package_mirrors.md)

`image_mirrors` Container image mirrors:
```yaml
mygroup/myproject:
  image_mirrors:
    # Mirror debian:bookworm
    # ... to registry.example.org/mygroup/myproject/library/debian:bookworm:
    - from: 'debian:bookworm'
    # Overriding destination:
    - from: 'quay.org/coreos/etcd:v3.4.1'
      to: 'etcd:v3.4.1' # Default would be coreos/etcd:v3.4.1

```

More information can be found [here](image_mirrors.md)

# Deprecated

`build_coverage_regex` (Removed) Test coverage parsing:
```yaml
mygroup/myproject:
  build_coverage_regex: My build coverage regex
```

`container_registry_enabled` (Deprecated) Enable container registry for this project. Use container_registry_access_level instead:
```yaml
mygroup/myproject:
  container_registry_enabled: true # or false
```

`emails_disabled` (Deprecated) Disable email notifications. Use emails_enabled instead:
```yaml
mygroup/myproject:
  emails_disabled: true # or false
```

`issues_enabled` (Deprecated) Enable issues for this project. Use issues_access_level instead:
```yaml
mygroup/myproject:
  issues_enabled: true # or false
```

`jobs_enabled` (Deprecated) Enable jobs for this project. Use builds_access_level instead:
```yaml
mygroup/myproject:
  jobs_enabled: true # or false
```

`merge_requests_enabled` (Deprecated) Enable merge requests for this project. Use merge_requests_access_level instead:
```yaml
mygroup/myproject:
  merge_requests_enabled: true # or false
```

`public_builds` (Deprecated) If true, jobs can be viewed by non-project members. Use public_jobs instead:
```yaml
mygroup/myproject:
  public_builds: true # or false
```

`snippets_enabled` (Deprecated) Enable snippets for this project. Use snippets_access_level instead:
```yaml
mygroup/myproject:
  snippets_enabled: true # or false
```

`tag_list` (Deprecated in GitLab 14.0) The list of tags for a project; put array of tags, that should be finally assigned to a project. Use topics instead:
```yaml
mygroup/myproject:
  tag_list: [GitLab, API, YAML]
```

`wiki_enabled` (Deprecated) Enable wiki for this project. Use wiki_access_level instead:
```yaml
mygroup/myproject:
  wiki_enabled: true # or false
```

# Undocumented

`external_authorization_classification_label` The classification label for the project:
```yaml
mygroup/myproject:
  external_authorization_classification_label: My external authorization classification label
```

`repository_storage` Which storage shard the repository is on. Available only to admins:
```yaml
mygroup/myproject:
  repository_storage: My repository storage
```


