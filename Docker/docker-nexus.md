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
# Generate [CA trust](https://github.com/Saeed7596/DevOps/blob/main/SSL%26TLS/OpenSSL%20CA%20Trust.md)

# defulat.conf - with self-sign openssl
```conf
server {
    listen 80;
    server_name nexus.example.com;
    location / {
        return 301 https://$host$request_uri;
    }
}
server {
    listen 443 ssl;
    server_name nexus.example.com;

    client_max_body_size 5G;

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
    ssl_certificate     /etc/nginx/certs/nexus.crt;
    ssl_certificate_key /etc/nginx/certs/nexus.key;
}

server {
    listen 80;
    server_name docker.example.com;
    location / {
        return 301 https://$host$request_uri;
    }
}
server {
    listen 443 ssl;
    server_name docker.example.com;

    client_max_body_size 5G;

    location / {
        proxy_read_timeout      300;
        proxy_connect_timeout   300;
        proxy_redirect          off;

        proxy_set_header        Host                $http_host;
        proxy_set_header        X-Real-IP           $remote_addr;
        proxy_set_header        X-Forwarded-For     $proxy_add_x_forwarded_for;
        proxy_set_header        X-Forwarded-Proto   https;
        proxy_set_header        X-Frame-Options     SAMEORIGIN;
        proxy_pass http://172.17.0.1:8084;
    }
    ssl_certificate     /etc/nginx/certs/nexus.crt;
    ssl_certificate_key /etc/nginx/certs/nexus.key;
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

---

# Delete a Specific Docker Image:
## 🔹 Method 1: Remove a specific tag from a repository
For example, if your repository name is `docker-hosted` and the desired image is `myapp:1.0`:
1. Find the relevant asset:
```bash
curl -u admin:yourpassword \
  -X GET "http://<nexus-host>:8081/service/rest/v1/assets?repository=docker-hosted" \
  | jq .
```
The output will contain a list of assets. Look for the part where the `path` looks like this:
```bash
myapp/manifest/1.0
```
Each asset has an `id`.

2. Delete asset using `id`:
```bash
curl -u admin:yourpassword \
  -X DELETE "http://<nexus-host>:8081/service/rest/v1/assets/<asset-id>"
```

## 🔹 Method 2: Delete the entire Image (all tags)
To completely delete an image from a repository, you can use the Component API:
1. Find the component:
```bash
curl -u admin:yourpassword \
  -X GET "http://<nexus-host>:8081/service/rest/v1/components?repository=docker-hosted" \
  | jq .
```
Search for the component with the desired name (e.g. `myapp`).
2. Delete
```bash
curl -u admin:yourpassword \
  -X DELETE "http://<nexus-host>:8081/service/rest/v1/components/<component-id>"
```

# 🔹 Important Note
* Nexus does not have a default UI for deleting image/tag in the docker registry; the API must be used.
* After deleting, it is better to run garbage collection from `Admin → Cleanup → Compact Blob Store` to free up disk space.

# Helpful Links
* [Components API](https://help.sonatype.com/en/components-api.html#ComponentsAPI-DeleteComponent)
* [Delete Docker Images From Nexus Repository 3](https://support.sonatype.com/hc/en-us/articles/360009696054-Options-to-Delete-Docker-Images-From-Nexus-Repository-3)

---

# Automate Delete
Just give it the `repo`, `image`, and `tag`, and it will find it on Nexus and delete it.
```bash
nano delete_image.sh
```
```bash
#!/bin/bash
# Script to delete a Docker image (tag) from Nexus Repository using REST API

# --- Configuration ---
NEXUS_URL="http://<nexus-host>:8081"   # Nexus base URL
REPO="docker-hosted"                   # Docker repository name
USER="admin"                           # Nexus username
PASS="yourpassword"                    # Nexus password

# --- Input Arguments ---
IMAGE_NAME=$1   # e.g. myapp
IMAGE_TAG=$2    # e.g. 1.0

if [[ -z "$IMAGE_NAME" || -z "$IMAGE_TAG" ]]; then
  echo "Usage: $0 <image-name> <tag>"
  exit 1
fi

echo "[*] Searching for image $IMAGE_NAME:$IMAGE_TAG in repository $REPO ..."

# Query components in the repository
COMPONENTS=$(curl -s -u $USER:$PASS \
  -X GET "$NEXUS_URL/service/rest/v1/components?repository=$REPO")

# Extract component id for the given image:tag
COMP_ID=$(echo $COMPONENTS | jq -r ".items[] | select(.name==\"$IMAGE_NAME\" and .version==\"$IMAGE_TAG\") | .id")

if [[ -z "$COMP_ID" || "$COMP_ID" == "null" ]]; then
  echo "[!] Image $IMAGE_NAME:$IMAGE_TAG not found in repository $REPO."
  exit 1
fi

echo "[*] Found component ID: $COMP_ID"
echo "[*] Deleting..."

# Delete the component
curl -s -u $USER:$PASS -X DELETE "$NEXUS_URL/service/rest/v1/components/$COMP_ID"

if [[ $? -eq 0 ]]; then
  echo "[✔] Successfully deleted $IMAGE_NAME:$IMAGE_TAG from $REPO."
else
  echo "[✘] Failed to delete image."
fi
```
```bash
chmod +x delete_image.sh
```
```bash
./delete_image.sh
```

---

# LDAP Integration
## [first step](https://help.sonatype.com/en/ldap.html)
## [second step](https://help.sonatype.com/en/ldap-integration.html)

---

# 1. Enable LDAP Authentication Realm
**Settings -> Security -> Realms** 

* Move the `LDAP Realm` beneath the Local Authenticating Realm in the list.

---

# 2. Create LDAP Connection Profile
**Settings -> Security -> LDAP**

---

# 3. Create Role
**Administration → Security → Roles**
* Type: Nexus role
* Applied Privileges:
    * `nx-repository-view-docker-<repo_name>-read` → pull

    * `nx-repository-view-docker-<repo_name>-add` → push

    * `nx-repository-view-docker-<repo_name>-delete` → delete

Assign this role to the desired LDAP user or group.
