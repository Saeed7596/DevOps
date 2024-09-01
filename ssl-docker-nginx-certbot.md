#ssl
#first it should be happened with the user the create the app for example gitlab_ssh
#docker compose file =>file name is  ** docker-nginx.compose **
=====================================================================================
```
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
=====================================================================================
#second step mkdir nginx directory and nano default.conf file
=====================================================================================
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
=====================================================================================
> pay attention to the comment line
#first time run the docker compose with this command line
``` docker compose -f docker-nginx.compose up -d ```
#after that check the logs of certbot container and certbot directory to see the files 
#and the must have the permission of the user of app (gitlab_ssh)
#check ``` ls -l ``` and if the files have anthoer user permission user ``` chown -R gitlab_ssh:gitlab_ssh certbot ``` to change the permission
``` docker compose -f docker-nginx.compose down ```
#maybe the /certbot/conf don't have the "ssl-dhparams.pem" & "options-ssl-nginx.conf" so with ``` nano ssl-dhparams.pem ``` & ``` nano options-ssl-nginx.conf ```
#create this file (with vauleable content!)
#then ``` nano ./nginx/default.conf ``` and uncomment the comment line
#now run the " docker-nginx.compose " again
``` docker compose -f docker-nginx.compose up -d ```



