# Default `nginx.conf`
```nginx
user  nginx;
worker_processes  auto;

error_log  /var/log/nginx/error.log notice;
pid        /var/run/nginx.pid;


events {
    worker_connections  1024;
}


http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;

    log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for"';

    access_log  /var/log/nginx/access.log  main;

    sendfile        on;
    #tcp_nopush     on;

    keepalive_timeout  65;

    #gzip  on;

    include /etc/nginx/conf.d/*.conf;
}
```
# High Performance `nginx.conf`
```nginx
user  nginx;
worker_processes  auto;

# Error log and PID settings
error_log  /var/log/nginx/error.log notice;
pid        /var/run/nginx.pid;

# Enables the use of JIT for regular expressions to speed up their processing
pcre_jit on;

events {
    worker_connections  8192;
    multi_accept on;
    use epoll;
}

http {
    # Include MIME types
    #include /usr/local/openresty/nginx/conf/mime.types;
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;

    # SSL settings
    ssl_protocols       TLSv1.2 TLSv1.3;
    ssl_ciphers         HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    # Security headers for all servers
    server_tokens off; # Disables displaying the Nginx version in HTTP headers to prevent attackers from exploiting known vulnerabilities.
    add_header X-Content-Type-Options nosniff; # Prevents browsers from interpreting files as a different MIME type, enhancing security against MIME sniffing attacks.
    add_header X-XSS-Protection "1; mode=block"; # Enables browser's built-in XSS protection and blocks the page if an attack is detected.
    # add_header X-Robots-Tag none; # SEO Problem: search engines can't index the page
    add_header X-Robots-Tag "index, follow"; # Allows search engines to index the page and follow its links for better SEO.
    add_header X-Download-Options noopen; # Prevents files downloaded from being automatically executed in some browsers (e.g., Internet Explorer).
    add_header X-Permitted-Cross-Domain-Policies none; # Blocks access to Adobe cross-domain policy files, restricting resource sharing from unauthorized domains.
    # add_header Referrer-Policy no-referrer; # Google analytics not work!
    add_header Referrer-Policy "strict-origin-when-cross-origin"; # Controls how much referrer information is sent with requests to enhance privacy while maintaining analytics.

    # Client header and body settings
    client_max_body_size 32M;
    client_body_buffer_size 128k;
    client_header_buffer_size 1024;
    large_client_header_buffers 4 8192;

    # Proxy buffer settings
    proxy_buffer_size 512k;
    proxy_buffers 8 512k;
    proxy_busy_buffers_size 512k;

    # Logging configuration
    log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for"';
    access_log  /var/log/nginx/access.log  main;

    # Connection settings
    sendfile        on;
    tcp_nopush      on;
    tcp_nodelay     on;
    keepalive_timeout  65;

    # Gzip compression settings
    gzip on;
    gzip_types text/plain text/css application/javascript application/json image/svg+xml;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_comp_level 6;
    gzip_proxied any;

    # Optional Brotli compression settings (commented out)
    #brotli on;
    #brotli_comp_level 4;
    #brotli_types text/plain text/css application/json application/javascript application/x-javascript text/xml application/xml application/xml+rss text/javascript;

    # Include additional configurations
    include /etc/nginx/conf.d/*.conf;
}
```
# `default.conf`
```nginx
log_format custom '$http_site_url';

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
    listen 443 ssl http2;
    server_name example.com;
    client_max_body_size 32M;

    location / {
        access_log /var/log/nginx/custom.log custom;
        proxy_read_timeout      300;
        proxy_connect_timeout   300;
        proxy_redirect          off;

        proxy_set_header        Host                $http_host;
        proxy_set_header        X-Real-IP           $remote_addr;
        proxy_set_header        X-Forwarded-For     $proxy_add_x_forwarded_for;
        proxy_set_header        X-Forwarded-Proto   https;
        proxy_set_header        X-Frame-Options     SAMEORIGIN;
        proxy_pass http://172.17.0.1:3000;
    }
    ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;
}
```
# Some Change
## In `nginx.conf`
```bash
sysctl fs.file-max
fs.file-max = value
```
### `worker_rlimit_nofile` is less than the total value of `fs.file-max`
```nginx
worker_processes auto;

events {
    worker_connections 1024;
}

# worker_rlimit_nofile = worker_connections * 2
worker_rlimit_nofile 2048;

http {
    # HTTP config
}
```
## Change of `default.conf`
### Cache
```nginx
server {
    location ~* \.(webp|jpg|jpeg|png|gif|css|js|ico|woff|woff2|tff|svg)$ {
        expires 30d;
        add_header Cache-Control "public, max-age=2592000";
        try_files $uri $uri/ =404;
    }
}
```
### HSTS (HTTP Strict Transport Security)
```nginx
server {
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
}
```
# `stub_status`
```nginx
server {    
    listen 80;
    server_name example.com;

    location = /basic_status {
        stub_status;
    }
}
```
### Now you access to `stub_status`, but it's Unsecured Access to Metrics.
### for secure
```nginx
location /basic_status {
    stub_status;
    allow 192.168.1.0/24;
    allow 127.0.0.1;
    deny all;               # Block access for others
}
```
