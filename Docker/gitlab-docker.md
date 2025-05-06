> first step should be create a new variable:

**nano `~/.bashrc`**

add this line: 
```bash
export GITLAB_HOME=/srv/gitlab
```
save the file and run:
*`source ~/.bashrc`*

> second step in /srv directory

**nano `docker-compose.yml`**
```yml
version: "3.3"
services:
  nginx:
    container_name: nginx
    image: nginx:1.24.0
    ports:
      - 80:80
      - 443:443
    environment:
      - TZ=Asia/Tehran
    volumes:
      - ./nginx/:/etc/nginx/conf.d/
      - ./certbot/conf:/etc/letsencrypt
      - ./certbot/www:/var/www/certbot
    #deploy:
    #  restart_policy:
    #    condition: on-failure
    #    delay: 10s
    #    max_attempts: 5
    #    window: 120s
    restart: unless-stopped
  certbot:
    image: certbot:v2.6.0
    command: 'certonly --reinstall --webroot --webroot-path=/var/www/certbot --email email@gmail.com --agree-tos --no-eff-email -d git.example.ir'
    volumes:
      - ./certbot/conf:/etc/letsencrypt
      - ./certbot/www:/var/www/certbot
```

**nano `/gitlab/docker-compose.yml`**
```yml
version: '3.6'
services:
  web:
    image: 'gitlab-ce:version'
    restart: always
    hostname: 'git.example.ir'
    environment:
      GITLAB_OMNIBUS_CONFIG: |
        external_url 'https://git.example.ir'
        # Add any other gitlab.rb configuration here, each on its own line
    ports:
      - '8580:80'
      - '8543:443'
      - '8622:22'
    volumes:
      - '$GITLAB_HOME/config:/etc/gitlab'
      - '$GITLAB_HOME/logs:/var/log/gitlab'
      - '$GITLAB_HOME/data:/var/opt/gitlab'
    shm_size: '512m'
```
**nano `/nginx/default.conf`**
```
server {
    listen 80;
    server_name git.example.ir;
    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }
    location / {
        return 301 https://$host$request_uri;
    }
}
server {
    #listen 443 ssl;
    server_name git.example.ir;
    client_max_body_size 512M;

    location / {
        proxy_read_timeout      300;
        proxy_connect_timeout   300;
        proxy_redirect          off;

        proxy_set_header        Host                $http_host;
        proxy_set_header        X-Real-IP           $remote_addr;
        proxy_set_header        X-Forwarded-For     $proxy_add_x_forwarded_for;
        proxy_set_header        X-Forwarded-Proto   https;
        proxy_set_header        X-Frame-Options     SAMEORIGIN;
        proxy_pass https://172.17.0.1:8543;
    }
    #ssl on;
    #ssl_certificate /etc/letsencrypt/live/git.example.ir/fullchain.pem;
    #ssl_certificate_key /etc/letsencrypt/live/git.example.ir/privkey.pem;
    #include /etc/letsencrypt/options-ssl-nginx.conf;
    #ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;
}

```
```bash
cd /srv/gitlab
docker compose -f docker-compose.yml up -d
cd /srv
docker compose -f docker-compose.yml up -d
docker compose -f docker-compose.yml down
nano /nginx/default.conf
#uncomment the ssl comment line
docker compose -f docker-compose.yml up -d
```
-------------------------------------------
# Move gitlab
```bash
docker exec -it <gitlab container_id> /bin/bash
gitlab-backup create #this commmand create a backup in /var/opt/gitlab/backups path
exit #exit the gitlab container
docker cp <gitlab container_id>:/var/opt/gitlab/backups /path/to/local/backup
#with scp can move this backup to new server
#in new server run the docker compose of gitlab
docker cp /path/to/local/backup <gitlab container_id>:/var/opt/gitlab/backups
docker exec -it <gitlab container_id> /bin/bash
chown git:git /var/opt/gitlab/backups/<backup_file>
chmod 600 /var/opt/gitlab/backups/<backup_file>
gitlab-backup restore BACKUP=<backup_file_timestamp> #just the timestamp
#like this "gitlab-backup restore BACKUP=1727362106_2024_09_26_16.1.2"
gitlab-ctl reconfigure
gitlab-ctl restart
#if you have error 500 in CI/CD copy the gitlab-secrets.json from old server to new server
#in new server remove gitlab-secrets.json
docker compose -f docker-compose.yml down
rm gitlab-secrets.json
#in old server
scp /srv/gitlab/config/gitlab-secrets.json username@remote_host:/srv/gitlab/config/
```
-------------------------------------------
# gitlab-runner 
# GitLab Runner Installation with Docker
## Steps
### 1. Pull the GitLab Runner image
```bash
docker pull gitlab/gitlab-runner:latest
```

### 2. Run the GitLab Runner container
```bash
docker run -d --name gitlab-runner --restart always \
  -v /srv/gitlab-runner/config:/etc/gitlab-runner \
  -v /var/run/docker.sock:/var/run/docker.sock \
  gitlab/gitlab-runner:latest
```

* `/srv/gitlab-runner/config:/etc/gitlab-runner` : Mounts a volume for Runner configuration.
* `/var/run/docker.sock:/var/run/docker.sock` : Allows Docker to be controlled inside jobs.

### 3. Register the GitLab Runner

