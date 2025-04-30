# OpenShift Offline Mirror Installation Guide (RedHat9 OS)

> Automating OpenShift Image Mirroring for Air-Gapped or Private Environments.
Follow this [Link](https://docs.redhat.com/en/documentation/openshift_container_platform/4.16/html/disconnected_installation_mirroring/about-installing-oc-mirror-v2)
---

## Prerequisites

| Requirement | Details |
|-------------|---------|
| OS | Linux (RHEL / CentOS / Fedora / Ubuntu) |
| Tools | wget, jq, curl, tar |
| Pull Secret | Download from [Red Hat Console](https://console.redhat.com/openshift/downloads#tool-pull-secret) and save it as: `$HOME/Downloads/pull-secret` |
| Disk Space | Depends on the OpenShift release (Expect 100GB+ for full mirror) |

---

## Steps

### 1. Install OpenShift CLI (oc) & oc-mirror

```bash
#!/bin/bash

set -e
umask 0022

echo "Installing OpenShift CLI..."
if ! command -v oc &> /dev/null; then
  wget https://mirror.openshift.com/pub/openshift-v4/x86_64/clients/ocp/stable/openshift-client-linux-amd64-rhel9.tar.gz
  tar -zxvf openshift-client-linux-amd64-rhel9.tar.gz
  chmod +x oc kubectl
  sudo mv oc kubectl /usr/local/bin
  rm -f openshift-client-linux-amd64-rhel9.tar.gz
else
  echo "oc already installed."
fi

echo "Installing oc-mirror..."
if ! command -v oc-mirror &> /dev/null; then
  wget https://mirror.openshift.com/pub/openshift-v4/x86_64/clients/ocp/latest/oc-mirror.rhel9.tar.gz
  tar -zxvf oc-mirror.rhel9.tar.gz
  chmod +x oc-mirror
  sudo mv oc-mirror /usr/local/bin/
  rm -f oc-mirror.rhel9.tar.gz
else
  echo "oc-mirror already installed."
fi
```

### 2. Install Docker (if not installed)
```bash
echo "Checking Docker..."
if ! command -v docker &> /dev/null; then
  curl -fsSL https://get.docker.com -o install-docker.sh
  sudo sh install-docker.sh
  rm -f install-docker.sh
fi

sudo usermod -aG docker $USER
newgrp docker
```

### 3. Prepare Docker Auth with Pull Secret
```bash
mkdir -p $HOME/.docker
cat $HOME/Downloads/pull-secret | jq . > $HOME/.docker/config.json
chmod 600 $HOME/.docker/config.json

export DOCKER_CONFIG=$HOME/.docker
echo 'export DOCKER_CONFIG=$HOME/.docker' >> ~/.bashrc
source ~/.bashrc
```
  ### 3.1 . Prepare Private Registry Auth
  ```bash
  cat $HOME/Downloads/pull-secret | jq . > ./auths.json
  ```
  Add your private registry (nexus)
  
  Base64 encode your registry username and password:
  ```bash
  echo -n 'username:password' | base64 -w0
  ```
  Add this part to `auths.json`
  ```json
  "registry.example.com": {
    "auth": "YWRtaW46bXlwYXNzd29yZA==",
    "email": "you@example.com"
  }
  ```
  The final result should look something like this:
  ```json
  {
    "auths": {
      "registry.example.com": {
        "auth": "BGVtbYk3ZHAtqXs=",
        "email": "you@example.com"
      },
      "cloud.openshift.com": {
        "auth": "b3BlbnNo...",
        "email": "you@example.com"
      },
      "quay.io": {
        "auth": "b3BlbnNo...",
        "email": "you@example.com"
      },
      "registry.connect.redhat.com": {
        "auth": "NTE3Njg5Nj...",
        "email": "you@example.com"
      },
      "registry.redhat.io": {
        "auth": "NTE3Njg5Nj...",
        "email": "you@example.com"
      }
    }
  }
  ```
  Save `auth.json` in this path:
  ```bash
  mkdir -p $XDG_RUNTIME_DIR/containers && cp ./auths.json $XDG_RUNTIME_DIR/containers/auth.json
  ```
  Or if you don't have the XDG_RUNTIME_DIR variable, create one manually:
  ```bash
  mkdir -p ~/.config/containers
  cp ./auths.json ~/.config/containers/auth.json
  ```

### 4. Login to Red Hat Registry
```bash
docker login registry.redhat.io
```
For Test:
```bash
docker pull registry.redhat.io/redhat/redhat-operator-index:v4.18
```
### 5. Generate ImageSet Config
Find operator channel and release information
```bash
oc mirror list operators --catalogs --version=4.18
```
Find the available packages within the selected catalog
```bash
oc mirror list operators --catalog=registry.redhat.io/redhat/redhat-operator-index:v4.18
```
Find channels for the selected package
```bash
oc mirror list operators --catalog=registry.redhat.io/redhat/redhat-operator-index:v4.18 --package=rhods-operator
```
```bash
oc mirror init > imageset-config.yaml
```
⚠ Customize imageset-config.yaml as needed (OpenShift version, target registry, match `catalog and openshift version`, etc.)
YAML Sample:
```yaml
kind: ImageSetConfiguration
apiVersion: mirror.openshift.io/v1alpha2
storageConfig:
  local:
    path: ./
mirror:
  platform:
    channels:
    - name: stable-4.18
      type: ocp
  operators:
  - catalog: registry.redhat.io/redhat/redhat-operator-index:v4.18
    packages:
    - name: serverless-operator
      channels:
      - name: stable
  additionalImages:
  - name: registry.redhat.io/ubi8/ubi:latest
  helm: {}
```
oc-mirror v2 with operator Sample:
```yaml

kind: ImageSetConfiguration
apiVersion: mirror.openshift.io/v2alpha1
mirror:
  platform:
    channels:
    - name: stable-4.18
      type: ocp
  operators:
  - catalog: registry.redhat.io/redhat/redhat-operator-index:v4.18
    packages:
    - name: openshift-gitops-operator
      channels:
      - name: gitops-1.16
    - name: servicemeshoperator
      channels:
      - name: stable
    - name: loki-operator
      channels:
      - name: stable-6.2
    - name: cluster-logging
      channels:
      - name: stable-6.2
    - name: redhat-oadp-operator 
      channels:
      - name: stable-1.4
    - name: openshift-cert-manager-operator
      channels:
      - name: stable-v1
    - name: container-security-operator
      channels:
      - name: stable-3.14
    - name: cluster-observability-operator
      channels:
      - name: stable
  helm: {}
```

### 6. Start Mirroring to Local Directory
```bash
oc mirror --v2 --help
```
### Print actions without mirroring images (Test)
```bash
oc mirror -c <image_set_config_yaml> file://<oc_mirror_workspace_path> --dry-run --v2 
oc mirror -c <image_set_config_yaml> --from file://<oc_mirror_workspace_path> docker://<mirror_registry_url> --dry-run --v2
```
### Partially Disconnected Mode
If you have a system that has access to the Internet and the target registry:
```bash
oc mirror --config=./imageset-config.yaml docker://registry.example.com:5000 --v2
```
### Fully Disconnected Mode
If your system has access to the internet but not to the target registry:
  1. Save the images as a .tar file:​
  ```bash
  oc mirror --config=./imageset-config.yaml file://local-mirror --v2
  ```
  2. Transfer the .tar file to the disconnected environment.
  3. In the disconnected environment, transfer the images to the destination registry:​
  ```bash
  # v2
  oc mirror -c imageset-config.yaml --from file://<file_path> docker://<mirror_registry_url> --v2
  oc mirror -c imageset-config.yaml --from file:///home/<user>/local-mirror/ docker://registry.example.com --v2
  # v1
  oc mirror --from=./mirror_000001.tar docker://registry.example.com --dest-skip-tls --dest-use-http
  ```
### Mirror To Disk (v2)
- Note: Edit `imageset-config.yaml`
  - 1. Change the `apiVersion: mirror.openshift.io/v1alpha2` to `apiVersion: mirror.openshift.io/v2alpha1`
  - 2. Remove `storageConfig`
```bash
oc mirror -c ./imageset-config.yaml file:///home/<user>/oc-mirror/mirror1 --v2
```
### Mirror To Disk (v1)
```bash
mkdir local-mirror
oc mirror --verbose 3 -c imageset-config.yaml file://local-mirror

# REGISTRY_AUTH_FILE=$HOME/Downloads/pull-secret oc mirror --config imageset-config.yaml file://local-mirror -v=3
```

---

Output Directory Structure
```lua
local-mirror/
├── manifests/
└── blobs/
```
This directory contains all necessary files to populate your private registry or prepare for air-gapped installation.

---

### Check
```bash
nano mirror.sh
```
```sh
#!/bin/bash

set -e

echo "------ Check oc command ------"
if ! command -v oc &> /dev/null
then
    echo "❌ oc command not found"
    exit 1
else
    echo "✅ oc found -> version: $(oc version | head -n 1)"
fi

echo "------ Check oc-mirror command ------"
if ! command -v oc-mirror &> /dev/null
then
    echo "❌ oc-mirror not found"
    exit 1
else
    echo "✅ oc-mirror found -> version: $(oc-mirror version || echo 'old oc mirror')"
fi

echo "------ Check pull-secret ------"
if grep -q "registry.redhat.io" $HOME/Downloads/pull-secret; then
    echo "✅ pull-secret looks valid for registry.redhat.io"
else
    echo "❌ pull-secret missing registry.redhat.io credentials"
    exit 1
fi

echo "------ Test Auth with registry.redhat.io ------"
if ! REGISTRY_AUTH_FILE=$HOME/Downloads/pull-secret skopeo inspect docker://registry.redhat.io/redhat/redhat-operator-index:v4.18 &> /dev/null
then
    echo "❌ Cannot access registry.redhat.io/redhat/redhat-operator-index:v4.18"
    echo "Check your pull-secret or subscription permission!"
    exit 1
else
    echo "✅ Access to registry.redhat.io confirmed"
fi

echo "------ Start oc mirror ------"
oc mirror --verbose 3 -c imageset-config.yaml file://local-mirror

echo "------ Done ------"
```
```bash
sudo dnf install -y skopeo
skopeo --version
```
```bash
chmod +x mirror.sh
./mirror.sh
```

---

