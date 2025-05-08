# GitLab CI/CD Variables

## Overview

GitLab CI/CD variables are key-value pairs used to customize the behavior of CI/CD pipelines. They allow you to store information such as secrets, tokens, configuration settings, and other parameters that your jobs and scripts can use.

Variables can be defined at multiple levels:

* **Instance-level**: Available across all projects (admin access required)
* **Group-level**: Available for all projects within a group
* **Project-level**: Available within a single project
* **Pipeline/job-level**: Defined within `.gitlab-ci.yml` directly

## Types of Variables

* **Environment Variables**: Automatically created by GitLab (e.g., `CI_COMMIT_SHA`, `CI_JOB_ID`)
* **Custom Variables**: Created by users at different levels
* **Protected Variables**: Only exposed to pipelines running on protected branches or tags
* **Masked Variables**: Hidden in job logs for security purposes

## How to Define Variables

### 1. In GitLab UI

Go to:

* Project -> Settings -> CI/CD -> Variables -> Add Variable

Options:

* Key (name of variable)
* Value (secret or value)
* Protect/Mask/Environment Scope options

### 2. In `.gitlab-ci.yml`

```yaml
variables:
  VAR_NAME: "value"

stages:
  - build

build_job:
  stage: build
  script:
    - echo "$VAR_NAME"
```

### 3. As Job-level Variables

```yaml
job_name:
  stage: test
  variables:
    TEST_ENV: "testing"
  script:
    - echo "$TEST_ENV"
```

## Using Variables

Simply reference them in your scripts using `$VARIABLE_NAME`.
Example:

```yaml
script:
  - echo "Deploying to $ENVIRONMENT"
```

## Best Practices

* **Protect sensitive variables** by enabling "Protected" and "Masked" options.
* **Use environment scopes** for stage-specific or environment-specific values.
* **Use job-level variables** when specific jobs require different settings.
* **Avoid hardcoding secrets** inside `.gitlab-ci.yml`.

## Example Use Case

Setting a Kubernetes config from a variable:

```yaml
before_script:
  - mkdir -p ~/.kube
  - echo "$KUBE_CONFIG" > ~/.kube/config # $KUBE_CONFIG is defined earlier in CI/CD settings
```

---

GitLab Variables help make your pipelines dynamic, secure, and environment-specific.
