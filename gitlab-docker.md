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
    deploy:
      restart_policy:
        condition: any
        delay: 10s
        max_attempts: 5
        window: 120s
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
