# Table of Contents <!-- omit in toc -->

- [User lifecycle](#user-lifecycle)
- [Edit](#edit)
  - [Account](#account)
  - [Password](#password)
  - [Access](#access)
  - [Limits](#limits)
  - [Profile](#profile)

# User lifecycle

`gitlab_id` GitLab id:
```yaml
mmyuser:
  type: user
  gitlab_id: gitlab
```

More information can be found [here](action_file.md#gitlab_id)

`create_object` Create object if it does not exists:
```yaml
mmyuser:
  type: user
  create_object: true # or false
```

`delete_object` Delete object if it exists:
```yaml
mmyuser:
  type: user
  delete_object: true # or false
```

# Edit

## Account

`name` Name:
```yaml
mmyuser:
  type: user
  name: My name
```

`email` Email:
```yaml
mmyuser:
  type: user
  email: My email
```

`skip_confirmation` Skip confirmation and assume e-mail is verified:
```yaml
mmyuser:
  type: user
  skip_confirmation: true # or false
```

`skip_reconfirmation` Skip reconfirmation:
```yaml
mmyuser:
  type: user
  skip_reconfirmation: true # or false
```

`public_email` The public email of the user:
```yaml
mmyuser:
  type: user
  public_email: My public email
```

`state` User state:
```yaml
mmyuser:
  type: user
  state: active # one of active, banned, blocked, blocked_pending_approval, deactivated, ldap_blocked
```

## Password

`password` Password:
```yaml
mmyuser:
  type: user
  password: My password
```

`reset_password` Send user password reset link:
```yaml
mmyuser:
  type: user
  reset_password: true # or false
```

`force_random_password` Set user password to a random value :
```yaml
mmyuser:
  type: user
  force_random_password: true # or false
```

## Access

`projects_limit` Number of projects user can create:
```yaml
mmyuser:
  type: user
  projects_limit: 42
```

`can_create_group` User can create groups:
```yaml
mmyuser:
  type: user
  can_create_group: true # or false
```

`admin` User is admin:
```yaml
mmyuser:
  type: user
  admin: true # or false
```

`external` Flags the user as external:
```yaml
mmyuser:
  type: user
  external: true # or false
```

`provider` External provider name:
```yaml
mmyuser:
  type: user
  provider: My provider
```

`extern_uid` External UID:
```yaml
mmyuser:
  type: user
  extern_uid: My extern uid
```

## Limits

`shared_runners_minutes_limit` Pipeline minutes quota for this user:
```yaml
mmyuser:
  type: user
  shared_runners_minutes_limit: 42
```

`extra_shared_runners_minutes_limit` Extra pipeline minutes quota for this user:
```yaml
mmyuser:
  type: user
  extra_shared_runners_minutes_limit: 42
```

## Profile

`avatar` Image file for user's avatar:
```yaml
mmyuser:
  type: user
  avatar: My avatar
```

`skype` Skype ID:
```yaml
mmyuser:
  type: user
  skype: My skype
```

`linkedin` LinkedIn:
```yaml
mmyuser:
  type: user
  linkedin: My linkedin
```

`twitter` Twitter account:
```yaml
mmyuser:
  type: user
  twitter: My twitter
```

`website_url` Website URL:
```yaml
mmyuser:
  type: user
  website_url: My website url
```

`location` User's location:
```yaml
mmyuser:
  type: user
  location: My location
```

`organization` Organization name:
```yaml
mmyuser:
  type: user
  organization: My organization
```

`bio` User's biography:
```yaml
mmyuser:
  type: user
  bio: My bio
```

`private_profile` User's profile is private:
```yaml
mmyuser:
  type: user
  private_profile: true # or false
```

`note` Admin note:
```yaml
mmyuser:
  type: user
  note: My note
```


