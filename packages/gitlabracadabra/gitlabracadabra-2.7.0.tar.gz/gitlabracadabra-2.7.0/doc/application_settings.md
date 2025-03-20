# Table of Contents <!-- omit in toc -->

- [Application settings lifecycle](#application-settings-lifecycle)
- [Undocumented](#undocumented)

# Application settings lifecycle

`gitlab_id` GitLab id:
```yaml
application_settings:
  type: application-settings
  gitlab_id: gitlab
```

More information can be found [here](action_file.md#gitlab_id)

# Undocumented

`admin_mode` Require administrators to enable Admin Mode by re-authenticating for administrative tasks:
```yaml
application_settings:
  type: application-settings
  admin_mode: true # or false
```

`admin_notification_email` Abuse reports will be sent to this address if it is set. Abuse reports are always available in the admin area:
```yaml
application_settings:
  type: application-settings
  admin_notification_email: My admin notification email
```

`after_sign_out_path` Where to redirect users after logout:
```yaml
application_settings:
  type: application-settings
  after_sign_out_path: My after sign out path
```

`after_sign_up_text` Text shown to the user after signing up:
```yaml
application_settings:
  type: application-settings
  after_sign_up_text: My after sign up text
```

`akismet_api_key` API key for akismet spam protection:
```yaml
application_settings:
  type: application-settings
  akismet_api_key: My akismet api key
```

`akismet_enabled` Enable or disable akismet spam protection:
```yaml
application_settings:
  type: application-settings
  akismet_enabled: true # or false
```

`allow_group_owners_to_manage_ldap` Set to true to allow group owners to manage LDAP:
```yaml
application_settings:
  type: application-settings
  allow_group_owners_to_manage_ldap: true # or false
```

`allow_local_requests_from_hooks_and_services` Allow requests to the local network from hooks and services:
```yaml
application_settings:
  type: application-settings
  allow_local_requests_from_hooks_and_services: true # or false
```

`archive_builds_in_human_readable` Set the duration for which the jobs will be considered as old and expired. Once that time passes, the jobs will be archived and no longer able to be retried. Make it empty to never expire jobs. It has to be no less than 1 day, for example: `15 days`, `1 month`, `2 years`:
```yaml
application_settings:
  type: application-settings
  archive_builds_in_human_readable: My archive builds in human readable
```

`authorized_keys_enabled` By default, we write to the authorized_keys file to support Git over SSH without additional configuration. GitLab can be optimized to authenticate SSH keys via the database file. Only disable this if you have configured your OpenSSH server to use the AuthorizedKeysCommand:
```yaml
application_settings:
  type: application-settings
  authorized_keys_enabled: true # or false
```

`auto_devops_domain` Specify a domain to use by default for every project's Auto Review Apps and Auto Deploy stages:
```yaml
application_settings:
  type: application-settings
  auto_devops_domain: My auto devops domain
```

`auto_devops_enabled` Enable Auto DevOps for projects by default. It will automatically build, test, and deploy applications based on a predefined CI/CD configuration:
```yaml
application_settings:
  type: application-settings
  auto_devops_enabled: true # or false
```

`can_create_group` Indicates whether users can create top-level groups. Introduced in GitLab 15.5. Defaults to true:
```yaml
application_settings:
  type: application-settings
  can_create_group: true # or false
```

`check_namespace_plan` Enabling this will make only licensed EE features available to projects if the project namespace's plan includes the feature or if the project is public:
```yaml
application_settings:
  type: application-settings
  check_namespace_plan: true # or false
```

`commit_email_hostname`  Custom hostname (for private commit emails):
```yaml
application_settings:
  type: application-settings
  commit_email_hostname: My commit email hostname
```

`container_registry_token_expire_delay` Container Registry token duration in minutes:
```yaml
application_settings:
  type: application-settings
  container_registry_token_expire_delay: 42
```

`default_artifacts_expire_in` Set the default expiration time for each job's artifacts:
```yaml
application_settings:
  type: application-settings
  default_artifacts_expire_in: My default artifacts expire in
```

`default_branch_protection` Determine if developers can push to default branch. Can take: 0 (not protected, both developers and maintainers can push new commits, force push, or delete the branch), 1 (partially protected, developers and maintainers can push new commits, but cannot force push or delete the branch) or 2 (fully protected, developers cannot push new commits, but maintainers can; no-one can force push or delete the branch) as a parameter. Default is 2:
```yaml
application_settings:
  type: application-settings
  default_branch_protection: 0 # one of 0, 1, 2, 3
```

`default_ci_config_path` Default CI configuration path for new projects:
```yaml
application_settings:
  type: application-settings
  default_ci_config_path: My default ci config path
```

`default_group_visibility` What visibility level new groups receive. Can take private, internal and public as a parameter. Default is private:
```yaml
application_settings:
  type: application-settings
  default_group_visibility: private # one of private, internal, public
```

`default_project_creation` Default project creation protection. Can take: `0` _(No one)_, `1` _(Maintainers)_ or `2` _(Developers + Maintainers)_:
```yaml
application_settings:
  type: application-settings
  default_project_creation: 0 # one of 0, 1, 2
```

`default_project_visibility` What visibility level new projects receive. Can take `private`, `internal` and `public` as a parameter:
```yaml
application_settings:
  type: application-settings
  default_project_visibility: private # one of private, internal, public
```

`default_projects_limit` Project limit per user:
```yaml
application_settings:
  type: application-settings
  default_projects_limit: 42
```

`default_snippet_visibility` What visibility level new snippets receive. Can take private, internal and public as a parameter. Default is private:
```yaml
application_settings:
  type: application-settings
  default_snippet_visibility: private # one of private, internal, public
```

`diff_max_patch_bytes` Maximum diff patch size (Bytes):
```yaml
application_settings:
  type: application-settings
  diff_max_patch_bytes: 42
```

`disabled_oauth_sign_in_sources` Disabled OAuth sign-in sources:
```yaml
application_settings:
  type: application-settings
  disabled_oauth_sign_in_sources: [My disabled oauth sign in sources]
```

`dns_rebinding_protection_enabled` Enforce DNS rebinding attack protection:
```yaml
application_settings:
  type: application-settings
  dns_rebinding_protection_enabled: true # or false
```

`domain_blacklist` Users with e-mail addresses that match these domain(s) will NOT be able to sign-up. Wildcards allowed. Use separate lines for multiple entries. Ex: domain.com, *.domain.com:
```yaml
application_settings:
  type: application-settings
  domain_blacklist: [My domain blacklist]
```

`domain_blacklist_enabled` Allows blocking sign-ups from emails from specific domains:
```yaml
application_settings:
  type: application-settings
  domain_blacklist_enabled: true # or false
```

`domain_whitelist` Force people to use only corporate emails for sign-up. Default is null, meaning there is no restriction:
```yaml
application_settings:
  type: application-settings
  domain_whitelist: [My domain whitelist]
```

`dsa_key_restriction` The minimum allowed bit length of an uploaded DSA key. Default is 0 (no restriction). -1 disables DSA keys:
```yaml
application_settings:
  type: application-settings
  dsa_key_restriction: 42
```

`ecdsa_key_restriction` The minimum allowed curve size (in bits) of an uploaded ECDSA key. Default is 0 (no restriction). -1 disables ECDSA keys:
```yaml
application_settings:
  type: application-settings
  ecdsa_key_restriction: 42
```

`ed25519_key_restriction` The minimum allowed curve size (in bits) of an uploaded ED25519 key. Default is 0 (no restriction). -1 disables ED25519 keys:
```yaml
application_settings:
  type: application-settings
  ed25519_key_restriction: 42
```

`elasticsearch_aws` Enable the use of AWS hosted Elasticsearch:
```yaml
application_settings:
  type: application-settings
  elasticsearch_aws: true # or false
```

`elasticsearch_aws_access_key` AWS IAM access key:
```yaml
application_settings:
  type: application-settings
  elasticsearch_aws_access_key: My elasticsearch aws access key
```

`elasticsearch_aws_region` The AWS region the elasticsearch domain is configured:
```yaml
application_settings:
  type: application-settings
  elasticsearch_aws_region: My elasticsearch aws region
```

`elasticsearch_aws_secret_access_key` AWS IAM secret access key:
```yaml
application_settings:
  type: application-settings
  elasticsearch_aws_secret_access_key: My elasticsearch aws secret access key
```

`elasticsearch_experimental_indexer` Use the experimental elasticsearch indexer. More info: https://gitlab.com/gitlab-org/gitlab-elasticsearch-indexer :
```yaml
application_settings:
  type: application-settings
  elasticsearch_experimental_indexer: true # or false
```

`elasticsearch_indexing` Enable Elasticsearch indexing:
```yaml
application_settings:
  type: application-settings
  elasticsearch_indexing: true # or false
```

`elasticsearch_limit_indexing` Limit Elasticsearch to index certain namespaces and projects:
```yaml
application_settings:
  type: application-settings
  elasticsearch_limit_indexing: true # or false
```

`elasticsearch_namespace_ids` The namespaces to index via Elasticsearch if elasticsearch_limit_indexing is enabled:
```yaml
application_settings:
  type: application-settings
  elasticsearch_namespace_ids: [My elasticsearch namespace ids]
```

`elasticsearch_project_ids` The projects to index via Elasticsearch if elasticsearch_limit_indexing is enabled:
```yaml
application_settings:
  type: application-settings
  elasticsearch_project_ids: [My elasticsearch project ids]
```

`elasticsearch_search` Enable Elasticsearch search:
```yaml
application_settings:
  type: application-settings
  elasticsearch_search: true # or false
```

`elasticsearch_url` The url to use for connecting to Elasticsearch. Use a comma-separated list to support cluster (e.g., http://localhost:9200, http://localhost:9201). If your Elasticsearch instance is password protected, pass the username:password in the URL (e.g., http://<username>:<password>@<elastic_host>:9200/):
```yaml
application_settings:
  type: application-settings
  elasticsearch_url: My elasticsearch url
```

`email_additional_text` Additional text added to the bottom of every email for legal/auditing/compliance reasons:
```yaml
application_settings:
  type: application-settings
  email_additional_text: My email additional text
```

`email_author_in_body` Some email servers do not support overriding the email sender name. Enable this option to include the name of the author of the issue, merge request or comment in the email body instead:
```yaml
application_settings:
  type: application-settings
  email_author_in_body: true # or false
```

`enabled_git_access_protocol` Enabled protocols for Git access. Allowed values are: ssh, http, and nil to allow both protocols:
```yaml
application_settings:
  type: application-settings
  enabled_git_access_protocol: ssh # one of ssh, http, both
```

`enforce_terms` Enforce application ToS to all users:
```yaml
application_settings:
  type: application-settings
  enforce_terms: true # or false
```

`external_auth_client_cert` The certificate to use to authenticate with the external authorization service:
```yaml
application_settings:
  type: application-settings
  external_auth_client_cert: My external auth client cert
```

`external_auth_client_key` Private key for the certificate when authentication is required for the external authorization service, this is encrypted when stored:
```yaml
application_settings:
  type: application-settings
  external_auth_client_key: My external auth client key
```

`external_auth_client_key_pass` Passphrase to use for the private key when authenticating with the external service this is encrypted when stored:
```yaml
application_settings:
  type: application-settings
  external_auth_client_key_pass: My external auth client key pass
```

`external_authorization_service_default_label` The default classification label to use when requesting authorization and no classification label has been specified on the project:
```yaml
application_settings:
  type: application-settings
  external_authorization_service_default_label: My external authorization service default label
```

`external_authorization_service_enabled` Enable using an external authorization service for accessing projects:
```yaml
application_settings:
  type: application-settings
  external_authorization_service_enabled: true # or false
```

`external_authorization_service_timeout` The timeout after which an authorization request is aborted, in seconds. When a request times out, access is denied to the user. (min: 0.001, max: 10, step: 0.001):
```yaml
application_settings:
  type: application-settings
  external_authorization_service_timeout: My external authorization service timeout
```

`external_authorization_service_url` URL to which authorization requests will be directed:
```yaml
application_settings:
  type: application-settings
  external_authorization_service_url: My external authorization service url
```

`file_template_project_id` The ID of a project to load custom file templates from:
```yaml
application_settings:
  type: application-settings
  file_template_project_id: 42
```

`first_day_of_week` Start day of the week for calendar views and date pickers:
```yaml
application_settings:
  type: application-settings
  first_day_of_week: sunday # one of sunday, monday, saturday
```

`geo_node_allowed_ips` Comma-separated list of IPs and CIDRs of allowed secondary nodes. For example, 1.1.1.1, 2.2.2.0/24:
```yaml
application_settings:
  type: application-settings
  geo_node_allowed_ips: My geo node allowed ips
```

`geo_status_timeout` The amount of seconds after which a request to get a secondary node status will time out:
```yaml
application_settings:
  type: application-settings
  geo_status_timeout: 42
```

`gitaly_timeout_default` Default Gitaly timeout, in seconds. This timeout is not enforced for git fetch/push operations or Sidekiq jobs. Set to 0 to disable timeouts:
```yaml
application_settings:
  type: application-settings
  gitaly_timeout_default: 42
```

`gitaly_timeout_fast` Gitaly fast operation timeout, in seconds. Some Gitaly operations are expected to be fast. If they exceed this threshold, there may be a problem with a storage shard and 'failing fast' can help maintain the stability of the GitLab instance. Set to 0 to disable timeouts:
```yaml
application_settings:
  type: application-settings
  gitaly_timeout_fast: 42
```

`gitaly_timeout_medium` Medium Gitaly timeout, in seconds. This should be a value between the Fast and the Default timeout. Set to 0 to disable timeouts:
```yaml
application_settings:
  type: application-settings
  gitaly_timeout_medium: 42
```

`grafana_enabled` Enable Grafana:
```yaml
application_settings:
  type: application-settings
  grafana_enabled: true # or false
```

`grafana_url` Grafana URL:
```yaml
application_settings:
  type: application-settings
  grafana_url: My grafana url
```

`gravatar_enabled` Enable Gravatar:
```yaml
application_settings:
  type: application-settings
  gravatar_enabled: true # or false
```

`hashed_storage_enabled` Create new projects using hashed storage paths: Enable immutable, hash-based paths and repository names to store repositories on disk. This prevents repositories from having to be moved or renamed when the Project URL changes and may improve disk I/O performance. (EXPERIMENTAL):
```yaml
application_settings:
  type: application-settings
  hashed_storage_enabled: true # or false
```

`help_page_hide_commercial_content` Hide marketing-related entries from help:
```yaml
application_settings:
  type: application-settings
  help_page_hide_commercial_content: true # or false
```

`help_page_support_url` Alternate support URL for help page:
```yaml
application_settings:
  type: application-settings
  help_page_support_url: My help page support url
```

`help_page_text` Custom text displayed on the help page:
```yaml
application_settings:
  type: application-settings
  help_page_text: My help page text
```

`help_text` GitLab server administrator information:
```yaml
application_settings:
  type: application-settings
  help_text: My help text
```

`hide_third_party_offers` Do not display offers from third parties within GitLab:
```yaml
application_settings:
  type: application-settings
  hide_third_party_offers: true # or false
```

`home_page_url` Redirect to this URL when not logged in:
```yaml
application_settings:
  type: application-settings
  home_page_url: My home page url
```

`housekeeping_enabled` Enable or disable git housekeeping:
```yaml
application_settings:
  type: application-settings
  housekeeping_enabled: true # or false
```

`housekeeping_full_repack_period` Number of Git pushes after which an incremental git repack is run:
```yaml
application_settings:
  type: application-settings
  housekeeping_full_repack_period: 42
```

`housekeeping_gc_period` Number of Git pushes after which git gc is run:
```yaml
application_settings:
  type: application-settings
  housekeeping_gc_period: 42
```

`housekeeping_incremental_repack_period` Number of Git pushes after which an incremental git repack is run:
```yaml
application_settings:
  type: application-settings
  housekeeping_incremental_repack_period: 42
```

`html_emails_enabled` Enable HTML emails:
```yaml
application_settings:
  type: application-settings
  html_emails_enabled: true # or false
```

`import_sources` Sources to allow project import from, possible values:
```yaml
application_settings:
  type: application-settings
  import_sources: [My import sources]
```

`instance_statistics_visibility_private` When set to true Instance statistics will only be available to admins:
```yaml
application_settings:
  type: application-settings
  instance_statistics_visibility_private: true # or false
```

`local_markdown_version` Increase this value when any cached markdown should be invalidated:
```yaml
application_settings:
  type: application-settings
  local_markdown_version: 42
```

`max_artifacts_size` Maximum artifacts size in MB:
```yaml
application_settings:
  type: application-settings
  max_artifacts_size: 42
```

`max_attachment_size` Limit attachment size in MB:
```yaml
application_settings:
  type: application-settings
  max_attachment_size: 42
```

`max_pages_size` Maximum size of pages repositories in MB:
```yaml
application_settings:
  type: application-settings
  max_pages_size: 42
```

`metrics_enabled` Enable influxDB metrics:
```yaml
application_settings:
  type: application-settings
  metrics_enabled: true # or false
```

`metrics_host` InfluxDB host:
```yaml
application_settings:
  type: application-settings
  metrics_host: My metrics host
```

`metrics_method_call_threshold` A method call is only tracked when it takes longer than the given amount of milliseconds:
```yaml
application_settings:
  type: application-settings
  metrics_method_call_threshold: 42
```

`metrics_packet_size` The amount of datapoints to send in a single UDP packet:
```yaml
application_settings:
  type: application-settings
  metrics_packet_size: 42
```

`metrics_pool_size` The amount of InfluxDB connections to keep open:
```yaml
application_settings:
  type: application-settings
  metrics_pool_size: 42
```

`metrics_port` The UDP port to use for connecting to InfluxDB:
```yaml
application_settings:
  type: application-settings
  metrics_port: 42
```

`metrics_sample_interval` The sampling interval in seconds:
```yaml
application_settings:
  type: application-settings
  metrics_sample_interval: 42
```

`metrics_timeout` The amount of seconds after which InfluxDB will time out:
```yaml
application_settings:
  type: application-settings
  metrics_timeout: 42
```

`mirror_available` Allow mirrors to be set up for projects. If disabled, only admins will be able to set up mirrors in projects:
```yaml
application_settings:
  type: application-settings
  mirror_available: true # or false
```

`mirror_capacity_threshold` Minimum capacity to be available before scheduling more mirrors preemptively:
```yaml
application_settings:
  type: application-settings
  mirror_capacity_threshold: 42
```

`mirror_max_capacity` Maximum number of mirrors that can be synchronizing at the same time:
```yaml
application_settings:
  type: application-settings
  mirror_max_capacity: 42
```

`mirror_max_delay` Maximum time (in minutes) between updates that a mirror can have when scheduled to synchronize:
```yaml
application_settings:
  type: application-settings
  mirror_max_delay: 42
```

`pages_domain_verification_enabled` Require users to prove ownership of custom domains. Domain verification is an essential security measure for public GitLab sites. Users are required to demonstrate they control a domain before it is enabled:
```yaml
application_settings:
  type: application-settings
  pages_domain_verification_enabled: true # or false
```

`password_authentication_enabled_for_git` Enable authentication for Git over HTTP(S) via a GitLab account password. Default is true:
```yaml
application_settings:
  type: application-settings
  password_authentication_enabled_for_git: true # or false
```

`password_authentication_enabled_for_web` Enable authentication for the web interface via a GitLab account password. Default is true:
```yaml
application_settings:
  type: application-settings
  password_authentication_enabled_for_web: true # or false
```

`performance_bar_allowed_group_path` Path of the group that is allowed to toggle the performance bar:
```yaml
application_settings:
  type: application-settings
  performance_bar_allowed_group_path: My performance bar allowed group path
```

`plantuml_enabled` Enable PlantUML integration:
```yaml
application_settings:
  type: application-settings
  plantuml_enabled: true # or false
```

`plantuml_url` The PlantUML instance URL for integration:
```yaml
application_settings:
  type: application-settings
  plantuml_url: My plantuml url
```

`polling_interval_multiplier` Interval multiplier used by endpoints that perform polling. Set to 0 to disable polling:
```yaml
application_settings:
  type: application-settings
  polling_interval_multiplier: My polling interval multiplier
```

`project_export_enabled` Enable project export:
```yaml
application_settings:
  type: application-settings
  project_export_enabled: true # or false
```

`prometheus_metrics_enabled` Enable prometheus metrics:
```yaml
application_settings:
  type: application-settings
  prometheus_metrics_enabled: true # or false
```

`protected_ci_variables` Environment variables are protected by default:
```yaml
application_settings:
  type: application-settings
  protected_ci_variables: true # or false
```

`pseudonymizer_enabled` When enabled, GitLab will run a background job that will produce pseudonymized CSVs of the GitLab database that will be uploaded to your configured object storage directory:
```yaml
application_settings:
  type: application-settings
  pseudonymizer_enabled: true # or false
```

`recaptcha_enabled` Enable recaptcha:
```yaml
application_settings:
  type: application-settings
  recaptcha_enabled: true # or false
```

`recaptcha_private_key` Private key for recaptcha:
```yaml
application_settings:
  type: application-settings
  recaptcha_private_key: My recaptcha private key
```

`recaptcha_site_key` Site key for recaptcha:
```yaml
application_settings:
  type: application-settings
  recaptcha_site_key: My recaptcha site key
```

`receive_max_input_size` Maximum push size (MB):
```yaml
application_settings:
  type: application-settings
  receive_max_input_size: 42
```

`repository_checks_enabled` GitLab will periodically run git fsck in all project and wiki repositories to look for silent disk corruption issues:
```yaml
application_settings:
  type: application-settings
  repository_checks_enabled: true # or false
```

`repository_size_limit` Size limit per repository (MB):
```yaml
application_settings:
  type: application-settings
  repository_size_limit: 42
```

`repository_storages` A list of names of enabled storage paths, taken from gitlab.yml. New projects will be created in one of these stores, chosen at random:
```yaml
application_settings:
  type: application-settings
  repository_storages: [My repository storages]
```

`require_two_factor_authentication` Require all users to set up Two-factor authentication:
```yaml
application_settings:
  type: application-settings
  require_two_factor_authentication: true # or false
```

`restricted_visibility_levels` Selected levels cannot be used by non-admin users for groups, projects or snippets. Can take private, internal and public as a parameter. Default is null which means there is no restriction:
```yaml
application_settings:
  type: application-settings
  restricted_visibility_levels: [My restricted visibility levels]
```

`rsa_key_restriction` The minimum allowed bit length of an uploaded RSA key. Default is 0 (no restriction). -1 disables RSA keys:
```yaml
application_settings:
  type: application-settings
  rsa_key_restriction: 42
```

`send_user_confirmation_email` Send confirmation email on sign-up:
```yaml
application_settings:
  type: application-settings
  send_user_confirmation_email: true # or false
```

`session_expire_delay` Session duration in minutes. GitLab restart is required to apply changes:
```yaml
application_settings:
  type: application-settings
  session_expire_delay: 42
```

`shared_runners_enabled` Enable shared runners for new projects:
```yaml
application_settings:
  type: application-settings
  shared_runners_enabled: true # or false
```

`shared_runners_minutes` Set the maximum number of pipeline minutes that a group can use on shared Runners per month:
```yaml
application_settings:
  type: application-settings
  shared_runners_minutes: 42
```

`shared_runners_text` Shared runners text:
```yaml
application_settings:
  type: application-settings
  shared_runners_text: My shared runners text
```

`sign_in_text` Text on the login page:
```yaml
application_settings:
  type: application-settings
  sign_in_text: My sign in text
```

`signup_enabled` Enable registration:
```yaml
application_settings:
  type: application-settings
  signup_enabled: true # or false
```

`slack_app_enabled`  Enable Slack app:
```yaml
application_settings:
  type: application-settings
  slack_app_enabled: true # or false
```

`slack_app_id` The app id of the Slack-app:
```yaml
application_settings:
  type: application-settings
  slack_app_id: My slack app id
```

`slack_app_secret` The app secret of the Slack-app:
```yaml
application_settings:
  type: application-settings
  slack_app_secret: My slack app secret
```

`slack_app_verification_token` The verification token of the Slack-app:
```yaml
application_settings:
  type: application-settings
  slack_app_verification_token: My slack app verification token
```

`terminal_max_session_time` Maximum time for web terminal websocket connection (in seconds). Set to 0 for unlimited time:
```yaml
application_settings:
  type: application-settings
  terminal_max_session_time: 42
```

`terms` Markdown content for the ToS:
```yaml
application_settings:
  type: application-settings
  terms: My terms
```

`throttle_authenticated_api_enabled` Enable authenticated API request rate limit. Helps reduce request volume (e.g. from crawlers or abusive bots):
```yaml
application_settings:
  type: application-settings
  throttle_authenticated_api_enabled: true # or false
```

`throttle_authenticated_api_period_in_seconds` Rate limit period in seconds:
```yaml
application_settings:
  type: application-settings
  throttle_authenticated_api_period_in_seconds: 42
```

`throttle_authenticated_api_requests_per_period` Max requests per period per user:
```yaml
application_settings:
  type: application-settings
  throttle_authenticated_api_requests_per_period: 42
```

`throttle_authenticated_web_enabled` Enable authenticated web request rate limit. Helps reduce request volume (e.g. from crawlers or abusive bots):
```yaml
application_settings:
  type: application-settings
  throttle_authenticated_web_enabled: true # or false
```

`throttle_authenticated_web_period_in_seconds` Rate limit period in seconds:
```yaml
application_settings:
  type: application-settings
  throttle_authenticated_web_period_in_seconds: 42
```

`throttle_authenticated_web_requests_per_period` Max requests per period per user:
```yaml
application_settings:
  type: application-settings
  throttle_authenticated_web_requests_per_period: 42
```

`throttle_unauthenticated_enabled` Enable unauthenticated request rate limit. Helps reduce request volume (e.g. from crawlers or abusive bots):
```yaml
application_settings:
  type: application-settings
  throttle_unauthenticated_enabled: true # or false
```

`throttle_unauthenticated_period_in_seconds` Rate limit period in seconds:
```yaml
application_settings:
  type: application-settings
  throttle_unauthenticated_period_in_seconds: 42
```

`throttle_unauthenticated_requests_per_period` Max requests per period per IP:
```yaml
application_settings:
  type: application-settings
  throttle_unauthenticated_requests_per_period: 42
```

`time_tracking_limit_to_hours` Limit display of time tracking units to hours. Default is false:
```yaml
application_settings:
  type: application-settings
  time_tracking_limit_to_hours: true # or false
```

`two_factor_grace_period` Amount of time (in hours) that users are allowed to skip forced configuration of two-factor authentication:
```yaml
application_settings:
  type: application-settings
  two_factor_grace_period: 42
```

`unique_ips_limit_enabled` Limit sign in from multiple ips:
```yaml
application_settings:
  type: application-settings
  unique_ips_limit_enabled: true # or false
```

`unique_ips_limit_per_user` Maximum number of ips per user:
```yaml
application_settings:
  type: application-settings
  unique_ips_limit_per_user: 42
```

`unique_ips_limit_time_window` How many seconds an IP will be counted towards the limit:
```yaml
application_settings:
  type: application-settings
  unique_ips_limit_time_window: 42
```

`usage_ping_enabled` Every week GitLab will report license usage back to GitLab, Inc:
```yaml
application_settings:
  type: application-settings
  usage_ping_enabled: true # or false
```

`user_default_external` Newly registered users will be external by default:
```yaml
application_settings:
  type: application-settings
  user_default_external: true # or false
```

`user_default_internal_regex` Specify an e-mail address regex pattern to identify default internal users:
```yaml
application_settings:
  type: application-settings
  user_default_internal_regex: My user default internal regex
```

`user_oauth_applications` Allow users to register any application to use GitLab as an OAuth provider:
```yaml
application_settings:
  type: application-settings
  user_oauth_applications: true # or false
```

`user_show_add_ssh_key_message` When set to false disable the "You won't be able to pull or push project code via SSH" warning shown to users with no uploaded SSH key:
```yaml
application_settings:
  type: application-settings
  user_show_add_ssh_key_message: true # or false
```

`version_check_enabled` Let GitLab inform you when an update is available:
```yaml
application_settings:
  type: application-settings
  version_check_enabled: true # or false
```

`web_ide_clientside_preview_enabled` Client side evaluation (Allow live previews of JavaScript projects in the Web IDE using CodeSandbox client side evaluation):
```yaml
application_settings:
  type: application-settings
  web_ide_clientside_preview_enabled: true # or false
```