```bash
docker exec -it gitlab-runner gitlab-runner register
```

You will be prompted to provide:
* **GitLab URL** (e.g., `https://git.example.ir`)
* **Registration Token** (get this from your GitLab project's CI/CD settings)
* **Description** (name your runner)
* **Tags** (optional labels for this runner)
* **Executor** (`docker`, `shell`, etc.)
* **Default Docker image** (e.g., `docker:latest`)

---

# Understanding `/etc/gitlab-runner/config.toml`
The `config.toml` file is the main configuration file for GitLab Runner.

Example structure:
```toml
concurrent = 4
check_interval = 0

[session_server]
  session_timeout = 1800

[[runners]]
  name = "my-runner"
  url = "https://gitlab.com/"
  token = "xxxxxxxxxxxxxxxxxxxx"
  executor = "docker"

  [runners.custom_build_dir]
  [runners.docker]
    tls_verify = false
    pull_policy = ["if-not-present"]
    image = "docker:latest"
    privileged = true
    disable_entrypoint_overwrite = false
    oom_kill_disable = false
    disable_cache = false
    volumes = ["/cache"]
    shm_size = 0
```

## Important Sections:

* **concurrent**: Max number of jobs that can run simultaneously.
* **session\_server**: Configuration for WebSocket session for the job trace.
* **runners**: List of runners registered.

  * **name**: Friendly name for the runner.
  * **url**: GitLab instance URL.
  * **token**: Authentication token for the runner.
  * **executor**: How jobs are run (e.g., `docker`, `shell`, `virtualbox`).

### Inside `[runners.docker]`

* **image**: Default Docker image used.
* **privileged**: Whether to enable Docker-in-Docker.
* **volumes**: Volumes mounted into the containers.
* **shm\_size**: Shared memory size for containers.
* **pull_policy**: Defines when Docker should pull images. Example: `["if-not-present"]`

---

# Quick Commands

| Action                   | Command                                                                                                               |
| ------------------------ | --------------------------------------------------------------------------------------------------------------------- |
| View Runner logs         | `docker logs gitlab-runner`                                                                                           |
| Restart Runner container | `docker restart gitlab-runner`                                                                                        |
| Update Runner image      | `docker pull gitlab/gitlab-runner:latest && docker stop gitlab-runner && docker rm gitlab-runner && re-run container` |

---

# Tips

* Always backup `config.toml` before updating or modifying it.
* Use `tags` smartly to assign jobs to appropriate runners.
* Prefer "privileged" mode if you need to run Docker inside jobs.

---

**My `/etc/gitlab-runner/config.toml`**
```vim
concurrent = 1
check_interval = 0
shutdown_timeout = 0

[session_server]
  session_timeout = 1800

[[runners]]
  name = "My Runner"
  url = "https://git.example.ir"
  id = 2
  token = "Your Token" #when create the runner
  token_obtained_at = 2023-07-20T19:31:18Z
  token_expires_at = 0001-01-01T00:00:00Z
  executor = "docker"
  cache_dir = "/cache"
  [runners.cache]
    MaxUploadedArchiveSize = 0
  [runners.docker]
    tls_verify = false
    pull_policy = ["if-not-present"]
    image = "docker:24.0.2"
    privileged = false
    disable_entrypoint_overwrite = false
    oom_kill_disable = false
    disable_cache = false
    volumes = ["/cache:/cache", "/var/run/docker.sock:/var/run/docker.sock"]
    shm_size = 0
```

---

# Upgrade
## Change the image of docker-compose.yml file, but you should pay attention the [upgrade-path](https://gitlab-com.gitlab.io/support/toolbox/upgrade-path/), change image step by step.
* For example upgrade 16.1.2 to 17.3.4:
`16.3.9 > 16.7.10 > 16.11.10 > 17.3.4`
First pull the image, then change the *docker-compose.yml* image and:
```bash
docker pull gitlab-ce:version
docker compose -f docker-compose.yml down
docker compose -f docker-compose.yml up -d
```
**Note:** I didn't need these commands, but you might.
### Running the Database Migration
After the update, it's necessary to migrate the GitLab database to the new version. This step is crucial, and if not performed, you may encounter data inconsistency errors.

To run the database migration, use the following command:

```bash
docker exec -it <gitlab-container-name> gitlab-rake db:migrate
```
This command prepares the database for use with the new version.

### Reconfiguring GitLab
After migrating the database, you need to reconfigure GitLab to align the new settings with the updated version.

```bash
docker exec -it <gitlab-container-name> gitlab-ctl reconfigure
```
This command updates the internal GitLab settings.

### Restarting the GitLab Service
To ensure GitLab is running properly, restart the GitLab service:

```bash
docker exec -it <gitlab-container-name> gitlab-ctl restart
```

### Checking Logs and GitLab Status
To make sure everything is functioning correctly, check GitLab's logs:

```bash
docker logs <gitlab-container-name>
```
You can also check the GitLab status with this command:

```bash
docker exec -it <gitlab-container-name> gitlab-rake gitlab:check SANITIZE=true
```

### Recovering Sensitive Files in Case of Errors (e.g., `gitlab-secrets.json`)
If you encounter a 500 error after the update, you may need to restore sensitive files like `gitlab-secrets.json` from a backup. This file contains sensitive keys that might need to be restored for the new version.

