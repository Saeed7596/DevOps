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

**Note**: Version of ocp must be equal to these tool. So download the correct [version](https://mirror.openshift.com/pub/openshift-v4/x86_64/clients/ocp/). 

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

echo "Installing OpenShift Install..."
if ! command -v openshift-install-fips &> /dev/null ; then
    wget https://mirror.openshift.com/pub/openshift-v4/x86_64/clients/ocp/stable/openshift-install-linux.tar.gz
    tar zxvf openshift-install-linux.tar.gz
    chmod +x openshift-install
    sudo mv openshift-install /usr/local/bin
    rm -f openshift-install-linux.tar.gz
else
  echo "OpenShift Install already installed."
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
  Restart docker
  ```bash
  sudo systemctl restart docker
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

#### How to disk to mirror a Specific Operator Openshift:
```yaml
apiVersion: mirror.openshift.io/v2alpha1
kind: ImageSetConfiguration
mirror:
  operators:
  - catalog: registry.redhat.io/redhat/redhat-operator-index:v<OCP_VERSION> # Replace with your OCP version
    packages:
    - name: <operator-name> # Replace with the exact Operator name
      channels:
      - name: <channel-name> # Replace with the desired channel (e.g., stable, alpha)
```
For example:
```yaml
apiVersion: mirror.openshift.io/v2alpha1
kind: ImageSetConfiguration
mirror:
  operators:
  - catalog: registry.redhat.io/redhat/redhat-operator-index:v4.18
    packages:
    - name: elasticsearch-operator 
      channels:
      - name: stable-5.8
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
### Google Cloud 
* If use Google Cloud for dowmload image
* Make a copy in Bucket!
**Note:
Before creating VM and Google Storage Bucket, you must enable API s that are intended for allowing communication between GCP resources inside your project!**
```bash
cd local-mirror/
gsutil cp mirror_000001.tar gs://sarv-dev-ops-bucket-01/
tar -czvf working-dir.tar.gz working-dir/
gsutil cp working-dir.tar.gz gs://sarv-dev-ops-bucket-01/
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

# Installing on vSphere
0. From the vCenter home page, download the vCenter’s root CA certificates. Click Download trusted root CA certificates in the vSphere Web Services SDK section. The `<vCenter>/certs/download.zip` file downloads. Extract the compressed file that contains the vCenter root CA certificates.
```bash
sudo cp certs/lin/* /etc/pki/ca-trust/source/anchors

sudo update-ca-trust extract
```
2. Generate ssh-key
```bash
ssh-keygen -t rsa -N '' -f $HOME/.ssh/id_openshift
eval "$(ssh-agent -s)"
ssh-add $HOME/.ssh/id_openshift
```
2. Install `openshift-install`
Check
```bash
openshift-install version
```
3. Offline RHCOS image location
```bash
mkdir rhcos
cd rhcos
wget https://mirror.openshift.com/pub/openshift-v4/amd64/dependencies/rhcos/latest/rhcos-vmware.x86_64.ova
```
```bash
python3 -m http.server 8080
```
4. Create `install-config.yaml` file
```bash
mkdir cluster-config
cd cluster-config
```
```bash
nano install-config.yaml
```
Sample:
```yaml
apiVersion: v1
baseDomain: domain.com   # Your base domain (used in *.apps.<cluster-name>.<baseDomain>)
compute:
- architecture: amd64
  hyperthreading: Enabled
  name: worker
  platform:
    vsphere: {}
  replicas: 2
controlPlane:
  architecture: amd64
  hyperthreading: Enabled
  name: master
  platform:
    vsphere: {}
  replicas: 3
metadata:
  creationTimestamp: null
  name: ocp-cluster          # Cluster name (will be used in FQDNs like api.ocp.domain.com)
networking:
  networkType: OVNKubernetes
  clusterNetwork:
  - cidr: 10.128.0.0/14
    hostPrefix: 23
  serviceNetwork:
  - 172.30.0.0/16
  machineNetwork:
  - cidr: 192.168.252.0/23   # Your machine subnet (nmcli connection show ens34)
platform:
  vsphere:
    failureDomains:
    - name: <failure_domain_name>
      region: <default_region_name>
      server: <IP or FQDN of your vCenter server>
      topology:
        computeCluster: "/<data_center>/host/<cluster>"
        datacenter: <data_center>
        datastore: "/<data_center>/datastore/<datastore>"
        networks:
        - <VM_Network_name>
        resourcePool: "/<data_center>/host/<cluster>/Resources/<resourcePool>"
      zone: <default_zone_name>
    vcenters:
    - datacenters:
      - <Name of vSphere Datacenter>
      password: <vSpherePassword!>
      port: 443
      server: <IP or FQDN of your vCenter server>
      user: administrator@vsphere.local
    hosts:
    - role: bootstrap
      networkDevice:
        ipAddrs:
        - 192.168.252.229/23
        gateway: 192.168.253.254
        nameservers:
        - <DNS-IP>
    - role: control-plane
      networkDevice:
        ipAddrs:
        - 192.168.254.224/23
        gateway: 192.168.253.254
        nameservers:
        - <DNS-IP>
    - role: control-plane
      networkDevice:
        ipAddrs:
        - 192.168.254.225/23
        gateway: 192.168.253.254
        nameservers:
        - <DNS-IP>
    - role: control-plane
      networkDevice:
        ipAddrs:
        - 192.168.254.226/23
        gateway: 192.168.253.254
        nameservers:
        - <DNS-IP>
    - role: compute
      networkDevice:
        ipAddrs:
        - 192.168.254.227/23
        gateway: 192.168.253.254
        nameservers:
        - <DNS-IP>
    - role: compute
      networkDevice:
        ipAddrs:
        - 192.168.254.228/23
        gateway: 192.168.253.254
        nameservers:
        - <DNS-IP>
    diskType: thin
    # Offline RHCOS image location
    # if use registry
    clusterOSImage: http://mirror.example.com/upload/rhcos-vmware.x86_64.ova
    # if user local 
    # clusterOSImage: http://<ip-this-host>:8080/rhcos-vmware.x86_64.ova
publish: External
# Paste your pull secret here
pullSecret: |
  {"auths": ...}
# Your SSH public key (for accessing nodes)
sshKey: |
  ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC...
# Trust bundle for internal registry (e.g., Nexus self-signed cert)
additionalTrustBundle: |
  -----BEGIN CERTIFICATE-----
  (cert Nexus or CA internal)
  (Use CA Trust if you are using self-sign TLS and paste the rootCA.crt here)
  -----END CERTIFICATE-----
# Registry mirror for air-gap install
imageDigestMirrors:
  - mirrors:
    - registry.example.com/openshift/release
    source: quay.io/openshift-release-dev/ocp-v4.0-art-dev
  - mirrors:
    - registry.example.com/openshift/release-images
    source: quay.io/openshift-release-dev/ocp-release
```
* Note: `additionalTrustBundle` must be the **CA** or **root signer** (rootCA.crt), not the server-specific TLS certificate (like Nexus or vCenter).
* Usually on the same server or in the path `/etc/ssl/certs/ca.crt`
5. Performing the actual installation
```bash
openshift-install create cluster --dir=<your-folder>
openshift-install create cluster --dir=cluster-config
openshift-install create cluster --dir . --log-level=info
```
* Note: if something get wrong
    ```bash
    openshift-install destroy cluster --dir .
    ```
6. The `kubeconfig` and `kubeadmin-password` files are generated in the same directory.
```bash
export KUBECONFIG=~/cluster-config/auth/kubeconfig
oc login -u kubeadmin -p $(cat ~/cluster-config/auth/kubeadmin-password)
```
```bash
oc whoami
```

---

# Preparation a cluster
After you have mirrored your image set to the mirror registry, you must apply the generated `ImageDigestMirrorSet` (IDMS), `ImageTagMirrorSet` (ITMS), `CatalogSource`, and `UpdateService` to the cluster.
```bash
oc apply -f <path_to_oc-mirror_workspace>/working-dir/cluster-resources
```
**Note**: If wants to apply new cluster-resources, you should keep the old one and then copy all cluster-resources file to another directory like `merged-cluster-resources` then apply!
```bash
cp <path_to_oc-mirror_workspace>/working-dir/cluster-resources/* ~/merged-cluster-resources
```
```bash
oc apply -f merged-cluster-resources/
```

Verification
```bash
oc get imagedigestmirrorset
oc get imagetagmirrorset
oc get catalogsource -n openshift-marketplace
```

---

# Test Cluster
Node status:
```bash
oc get nodes
```
Check the entire cluster status:
```bash
oc get clusteroperators
```
All must be in Available and True status.

Check API and DNS status:
```bash
oc get clusterversion
oc get co dns
oc get co kube-apiserver
```
Log Status
```bash
oc adm must-gather
```
This command collects all the logs necessary for debugging the cluster.

Final Test
```bash
oc get pods -A
oc get projects
oc describe node <node-name>
```

---

# Web Console
```bash
oc get route console -n openshift-console -o jsonpath='{.spec.host}'
```
```js
https://console-openshift-console.apps.<cluster-name>.<baseDomain>
```

---

# Check API Server healthz
```bash
curl -k https://api.openshift.<baseDomain>.com:6443/healthz
```

---

# Install Operator 
### With Web Connsole
1. Log in to the web console.
2. Go to Operators > OperatorHub.
3. Select the desired operator such as MongoDB, Logging, Service Mesh.
4. Click "Install".
5. Select the desired Namespace.
6. Confirm and the installation will begin.

### With CLI
For example install `Elasticsearch Operator`
```bash
oc apply -f - <<EOF
apiVersion: operators.coreos.com/v1alpha1
kind: Subscription
metadata:
  name: elasticsearch-operator
  namespace: openshift-operators
spec:
  channel: stable
  name: elasticsearch-operator
  source: redhat-operators
  sourceNamespace: openshift-marketplace
EOF
```
For operators in an air-gap environment and using the internal registry, change the `source` to, for example, `registry-operators`.

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

#  Deleting the images from disconnected environment 
1. Create a YAML file that deletes previous images:
```bash
oc mirror delete --config delete-image-set-config.yaml --workspace file://<previously_mirrored_work_folder> --v2 --generate docker://<remote_registry>
```
Where:
* `<previously_mirrored_work_folder>`: Use the directory where images were previously mirrored or stored during the mirroring process.
* `<remote_registry>`: Insert the URL or address of the remote container registry from which images will be deleted.
2. Go to the `<previously_mirrored_work_folder>/delete directory` that was created.
3. Verify that the `delete-images.yaml` file has been generated.
4. Manually ensure that each image listed in the file is no longer needed by the cluster and can be safely removed from the registry.
5. After you generate the `delete` YAML file, delete the images from the remote registry:
```bash
oc mirror delete --v2 --delete-yaml-file <previously_mirrored_work_folder>/delete/delete-images.yaml docker:/ <remote_registry>
```
Where:
* `<previously_mirrored_work_folder>`: Specify your previously mirrored work folder.

---

# 🔸 Shut down the nodes in the following order:
🧱 Shutdown order:
🔻 Worker nodes (important: Worker first)

🔻 Master nodes (all three Masters with a few seconds between them(At least 30 to 60 seconds))

🔻 Other servers (like Bastion, Load Balancer, or internal DNS machine)

In vSphere, use the console or govc or PowerCLI to shut down:
```bash
govc vm.power -off -vm openshift-worker-0
govc vm.power -off -vm openshift-worker-1
govc vm.power -off -vm openshift-master-0
govc vm.power -off -vm openshift-master-1
govc vm.power -off -vm openshift-master-2
```

# ✅ Powering up the cluster after a shutdown
🧱 Powering up order:
🔼 Master nodes (first master-0 → wait a few seconds → then master-1 → then master-2)

🔼 Worker nodes

🔼 Other services (like Bastion or Jump server)

Power up each Master with a short interval (like 20-30 seconds) so that etcd starts up properly.

---

# Update [link](https://access.redhat.com/labs/ocpupgradegraph/update_path)

* **Note**:Add `graph: true` to build and push the graph-data image to the mirror registry. The graph-data image is required to create OpenShift Update Service (OSUS). The `graph: true` field also generates the `UpdateService` custom resource manifest. The `oc` command-line interface (CLI) can use the `UpdateService` custom resource manifest to create OSUS. For more information, see About the OpenShift Update Service.

#### 🧰 Step 1: Prepare the offline mirror for the new version
```yaml
kind: ImageSetConfiguration
apiVersion: mirror.openshift.io/v2alpha1
mirror:
  platform:
    channels:
    - name: stable-4.17
      type: ocp
      minVersion: 4.17.35
      maxVersion: 4.17.35
    graph: true
  operators:
  - catalog: registry.redhat.io/redhat/redhat-operator-index:v4.17
    packages:
    - name: elasticsearch-operator
      channels:
      - name: stable-5.8
  helm: {}
```
Get two version:
```bash
kind: ImageSetConfiguration
apiVersion: mirror.openshift.io/v2alpha1
mirror:
  platform:
    channels:
      - name: stable-4.16
        type: ocp
        minVersion: 4.16.43
        maxVersion: 4.16.43
      - name: stable-4.17
        type: ocp
        minVersion: 4.17.35
        maxVersion: 4.17.35
    graph: true
  operators:
    - catalog: registry.redhat.io/redhat/redhat-operator-index:v4.16
      packages:
        - name: cluster-observability-operator 
          channels:
            - name: stable
        - name: cluster-logging 
          channels:
            - name: stable-6.2
        - name: loki-operator 
          channels:
            - name: stable-6.2 
        - name: netobserv-operator 
          channels:
            - name: stable
        - name: openshift-gitops-operator
          channels:
            - name: latest
        - name: servicemeshoperator 
          channels:
            - name: stable
        - name: tempo-product 
          channels:
            - name: stable
    - catalog: registry.redhat.io/redhat/redhat-operator-index:v4.17
      packages:
        - name: cluster-observability-operator 
          channels:
            - name: stable
        - name: cluster-logging 
          channels:
            - name: stable-6.3
        - name: loki-operator 
          channels:
            - name: stable-6.3 
        - name: netobserv-operator 
          channels:
            - name: stable
        - name: openshift-gitops-operator
          channels:
            - name: latest
        - name: servicemeshoperator 
          channels:
            - name: stable
        - name: tempo-product 
          channels:
            - name: stable
  helm: {}
```
```bash
oc mirror --config=imageset-config-4.17.yaml file://local-mirror/ --v2
```
```bash
oc mirror --config=imageset-config-4.17.yaml --from file:///home/<user>/local-mirror/ docker://registry.example.com --v2
```

#### 🛠️ Step 2: Create resources on the air-gap cluster
2.1 Define ImageContentSourcePolicy (ICSP)
```yaml
apiVersion: operator.openshift.io/v1alpha1
kind: ImageContentSourcePolicy
metadata:
  name: mirror-4-17
spec:
  repositoryDigestMirrors:
    - mirrors:
        - registry.example.com/ocp/release
      source: quay.io/openshift-release-dev/ocp-release
    - mirrors:
        - registry.example.com/ocp/release-images
      source: quay.io/openshift-release-dev/ocp-v4.0-art-dev
```
2.2 Defining CatalogSource for operators
```yaml
apiVersion: operators.coreos.com/v1alpha1
kind: CatalogSource
metadata:
  name: redhat-operators
  namespace: openshift-marketplace
spec:
  sourceType: grpc
  image: registry.example.com/olm/redhat-operator-index:v4.17
  displayName: Red Hat Operators
  publisher: Red Hat
```


---

## ✅ Prerequisites
1. Take a full etcd backup
```bash
oc adm cluster-backup /backup/path
```
2. Check version compatibility
Versions should be directly upgradeable. In the case of 4.16 → 4.17, this is usually not a problem.
```bash
oc adm upgrade --allow-explicit-upgrade --to-image <release-image>
```
3. Check out the Cluster.
```bash
oc get clusterversion
oc get clusteroperators
oc get nodes
```

## 🚀 OpenShift Cluster Update Steps
#### 🧩 Step 1: Check the available versions
```bash
oc adm upgrade
```
Or to see suggested versions:
```bash
oc adm upgrade --to-latest
```
#### 📦 Step 2: Apply the upgrade channel (optional)
If the channel is wrong (e.g. it's on `stable-4.16` and you want to go to `4.17`):
```bash
oc patch clusterversion version --type merge -p '{"spec": {"channel": "stable-4.17"}}'
```
#### ⬆️ Step 3: Start the upgrade
If version `4.17.35` was listed:
```bash
oc adm upgrade --to=4.17.35
```
If you are doing it locally or air-gap, you can give an explicit image:
```bash
oc adm upgrade --to-image=quay.io/openshift-release-dev/ocp-release@sha256:<digest>
# or
oc adm upgrade --to-image=registry.example.com/ocp/release@sha256:<digest>
```
#### 🔍 Step 4: Monitor the upgrade status
```bash
watch oc get clusterversion
watch oc get clusteroperators
watch oc get nodes
```
✅ When everything is `Available=True`, `Progressing=False`, `Degraded=False`, the upgrade is complete.

#### 📘 Important Notes
* First, the Control Plane (Master) Nodes are upgraded.
* Then the Worker Nodes are upgraded with drain and reboot respectively.
* During the process, Pods may be moved (Planned Disruption).

#### 📥 Rollback
* OpenShift does not officially support rollback version.
* The only way to rollback: restore etcd from a backup taken before the upgrade
```bash
oc adm cluster-restore /backup/path
```

---

# Debug and ssh
Whenever possible, access to nodes without using SSH, by spawning a debug pod directly from the `oc` command line:

```bash
oc debug node/[node_name]
```
Important note: By design, OpenShift 4 clusters are immutable and rely on Operators to apply cluster changes. In turn, this means that accessing the underlying nodes directly by SSH is not the recommended procedure. Additionally, the nodes will be tainted as accessed.

Workaround
When it is not possible to access the nodes with oc debug node command, it is possible to leverage the ssh protocol for the same:

* Generally, the "SSH keys (Public/Private)" are generated during the cluster installation.
* The "Public Key" is passed inside the install-config.yaml manifest .
* After successful cluster installation, the "Public key" is copied at path `$/home/core/.ssh/authorized_keys` or `/home/core/.ssh/authorized_keys.d` location across the nodes.
* It is possible to use the generated "SSH Private key" to access the nodes as core user by running below command:
```bash
ssh -i /path/to/privatekey core@[master-hostname]
ssh -i /path/to/privatekey core@[worker-hostname]
```
## If you use the same installation machine
* The private key that corresponds to that public key must be on the same machine.
* For example, if you placed the public key from ~/.ssh/id_rsa.pub, the private key is ~/.ssh/id_rsa.

Connection example:
```bash
ssh -i ~/.ssh/id_rsa core@<node-ip>
```
**Note**: The default user in RHCOS is `core`, not `root`.

## If you use a different machine
* You must transfer the private key to that machine (with permission: `chmod 600 id_rsa`).
* You will still connect with the core user.

---

# DEBUG!
Check:
```bash
oc get node
```
Output:
```text
NAME                       STATUS      ROLES                  AGE   VERSION
openshift-v6sts-master-0   Ready       control-plane,master   14d   v1.31.7
openshift-v6sts-master-1   Ready       control-plane,master   14d   v1.31.7
openshift-v6sts-master-2   NotReady    control-plane,master   14d   v1.31.7
openshift-v6sts-worker-0   NotReady    worker                 13d   v1.31.7
openshift-v6sts-worker-1   Ready       worker                 13d   v1.31.7
```
There are two nodes with status: `NotReady`
```bash
oc describe node openshift-v6sts-master-2
oc describe node openshift-v6sts-worker-1
```
* Look for `kubelet` status.
* It may be not ready.
* You can also check `Conditions:` section and look up the date to make sure it's accurate(up-to-date).

Check `CertificateSigningRequest (CSR)`
```bash
oc get csr 
oc adm certificate approve <csr_name>
```
* If you see some are `Pending`, **there is your problem.**  💥
* The `kubelet` can not connect to the `API Server` without Token.
```bash
oc get csr | grep Pending | awk '{print $1}' | xargs oc adm certificate approve
```
## ✅ Now must be solved!

### If the issue is not **Solved** yet,

Use ssh to connect to the nodes that are `NotReady`
```bash
ssh -i ~/.ssh/id_rsa core@<node-ip>
```
```bash
journalctl -u kubelet -f
sudo systemctl status kubelet 
sudo systemctl restart kubelet
```
Sometimes Problem is about the `NTP service`:
```bash
systemctl status chrony-wait.service
systemctl status chronyd
chronyc tracking

sudo systemctl restart chronyd
sudo systemctl enable chronyd
```
Connect the `NTP Server` Manually:
```bash
sudo bash -c 'echo "server <ntp-server-ip> iburst" >> /etc/chrony.conf'
sudo systemctl restart chronyd
```

---
