# Install Docker:
## remove old docker:
```bash
for pkg in docker.io docker-doc docker-compose docker-compose-v2 podman-docker containerd runc; do sudo apt-get remove $pkg; done
```
You can create a docker.sh file and put this value on it. then run with ./docker.sh
```bash
### Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
```
```bash
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
````
------------------------------------
# Install docker with the china Repo:
```bash
sudo apt-get update
sudo apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    software-properties-common
curl -fsSL https://mirrors.ustc.edu.cn/docker-ce/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository \
   "deb [arch=$(dpkg --print-architecture) https://mirrors.ustc.edu.cn/docker-ce/linux/ubuntu \
   $(lsb_release -cs) \
   stable"
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```
------------------------------------

# Manual Docker Installation on Ubuntu using .deb Packages

If you cannot use Docker's `apt` repository to install Docker Engine, you can download and manually install the `.deb` files for your Ubuntu release. You need to download a new file each time you want to upgrade Docker Engine.

## Steps to Install Docker Engine from a Package

### 1. Go to the Docker Downloads Page
Go to the following URL to find the Docker packages for your Ubuntu version:
[https://download.docker.com/linux/ubuntu/dists/](https://download.docker.com/linux/ubuntu/dists/)

### 2. Select Your Ubuntu Version
From the list, select your Ubuntu version (e.g., `focal` for Ubuntu 20.04).

### 3. Navigate to the Stable Pool Directory
Go to `pool/stable/` and select the applicable architecture:
- `amd64`
- `armhf`
- `arm64`
- `s390x`

### 4. Download the Required `.deb` Files
Download the following `.deb` files for Docker Engine, CLI, containerd, and Docker Compose packages:
- `containerd.io_<version>_<arch>.deb`
- `docker-ce-cli_<version>_<arch>.deb`
- `docker-ce_<version>_<arch>.deb`
- `docker-buildx-plugin_<version>_<arch>.deb`
- `docker-compose-plugin_<version>_<arch>.deb`

### 5. Install the `.deb` Packages
Use the `dpkg` command to install the downloaded packages. Replace the `<version>` and `<arch>` with the corresponding values from the files you downloaded:
```bash
sudo dpkg -i ./containerd.io_<version>_<arch>.deb \
  ./docker-ce-cli_<version>_<arch>.deb \
  ./docker-ce_<version>_<arch>.deb \
  ./docker-buildx-plugin_<version>_<arch>.deb \
  ./docker-compose-plugin_<version>_<arch>.deb
```

### 6. Start the Docker Daemon
The Docker daemon should start automatically after installation. If not, you can start it manually:
```bash
sudo service docker start
sudo systemctl enable docker
```

### 7. Verify Docker Installation
To verify that Docker Engine has been installed successfully, run the following command to test it with the `hello-world` image:
```bash
sudo docker run hello-world
```
This command downloads a test image, runs it in a container, and prints a confirmation message.

### Conclusion
If everything works as expected, you have successfully installed and started Docker Engine manually using `.deb` packages.
------------------------------------
# Check
```bash
docker version
docker --version
docker compose version
sudo docker run hello-world
```
------------------------------------
# Uninstall the Docker Engine, CLI, containerd, and Docker Compose packages:
```bash
sudo apt-get purge docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin docker-ce-rootless-extras
```
Images, containers, volumes, or custom configuration files on your host aren't automatically removed. To delete all images, containers, and volumes:
```bash
sudo rm -rf /var/lib/docker
sudo rm -rf /var/lib/containerd
```
------------------------------------
# change docker registry
### Russian registry
```bash
cat > /etc/docker/daemon.json <<EOF
{ "registry-mirrors" : [ "https://https://dockerhub.firstvds.ru", "https://dockerhub.timeweb.cloud", "https://huecker.io", "https://mirror.gcr.io", "https://c.163.com", "https://registry.docker-cn.com", "https://daocloud.io" ] }
EOF
```
### Your own Nexus registry
```bash
nano /etc/docker/daemon.json
```
```vim
{ "insecure-registries" : [ "IPNexus:port" ] 
}
```
```bash
sudo systemctl restart docker
```
```bash
sudo docker login registry.example.com
```
------------------------------------
# Some helpful docker command:
### Run container after reboot:
```bash
docker run -d --restart unless-stopped <container name>
docker update --restart unless-stopped <container name>
```
----------------------------------
### Copy
```bash
docker cp <container_name>:<path_inside_container> <path_on_host>
docker cp <path_on_host> <container_name>:<path_inside_container>
```
----------------------------------
### Clean cache
```bash
docker system df
docker builder prune

docker volume prune
docker system prune
docker system prune --volumes
#WARNING! This will remove:
        - all stopped containers
        - all networks not used by at least one container
        - all volumes not used by at least one container
        - all dangling images
        - all build cache

Are you sure you want to continue? [y/N] y
```
----------------------------------
### Accses docker to new user:
```bash
usermod -aG docker NEWUSER
```

------------------------------------

# Volume
**Default path = `/var/lib/docker/volumes/`**
# Docker Volume Commands
```bash
#Create a Volume:
docker volume create my_volume

#List Volumes:
docker volume ls

#Inspect a Volume:
docker volume inspect my_volume

#Remove a Volume:
docker volume rm my_volume

#Remove All Unused Volumes:
docker volume prune
```
