# OpenShift Offline Mirror Installation Guide

> Automating OpenShift Image Mirroring for Air-Gapped or Private Environments.

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
  wget https://mirror.openshift.com/pub/openshift-v4/x86_64/clients/ocp/stable/openshift-client-linux.tar.gz
  tar -zxvf openshift-client-linux.tar.gz
  chmod 551 oc
  sudo mv oc /usr/local/bin/
  rm -f openshift-client-linux.tar.gz
else
  echo "oc already installed."
fi

echo "Installing oc-mirror..."
if ! command -v oc-mirror &> /dev/null; then
  wget https://mirror.openshift.com/pub/openshift-v4/x86_64/clients/ocp/latest/oc-mirror.rhel9.tar.gz
  tar -zxvf oc-mirror.rhel9.tar.gz
  chmod 551 oc-mirror
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

### 4. Login to Red Hat Registry
```bash
docker login registry.redhat.io
```

### 5. Generate ImageSet Config
```bash
oc mirror init > imageset-config.yaml
```
⚠ Customize imageset-config.yaml as needed (OpenShift version, target registry, match `catalog and openshift version`, etc.)

### 6. Start Mirroring to Local Directory
```bash
REGISTRY_AUTH_FILE=$HOME/Downloads/pull-secret oc mirror --config imageset-config.yaml file://local-mirror

REGISTRY_AUTH_FILE=$HOME/Downloads/pull-secret oc mirror --config imageset-config.yaml file://local-mirror -v=5

#oc mirror --config imageset-config.yaml file://local-mirror -a $HOME/Downloads/pull-secret
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

### update oc mirror to v2
```bash
REGISTRY_AUTH_FILE=$HOME/Downloads/pull-secret oc mirror --v2 --config imageset-config.yaml file://local-mirror
```

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
REGISTRY_AUTH_FILE=$HOME/Downloads/pull-secret oc mirror --config imageset-config.yaml file://local-mirror -v=5

echo "------ Done ------"
```
```bash
chmod +x mirror.sh
./mirror.sh
```
