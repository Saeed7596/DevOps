> set ssl with docker

all step should be happened with the user that create the app for example `user_ssh` user

> first step => **nano `docker-nginx.yml`**
```yml
#version: "3.3"
services:
  nginx:
    image: nginx:1.24.0
    container_name: nginx
    logging:
      driver: "json-file"
      options:
        max-file: 5
        max-size: 10m
    ports:
      - 80:80
      - 443:443
    environment:
      - TZ=Asia/Tehran
    volumes:
      - ./nginx/:/etc/nginx/conf.d/
      - ./nginx_logs:/var/log/nginx
      - ./nginx_conf/nginx.conf:/etc/nginx/nginx.conf  # Volume for nginx.conf
      - ./certbot/conf:/etc/letsencrypt
      - ./certbot/www:/var/www/certbot
    restart: unless-stopped
    #restart: always
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
    external: true
      #name: app-network-name
```

## ** second step **mkdir `nginx`** directory and **nano `default.conf`** file **
```
server {
    listen 80 default_server;
    #listen 443 ssl default_server;
    server_name _;

    location / {
        #return 444;  # Drops the connection
        deny all;
    }
}
```
```conf
server {
    listen 80 default_server;
    listen [::]:80 default_server;
    server_name "_";
    return 444; # Connection closed without response
}

server {
    listen 443 default_server;
    listen [::]:443 default_server;
    server_name "_";
    ssl_reject_handshake on; # Reject SSL connection
}
```
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
    
    return 301 https://example.com$request_uri;
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

**` docker compose -f docker-nginx.yml up -d `**

after that check the logs of certbot container and certbot directory to see the files, and the must have the permission of the user of app "`user_ssh`"
for check use "`ls -l`" and if the files have anthoer user permission use "`chown -R user_ssh:user_ssh certbot`" to change the permission.

> Now run this commands:

**` docker compose -f docker-nginx.yml down `**

maybe the *"/certbot/conf"* don't have the **` ssl-dhparams.pem ` & ` options-ssl-nginx.conf `**.
So with **nano `ssl-dhparams.pem` & nano `options-ssl-nginx.conf`**

create this file **(with vauleable content!)**

then nano `./nginx/default.conf` and **uncomment the comment line**

now run the **`docker-nginx.yml`** again

**` docker compose -f docker-nginx.yml up -d `**

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
docker compose -f docker-nginx.yml restart nginx
# or
docker exec nginx nginx -t
docker exec nginx nginx -s reload
```
## Set new ssl without stop `nginx`
```bash
nano nginx/default.conf
# add new server block
nano docker-nginx.yml
# change domain name
docker exec nginx nginx -t
docker exec nginx nginx -s reload
docker compose -f docker-nginx.yml down certbot
docker compose -f docker-nginx.yml up -d certbot
nano nginx/default.conf
# uncomment the ssl line 0f new server block
docker exec nginx nginx -s reload
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
            access_log /var/log/nginx/website-access.log custom;
        }
```
# Add volume in `docker-compose.yml`
```yml
volumes:
  - ./nginx_logs:/var/log/nginx
```
```bash
#for frirst time because can't create nginx_logs directory
docker compose -f docker-nginx.yml down
docker compose -f docker-nginx.yml up -d
#after any change in default.conf
docker compose -f docker-nginx.yml restart nginx
# or
docker exec nginx nginx -t
docker exec nginx nginx -s reload
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
LOG_FILE="/your-path/nginx_logs/website-access.log"

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

zabbix_sender -z ip-zabbix-server-or-proxy -s "hostname-zabbix" -k "http.requests.count" -o "$json_output"

