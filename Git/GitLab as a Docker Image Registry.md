# Using GitLab as a Docker Image Registry

## 1. Enable GitLab Container Registry

* Ensure the GitLab Container Registry feature is enabled.
* If you manage your own GitLab instance, edit `/etc/gitlab/gitlab.rb`:

```bash
registry_external_url 'https://your-gitlab-domain:5050'
```

* Then reconfigure GitLab:

```bash
sudo gitlab-ctl reconfigure
```

> If you are using gitlab.com, the Container Registry is already enabled.

## 2. Find the Registry URL

Each GitLab project has a registry address, usually like this:

```
registry.gitlab.com/<namespace>/<project>
```

Example:

```
registry.gitlab.com/your-username/your-project
```

## 3. Log in to the GitLab Registry

Use `docker login` to authenticate:

```bash
docker login registry.gitlab.com
```

Credentials:

* **Username**: Your GitLab username or Personal Access Token
* **Password**: Your GitLab password or Access Token

## 4. Push a Docker Image to GitLab Registry

**Build the Docker image:**

```bash
docker build -t registry.gitlab.com/your-username/your-project/your-image:tag .
```

**Push the image:**

```bash
docker push registry.gitlab.com/your-username/your-project/your-image:tag
```

## 5. Use the Image in GitLab CI/CD

In your `.gitlab-ci.yml` file, you can directly use the image:

```yaml
image: registry.gitlab.com/your-username/your-project/your-image:tag

stages:
  - deploy

deploy-job:
  stage: deploy
  script:
    - echo "Deploying..."
```

## Important Notes

* Access to the Registry depends on your project's **Visibility** settings (Private or Public).
* For Private projects, authentication is required via `docker login`.
* Images stored in GitLab Registry count against your project storage quota.

---

**Ready to use GitLab as your private, secure Docker image repository!**
