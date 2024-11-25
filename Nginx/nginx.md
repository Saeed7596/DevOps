# Default
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
# High Performance
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

    server_tokens off;
    # Client header and body settings
    client_header_buffer_size 1k;
    large_client_header_buffers 4 8k;
    client_body_buffer_size 128k;
    client_max_body_size 32M;

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