> "$LOG_FILE"
```
*in zabbix dashbord > select host > create item > type item:Zabbix trapper > key=http.requests.count*
*select item > Create dependet item > add Preprocessing > JSONPath = $.['example.ir']*
```bash
chmod +x count_requests.sh
./count_requests.sh
crontab -e
```
```bash
* * * * * /path/to/your/script/count_requests.sh
```
# Change some config in nginx.conf
```bash
docker cp nginx:/etc/nginx/nginx.conf /home/path/nginx.conf
# edit file and save
docker cp /home/path/nginx.conf nginx:/etc/nginx/nginx.conf
```
*nginx.conf*
```conf
user  nginx;
worker_processes  auto;

error_log  /var/log/nginx/error.log notice;
pid        /var/run/nginx.pid;


# Enables the use of JIT for regular expressions to speed-up their processing.
pcre_jit on;

events {
    worker_connections  4096;
}


http {
    #include       mime.types;
    #include       /etc/nginx/mime.types;
    include /usr/local/openresty/nginx/conf/mime.types;
    default_type  application/octet-stream;

    client_header_buffer_size 1024;
    server_tokens off; # disable signature
    large_client_header_buffers 4 8192;

    proxy_buffer_size 128k;
    proxy_buffers 4 256k;
    proxy_busy_buffers_size 256k;
    client_max_body_size 10m;

    log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for"';

    access_log  /var/log/nginx/access.log  main;

    sendfile        on;
    #tcp_nopush     on;

    keepalive_timeout  65;

    #gzip  on;
    gzip on;
    gzip_types text/plain text/css application/javascript application/json image/svg+xml;
    gzip_vary on;
    gzip_min_length 10240;
    gzip_comp_level 5;
    gzip_proxied any;

    # Enable Brotli compression
    brotli on;
    brotli_comp_level 4;
    brotli_types text/plain text/css application/json application/javascript application/x-javascript text/xml application/xml application/xml+rss text/javascript;

    #more_clear_headers      server;
    #more_set_headers        "server: hidden";
    #proxy_pass_header       server;

    include /etc/nginx/conf.d/*.conf;
}
```
*default.conf*
```vim
location ~* \.(webp|jpg|jpeg|png|gif|ico)$ {
    expires 30d;
    add_header Cache-Control "public, no-transform";
    try_files $uri $uri/ =404;
}
```
```bash
docker exec -it nginx /bin/bash # nginx is container name
nginx -t # check new config
exit # from container
docker compose -f docker-nginx.yml restart nginx # nginx is service name in docker-nginx.yml file
# or
docker exec nginx nginx -t
docker exec nginx nginx -s reload
```
# If you want use brotli use image openresty
### `mkdri nginx_conf` and `nano *nginx.conf*`
```yml
services:
  nginx:
    container_name: nginx
    image: openresty/openresty:1.21.4.1-0-jammy
    ports:
      - 80:80
      - 443:443
    environment:
      - TZ=Asia/Tehran
    volumes:
      - ./nginx/:/etc/nginx/conf.d/
      - ./nginx_logs:/var/log/nginx
      #- ./nginx_conf/nginx.conf:/usr/local/openresty/nginx/conf/nginx.conf:ro # Volume for nginx.conf for image openresty (not work)
      - ./nginx_conf/nginx.conf:/etc/nginx/nginx.conf  # Volume for nginx.conf for image nginx and openresty
      - ./certbot/conf:/etc/letsencrypt
      - ./certbot/www:/var/www/certbot
    restart: unless-stopped
    networks:
      - net-name
  certbot:
    container_name: certbot
    image: certbot/certbot:v2.11.0
    command: 'certonly --reinstall --webroot --webroot-path=/var/www/certbot --email youremail@gmail.com --agree-tos --no-eff-email -d example.com'
    depends_on:
      - nginx
    volumes:
      - ./certbot/conf:/etc/letsencrypt
      - ./certbot/www:/var/www/certbot
networks:
  net-name:
    external: true
```
default `nginx.conf` image openresty in path `*/usr/local/openresty/nginx/conf/*`
```conf
# nginx.conf  --  docker-openresty
#
# This file is installed to:
#   `/usr/local/openresty/nginx/conf/nginx.conf`
# and is the file loaded by nginx at startup,
# unless the user specifies otherwise.
#
# It tracks the upstream OpenResty's `nginx.conf`, but removes the `server`
# section and adds this directive:
#     `include /etc/nginx/conf.d/*.conf;`
#
# The `docker-openresty` file `nginx.vh.default.conf` is copied to
# `/etc/nginx/conf.d/default.conf`.  It contains the `server section
# of the upstream `nginx.conf`.
#
# See https://github.com/openresty/docker-openresty/blob/master/README.md#nginx-config-files
#

#user  nobody;
#worker_processes 1;

# Enables the use of JIT for regular expressions to speed-up their processing.
pcre_jit on;



#error_log  logs/error.log;
#error_log  logs/error.log  notice;
#error_log  logs/error.log  info;

#pid        logs/nginx.pid;


events {
    worker_connections  1024;
}


http {
    include       mime.types;
    default_type  application/octet-stream;

    # Enables or disables the use of underscores in client request header fields.
    # When the use of underscores is disabled, request header fields whose names contain underscores are marked as invalid and become subject to the ignore_invalid_headers directive.
    # underscores_in_headers off;

    #log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
    #                  '$status $body_bytes_sent "$http_referer" '
    #                  '"$http_user_agent" "$http_x_forwarded_for"';

    #access_log  logs/access.log  main;

        # Log in JSON Format
        # log_format nginxlog_json escape=json '{ "timestamp": "$time_iso8601", '
        # '"remote_addr": "$remote_addr", '
        #  '"body_bytes_sent": $body_bytes_sent, '
        #  '"request_time": $request_time, '
        #  '"response_status": $status, '
        #  '"request": "$request", '
        #  '"request_method": "$request_method", '
        #  '"host": "$host",'
        #  '"upstream_addr": "$upstream_addr",'
        #  '"http_x_forwarded_for": "$http_x_forwarded_for",'
        #  '"http_referrer": "$http_referer", '
        #  '"http_user_agent": "$http_user_agent", '
        #  '"http_version": "$server_protocol", '
        #  '"nginx_access": true }';
        # access_log /dev/stdout nginxlog_json;

    # See Move default writable paths to a dedicated directory (#119)
    # https://github.com/openresty/docker-openresty/issues/119
    client_body_temp_path /var/run/openresty/nginx-client-body;
    proxy_temp_path       /var/run/openresty/nginx-proxy;
    fastcgi_temp_path     /var/run/openresty/nginx-fastcgi;
    uwsgi_temp_path       /var/run/openresty/nginx-uwsgi;
    scgi_temp_path        /var/run/openresty/nginx-scgi;

    sendfile        on;
    #tcp_nopush     on;

    #keepalive_timeout  0;
    keepalive_timeout  65;

    #gzip  on;

    include /etc/nginx/conf.d/*.conf;

    # Don't reveal OpenResty version to clients.
    # server_tokens off;
}
```
Another `nginx.conf` file for high traffic.
```conf
user  nginx;
worker_processes  auto;

error_log  /var/log/nginx/error.log notice;
pid        /var/run/nginx.pid;

pcre_jit on;

events {
    worker_connections  8192;
}

http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;

    client_header_buffer_size 1024;
    server_tokens off;
    large_client_header_buffers 4 8192;

    # Buffering and file size settings
    client_body_buffer_size 128k;
    client_max_body_size 20m;
    proxy_buffer_size 512k;
    proxy_buffers 8 512k;
    proxy_busy_buffers_size 512k;
    #proxy_temp_file_write_size 512k;

    # Log format
    log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for"';
    access_log  /var/log/nginx/access.log  main;

    # Connection optimization
    sendfile        on;
    tcp_nopush      on;
    tcp_nodelay     on;
    keepalive_timeout  65;

    # Compression settings
    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml+rss text/javascript;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_proxied any;
    gzip_comp_level 6;

    include /etc/nginx/conf.d/*.conf;
}
```
