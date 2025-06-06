```yml
version: '3.8'

services:
  nexus:
    user: "0"
    image: sonatype/nexus3
    container_name: nexus
    environment:
      - SONATYPE_DIR=/opt/sonatype
      - NEXUS_HOME=/opt/sonatype/nexus
      - NEXUS_DATA=/nexus-data
      - SONATYPE_WORK=/opt/sonatype/sonatype-work
      #- INSTALL4J_ADD_VM_PARAMS=-Xms2703m -Xmx2703m -XX:MaxDirectMemorySize=2703m
      - INSTALL4J_ADD_VM_PARAMS=-Xms4096m -Xmx8192m -XX:MaxDirectMemorySize=4096m
    volumes:
      - ./nexus-data:/nexus-data
    ports:
      - "8081:8081"
      - "8083:8083"
      - "8084:8084"
      - "8483:8483"
    restart: always
    command: ["/opt/sonatype/nexus/bin/nexus", "run"]

volumes:
  nexus-data:
```

Find the admin password with:
```bash
docker exec -it nexus cat /nexus-data/admin.password
```
After Change admin password:
  - **✔ Disable anonymous access**

---

## To push docker image from local to nexus:
1. **in Nexus Security -> Realms Tab -> Enable the `Docker Bearer Token Realm`**
2. **in Repositories -> create repository -> docker (hosted)**
3. **✔ check HTTP > put 8084 in the fill**
4. **✔ Enable Docker V1 API**
```bash
# in local machine
docker login nesxusIP-URL:8084
docker pull image:tag
docker tag image:tag nesxusURL:8084/image:tag
```
add `insecure-registries` in `/etc/docker/daemon.json`
```json
{
  "insecure-registries": ["nesxusIP-URL:8084"]
}
```
```bash
docker push nesxusIP-URL:8084/image:tag
```

---

# Auto login
## Config `.docker/config.json`
```bash
echo -n 'username:password' | base64 -w0
```
```json
{
  "auths": {
    "nexus.ir": {
      "auth": "BGVtbYk3ZHAtqXs=",
      "email": "you@example.com"
    }
  }
}
```

---

## Or use ca.crt (ca.crt is the `private-key` of site that generate with openssl or letsencrypt)
- openssl genrsa -out domain.key 2048 openssl req -new -key domain.key -out domain.csr
- copy the content of `private-key` and paste it in the ca.crt file in this path on linux machine that want to connect to registry.
### For Docker
- Copy the `private-key` of site.
- Put it in this dicrecory: `/etc/docker/certs.d/<registry-host>:<port>/ca.crt`
- `sudo mkdir -p /etc/docker/certs.d/nexus.ir`
- `sudo nano -p /etc/docker/certs.d/nexus.ir/ca.crt`
- `sudo systemctl restart docker`
- `docker login nexus.ir`

if use TLS Self-Signed and got error:
- `sudo cp ca.crt /etc/pki/ca-trust/source/anchors/`
- `sudo update-ca-trust`


### For podman:
- `sudo mkdir -p /etc/containers/certs.d/nexus.ir`
- `sudo cp ca.crt /etc/containers/certs.d/nexus.ir/ca.crt`

if use TLS Self-Signed and got error:
- `sudo cp ca.crt /etc/pki/ca-trust/source/anchors/`
- `sudo update-ca-trust`

---

# Podman
```bash
sudo nano /etc/containers/registries.conf
```
```bash
[[registry]]
location = "nesxusIP-URL:8084"
insecure = true
```

---

# nginx conf
```conf
server {
    listen 80;
    server_name nexus.ir;
    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }
    location / {
        return 301 https://$host$request_uri;
    }
}
server {
    listen 443 ssl;
    server_name nexus.ir;

    client_max_body_size 32M;
    # client_max_body_size 5G; # if got error: 413 Request Entity Too Large

    location / {
        proxy_read_timeout      300;
        proxy_connect_timeout   300;
        proxy_redirect          off;

        proxy_set_header        Host                $http_host;
        proxy_set_header        X-Real-IP           $remote_addr;
        proxy_set_header        X-Forwarded-For     $proxy_add_x_forwarded_for;
        proxy_set_header        X-Forwarded-Proto   https;
        proxy_set_header        X-Frame-Options     SAMEORIGIN;
        proxy_pass http://172.17.0.1:8081;
    }
    ssl_certificate /etc/letsencrypt/live/nexus.ir/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/nexus.ir/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;
}
```

---

# Use nexus for Other file
1. **in Repositories -> Create repository -> raw (hosted)**
Nexus Address
```bash
http://nexus.local:8081
```
Upload File with `curl`
```bash
curl -u admin:yourpassword --upload-file ./myfile.zip http://nexus.local:8081/repository/raw-files/myfolder/myfile.zip
```
Download File wirh `curl`
```bash
curl -u admin:yourpassword http://nexus.local:8081/repository/raw-files/myfolder/myfile.zip -O
```
