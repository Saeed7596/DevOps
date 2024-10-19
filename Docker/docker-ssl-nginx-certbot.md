> set ssl with docker

all step should be happened with the user that create the app for example `gitlab_ssh` user

> first step => **nano `docker-nginx.compose`**
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
    restart: unless-stopped
    networks:
      - app-network-name
  certbot:
    image: certbot:v2.6.0
    command: 'certonly --reinstall --webroot --webroot-path=/var/www/certbot --email < youremail@gmail.com > --agree-tos --no-eff-email -d example.com'
    # --force-renewal " can use this at the end of command line to renewal a new ssl key without check the expire time"
    depends_on:
      - nginx
    volumes:
      - ./certbot/conf:/etc/letsencrypt
      - ./certbot/www:/var/www/certbot
networks:
  app-network-name:
    external:
      name: app-network-name
```

> second step **mkdir `nginx`** directory and **nano `default.conf`** file
```
server {
    listen 80;
    server_name example.com www.example.com;
    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }
    location / {
        return 301 https://$host$request_uri;
    }
}
server {
    #listen 443 ssl;
    server_name example.com www.example.com;
    client_max_body_size 32M;

    location / {
        proxy_read_timeout      300;
        proxy_connect_timeout   300;
        proxy_redirect          off;

        proxy_set_header        Host                $http_host;
        proxy_set_header        X-Real-IP           $remote_addr;
        proxy_set_header        X-Forwarded-For     $proxy_add_x_forwarded_for;
        proxy_set_header        X-Forwarded-Proto   https;
        proxy_set_header        X-Frame-Options     SAMEORIGIN;
        proxy_pass http://172.17.0.1:app port;
    }
    #ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem;
    #ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;
    #include /etc/letsencrypt/options-ssl-nginx.conf;
    #ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;
}

```
----------------------------------------------------
```
# Redirect from www.example.com to example.com
server {
    listen 80;
    server_name www.example.com;
    
    return 301 http://example.com$request_uri;
}

server {
    listen 443 ssl;
    server_name www.example.com;
    
    #ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem;
    #ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;
    #include /etc/letsencrypt/options-ssl-nginx.conf;
    #ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

    return 301 https://example.com$request_uri;
}

# Main server block
server {
    listen 80;
    server_name example.com;
    
    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }
    location / {
        return 301 https://$host$request_uri;
    }
}

server {
    #listen 443 ssl;
    server_name example.com;
    client_max_body_size 32M;

    location / {
        proxy_read_timeout      300;
        proxy_connect_timeout   300;
        proxy_redirect          off;

        proxy_set_header        Host                $http_host;
        proxy_set_header        X-Real-IP           $remote_addr;
        proxy_set_header        X-Forwarded-For     $proxy_add_x_forwarded_for;
        proxy_set_header        X-Forwarded-Proto   https;
        proxy_set_header        X-Frame-Options     SAMEORIGIN;
        proxy_pass http://172.17.0.1:3030;
    }
    
    #ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem;
    #ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;
    #include /etc/letsencrypt/options-ssl-nginx.conf;
    #ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;
}

```
### pay attention to the comment line

> first time run the docker compose with this command line

**` docker compose -f docker-nginx.compose up -d `**

after that check the logs of certbot container and certbot directory to see the files, and the must have the permission of the user of app "`gitlab_ssh`"
for check use "`ls -l`" and if the files have anthoer user permission use "`chown -R gitlab_ssh:gitlab_ssh certbot`" to change the permission.

> Now run this commands:

**` docker compose -f docker-nginx.compose down `**

maybe the *"/certbot/conf"* don't have the **` ssl-dhparams.pem ` & ` options-ssl-nginx.conf `**.
So with **nano `ssl-dhparams.pem` & nano `options-ssl-nginx.conf`**

create this file **(with vauleable content!)**

then nano `./nginx/default.conf` and **uncomment the comment line**

now run the **`docker-nginx.compose`** again

**` docker compose -f docker-nginx.compose up -d `**

# Use cloudfare zero trust for ssl
* in tunnel use http and point ip to port 80 *
Change nginx `default.conf`
```conf
server {
    listen 80;
    server_name example.ir;

    location / {
        proxy_pass http://172.17.0.1:app port;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```
```bash
docker compose - f docker-nginx.compose restart nginx
```

# Count header with nginx
* First line of `default.conf`
```conf 
log_format custom '$remote_addr - $remote_user [$time_local] "$request" '
                '$status $body_bytes_sent "$http_referer" '
                '"$http_user_agent" "$http_my_header"';

# or save just this headers
log_format custom '$http_host';
```
```conf
# add this if in location / part
        if ($http_referer = "https://example.ir/") {
            access_log /var/log/nginx/danesh-access.log custom;
        }
```
# Add volume in `docker-compose.yml`
```yml
volumes:
  - ./nginx_logs:/var/log/nginx
```
```bash
#for frirst time because can't create nginx_logs directory
docker compose - f docker-nginx.compose down
docker compose - f docker-nginx.compose up -d
#after any change in default.conf
docker compose - f docker-nginx.compose restart nginx
```
# To send this logs to zabbix
```bash
apt install zabbix-sender
apt-get install jq
```
```bash
nano count_requests.sh
```
```sh
#!/bin/bash
LOG_FILE="/your-path/nginx_logs/access.log"

declare -A count

while IFS= read -r line; do
  ((count["$line"]++))
done < "$LOG_FILE"

json_output="{"
for line in "${!count[@]}"; do
  json_output+="$(echo $line | jq -R .): ${count[$line]},"
done
json_output="${json_output%,}}"

#echo "$json_output"

zabbix_sender -z ip-zabbix-server -s "hostname-zabbix" -k "http.requests.count" -o "$json_output"

> "$LOG_FILE"
```
> in zabbix dashbord > select host > create item > type item:Zabbix trapper > key=http.requests.count
```bash
crontab -e
```
```bash
* * * * * /path/to/your/script/count_requests.sh
```
