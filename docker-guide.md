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
```
----------------------------------
### Accses docker to new user:
```bash
usermod -aG docker NEWUSER
```
------------------------------------
# Docker Restart Policies

This document explains the different `restart` policies available in Docker for container restart management.

## Available Restart Policies

### 1. `always`
- **Behavior:** The container is always restarted, regardless of the reason for its stop.
- **Use Case:** Suitable for services that should always be running, even after manual stops.

### 2. `unless-stopped`
- **Behavior:** The container will be restarted automatically unless it was manually stopped by the user (using `docker stop`).
- **Use Case:** Ideal when you want the container to auto-restart after crashes or reboots, but avoid restarting if the user manually stopped it.

### 3. `on-failure[:max-retries]`
- **Behavior:** The container will only restart if it exits with a failure (non-zero exit code). You can also limit the number of restart attempts by specifying `max-retries`.
- **Use Case:** Useful for containers that should only restart in case of a failure, and where you want to control the maximum number of retries.

Example:

```yaml
restart: on-failure:3
```

In this example, the container will restart up to 3 times if it encounters a failure.

## Comparison of Restart Policies

| Policy          | Behavior                                                      |
|-----------------|---------------------------------------------------------------|
| `no`            | Container does not restart automatically (default behavior).   |
| `always`        | Container always restarts, even after manual stop.             |
| `unless-stopped`| Container restarts unless manually stopped by the user.        |
| `on-failure`    | Container restarts only if it fails (non-zero exit code).      |

