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
  wget https://mirror.openshift.com/pub/openshift-v4/x86_64/clients/ocp/stable/openshift-client-linux-amd64-rhel9.tar.gz
  tar -zxvf openshift-client-linux-amd64-rhel9.tar.gz
  chmod +x oc
  sudo mv oc /usr/local/bin
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

### 4. Login to Red Hat Registry
```bash
docker login registry.redhat.io
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
    path: /path/to/disk-rh-ai/metadata
mirror:
  operators:
  - catalog: registry.redhat.io/redhat/redhat-operator-index:v4.16
    targetCatalog: redhat-catalog-v4.16
    packages:
    - name: "jaeger-product"
      channels:
      - name: "stable"
        minVersion: "1.57.0-7"
    - name: "kiali-ossm"
      channels:
      - name: "stable"
        minVersion: "1.73.8"
    - name: "openshift-pipelines-operator-rh"
      channels:
      - name: "latest"
        minVersion: "1.15.1"
    - name: "rhods-operator"
      channels:
      - name: "fast"
        minVersion: "2.11.0"
    - name: "serverless-operator"
      channels:
      - name: "stable"
        minVersion: "1.33.1"
    - name: "servicemeshoperator"
      channels:
      - name: "stable"
        minVersion: "2.5.2-0"
  additionalImages:   
    - name: quay.io/integreatly/prometheus-blackbox-exporter@sha256:35b9d2c1002201723b7f7a9f54e9406b2ec4b5b0f73d114f47c70e15956103b5
    - name: quay.io/modh/caikit-nlp@sha256:0cde6c26e02ec398aea959a1a1bcdc615b86821adb41989e81d03de01124545c
    - name: quay.io/modh/caikit-tgis-serving@sha256:4e907ce35a3767f5be2f3175a1854e8d4456c43b78cf3df4305bceabcbf0d6e2
…
…
…
```

### 6. Start Mirroring to Local Directory
```bash
REGISTRY_AUTH_FILE=$HOME/Downloads/pull-secret oc mirror --config imageset-config.yaml file://local-mirror

REGISTRY_AUTH_FILE=$HOME/Downloads/pull-secret oc mirror --config imageset-config.yaml file://local-mirror -v=5

# oc mirror --verbose 3 -c <image_set_configuration> file://<file_path> --v2
mkdir local-mirror
oc mirror --verbose 3 -c imageset-config.yaml file://local-mirror --v2

# oc mirror --config imageset-config.yaml file://local-mirror -a $HOME/Downloads/pull-secret
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
sudo dnf install -y skopeo
```
```bash
chmod +x mirror.sh
./mirror.sh
```
