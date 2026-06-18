# Quay Registry

```bash
#!/bin/bash

# Setup quay mirror registry for serving openshift mirror images

mkdir ~/quay

curl -L https://developers.redhat.com/content-gateway/rest/mirror/pub/openshift-v4/clients/mirror-registry/latest/mirror-registry.tar.gz -o mirror-registry.tar.gz
mv mirror-registry.tar.gz ~/quay && cd ~/quay
mkdir certs
tar -xzvf mirror-registry.tar.gz

read -p "Have you setup any domain name for your registry?(domain/N)" ANSWER

if [[ "$ANSWER" == "N" || "$ANSWER" == "n" ]]; then
        export IP_ADDR=$(hostname -I | awk '{print $1}')
	export ANSWER=quay.local
	sudo echo "$IP_ADDR    quay.local" >> /etc/hosts


# gen key
openssl genrsa -out certs/rootCA.key 2048
openssl req -x509 -new -nodes -key certs/rootCA.key -sha256 -days 1024 -out certs/rootCA.pem

# sign the certificate
openssl genrsa -out certs/ssl.key 2048
openssl req -new -key certs/ssl.key -out certs/ssl.csr

cat << EOF > certs/openssl.cnf
[req]
req_extensions = v3_req
distinguished_name = req_distinguished_name
[req_distinguished_name]
[ v3_req ]
basicConstraints = CA:FALSE
keyUsage = nonRepudiation, digitalSignature, keyEncipherment
subjectAltName = @alt_names
[alt_names]
DNS.1 = 
EOF

sed -i "s/DNS.1 = /DNS.1 = $ANSWER/" certs/openssl.cnf
openssl x509 -req -in certs/ssl.csr -CA certs/rootCA.pem -CAkey certs/rootCA.key -CAcreateserial -out certs/ssl.cert -days 356 -extensions v3_req -extfile certs/openssl.cnf

./mirror-registry install \
  --quayHostname $ANSWER:8443 \
  --quayRoot ~/quay
  --sslCert certs/ssl.cert
  --sslKey certs/ssl.key
  --targetUsername $USERNAME
  --initUser quay
  --initPassword 12345678

sudo cp certs/rootCA.pem /etc/containers/certs.d/
sudo cp certs/rootCA.pem /etc/docker/certs.d/
sudo cp certs/rootCA.pem /etc/pki/ca-trust/source/anchors/

sudo systemctl restart docker
sudo systemctl restart podman
sudo update-ca-trust extract

podman login -u quay \
  -p 12345678 \
  $ANSWER:8443

echo -e "\n### You can log in by accessing the UI at https://$ANSWER:8443"
```

---

# oc mirror
```bash
#!/bin/bash

# make sure that you download pull-secret.txt in $HOME/downloads

umask 0022

wget https://mirror.openshift.com/pub/openshift-v4/x86_64/clients/ocp/stable/openshift-client-linux.tar.gz
tar -zxvf openshift-client-linux.tar.gz
chmod 551 oc
sudo mv oc /usr/local/bin
rm -f openshift-client-linux.tar.gz

wget https://mirror.openshift.com/pub/openshift-v4/x86_64/clients/ocp/latest/oc-mirror.rhel9.tar.gz
tar -zxvf oc-mirror.rhel9.tar.gz
chmod 551 oc-mirror
sudo mv oc-mirror /usr/local/bin
rm -f oc-mirror.rhel9.tar.gz

if [[ ! command -v docker ]]; then
  curl -fsSL https://get.docker.com -o install-docker.sh
  sudo sh install-docker.sh
  rm -f install-docker.sh
  sudo systemctl start docker
  sudo systemctl enable docker

mkdir -p $HOME/.docker
cat $HOME/downloads/pull-secret.txt | jq . > $HOME/.docker/config.json
export DOCKER_CONFIG=$HOME/.docker/config.json
echo 'export DOCKER_CONFIG=$HOME/.docker/config.json' >> ~/.bashrc
source ~/.bashrc

sudo usermod -aG docker $USER

docker login registry.redhat.io

oc mirror init > imageset-config.yaml
```
Another One:
```bash
#!/bin/bash
set -e

echo "=== OpenShift Mirror Setup Script ==="

# Variables
OC_VERSION="4.18.41"
OC_URL="https://mirror.openshift.com/pub/openshift-v4/x86_64/clients/ocp/${OC_VERSION}/openshift-client-linux-amd64-rhel9.tar.gz"
OC_MIRROR_URL="https://mirror.openshift.com/pub/openshift-v4/x86_64/clients/ocp/latest/oc-mirror.rhel9.tar.gz"
DOWNLOAD_DIR="$HOME/Downloads"

# Step 1: Download and install oc
echo "Downloading oc client ${OC_VERSION}..."
wget $OC_URL -P $DOWNLOAD_DIR
tar -zxvf $DOWNLOAD_DIR/openshift-client-linux-amd64-rhel9.tar.gz -C $DOWNLOAD_DIR
chmod +x $DOWNLOAD_DIR/oc $DOWNLOAD_DIR/kubectl
sudo mv $DOWNLOAD_DIR/oc $DOWNLOAD_DIR/kubectl /usr/local/bin/
oc version --client

# Step 2: Download and install oc-mirror
echo "Downloading latest oc-mirror..."
wget $OC_MIRROR_URL -P $DOWNLOAD_DIR
tar -zxvf $DOWNLOAD_DIR/oc-mirror.rhel9.tar.gz -C $DOWNLOAD_DIR
chmod +x $DOWNLOAD_DIR/oc-mirror
sudo mv $DOWNLOAD_DIR/oc-mirror /usr/local/bin/
oc mirror version

# Step 3: Configure pull secret
echo "Configuring pull secret..."
cat $DOWNLOAD_DIR/pull-secret | jq . > ./auths.json
mkdir -p $XDG_RUNTIME_DIR/containers
cp ./auths.json $XDG_RUNTIME_DIR/containers/auth.json
sudo systemctl restart podman
podman login registry.redhat.io

# Step 4: Create imageset-config.yaml
echo "Creating imageset-config.yaml..."
cat > imageset-config.yaml << 'EOF'
kind: ImageSetConfiguration
apiVersion: mirror.openshift.io/v2alpha1
mirror:
  platform:
    channels:
    - name: stable-4.18
      type: ocp
      minVersion: 4.18.41
      maxVersion: 4.18.41
    graph: true
  operators:
  - catalog: registry.redhat.io/redhat/redhat-operator-index:v4.18
    packages:
    - name: cluster-logging
      channels:
      - name: stable-6.4
    - name: cluster-observability-operator
      channels:
      - name: stable
    - name: container-security-operator
      channels:
      - name: stable-3.16
    - name: loki-operator
      channels:
      - name: stable-6.4
    - name: openshift-gitops-operator
      channels:
      - name: latest
  helm: {}
EOF

# Step 5: Run oc mirror
echo "Starting oc-mirror. This will take a while..."
oc mirror --config=./imageset-config.yaml file://ocp-4-18-41 --v2

# Step 6: Package working directory
echo "Packaging working directory..."
tar -czvf working-dir.tar.gz working-dir/

echo "=== Done ==="
echo "Output files:"
echo "  - ocp-4-18-41/mirror_000001.tar"
echo "  - working-dir.tar.gz"
```

---

# CRC
```bash
#!/bin/bash

# crc brings minimal OpenShift Container Platform 4 cluster to your local computer (for testing and development purpose)
echo
echo -e "\033[90m### minimum requirements:"
echo -e "\033[90m### 4 physical CPU cores - supported architecture for Openshift Container Platform: intel 64, AMD64, Apple silicon"
echo -e "\033[90m### at least 16 GB (my suggestion) of memory on the system (or 14 GB available)"
echo -e "\033[90m### at least 50 GB of storage (or 35 GB available)\033[0m"
echo

get_available_memory() {
    memory=$(free -g | awk 'NR==2 {print $7}')
    echo "$memory"
}

check_cpu_arch() {
    arch=$(lscpu | awk 'NR==1 {print $2}')
    case $arch in
        x86_64)
            echo -e "\033[90m### cpu architecture --> Intel 64 or AMD64\033[0m"
	    ;;
	arm64|aarch64)
            echo -e "\033[90m### cpu architecture --> ARM64\033[0m"
	    ;;
	*)
	    echo -e "### \033[31mwarning!!! cpu architecture maybe not supported.\033[0m cpu architecture --> $arch"
	    ;;
    esac	    
}

echo -e "\033[31m### Warning!!! you should not run this script as root. But user must be in sudoers.\033[0m"
echo -e "\033[90m### Note: Make sure not using 172 range ip address for proxing or anything else."
echo -e "\033[90m### And finally make sure to download pull-secret.txt file from this url https://console.redhat.com/openshift/create/local and place in $HOME/Downloads\033[0m"
echo
read -p "Are you ok with this conditions? (Y/N)" condition

if [[ "$condition" == "N" || "$condition" == "n" ]]; then
    echo -e "\033[90mExiting script...\033[0m"
    exit 1
fi

available_memory=$(get_available_memory)

if (( $(echo "$available_memory < 14" | bc -l) )); then
    echo -e "\033[90m### Available memory is less than 14 GB. Exiting install.\033[0m"
    exit 1
else
    check_cpu_arch
fi

echo -e "\033[90m### Note: Be sure that you have 40 GB free on the system.\033[0m"
read -p "### You should sibscribe first into Redhat account. did you do that? (Y/N)" value

if [[ "$value" == "N" || "$value" == "n" ]] ; then
    echo -e "\033[90m### Exiting...\033[0m"
    exit 1
elif [[ "$value" == "Y" || "$value" == "y" ]]; then
    sudo yum update -y
    sudo yum install -y curl wget NetworkManager
fi

if ! command -v crc &> /dev/null ; then
    mkdir -p ~/bin
    wget https://developers.redhat.com/content-gateway/rest/mirror/pub/openshift-v4/clients/crc/latest/crc-linux-amd64.tar.xz
    tar zxvf crc-linux-amd64.tar.xz
    mv crc-linux-*-amd64/crc ~/bin
    rm -rf crc-linux-*-amd64/ crc-linux-amd64.tar.xz
    echo "export PATH=$PATH:$HOME/bin" >> ~/.bashrc
    source ~/.bashrc
else
    echo -e "\033[90m### CRC already installed."
    echo -e "\033[90m### Start setup crc...\033[0m"
fi

if ! command -v crc > /dev/null ; then
    echo "CRC is not installed. Please try again..."
    exit 

crc setup
crc start -p ~/Downloads/pull-secret.txt

# Setup the oc environment

crc oc-env
eval $(crc oc-env)

echo -e "\033[90m### You can login as developer user and logout using: \n1.oc login -u developer -p developer https://api.crc.testing:6443 \n2.oc logout\n"
echo -e "\033[90m### You can login as platform's admin and logout using: \n1.oc login -u kubeadmin -p password https://api.crc.testing:6443 \n2.oc logout\n"
echo -e "\033[90m### Start graphical interface: crc console"
echo -e "\033[90m### Display cluster's status: crc status"
echo -e "\033[90m### Shut down the OpenShift cluster: crc stop"
echo -e "\033[90m### Delete or kill the OpenShift cluster: crc delete"
echo
echo -e "\033[90mHave a nice day :)\033[0m"
```

---

# OCP vSphere
```bash
#!/bin/bash


echo -e "\033[90m"
echo "### OpenShift is a family of containerization software products developed by Red Hat."
echo "### A hybrid cloud platform as a service built around Linux containers orchestrated and managed by Kubernetes on a foundation of Red Hat Enterprise Linux.\n"

echo "### This script uses installer-provisioned infrastructure methodology on vSphere platform."
echo "### Before Beginning instruction make sure that vCenter installed and it is configured, Create specific Datacenter and Cluster according your needs."

echo -e "\n### There are some conditions for installation become successful:"
echo -e "### 1.Access to port 443 and esxi hosts\n### 2.Control Plane nodes must be able to reach vCenter and ESXi hosts on port 443 for installation"
echo -e "### 3.Vmware vSphere version 7 update 2+ or vSphere version 8 update 1+ (These releases support Container Storage Interface)\n"
echo -e "### 4.Only single Vmware vCenter can be supported for installation\n### 5.Vmware license\033[0m\n"

echo "                    Version requirements for vSphere virtual environments"
echo -e "     -----------------------------------------------------------------------------\n     | Virtual environment product | Required version                            |"
echo -e "     -----------------------------------------------------------------------------\n     | VMware virtual hardware     | 15 or larter                                |"
echo -e "     -----------------------------------------------------------------------------\n     | vSphere ESXi hosts          | 7.0 Update 2 or later;8.0 Update 1 or later |"
echo -e "     -----------------------------------------------------------------------------\n     | vCenter host                | 7.0 Update 2 or later;8.0 Update 1 or later |"
echo -e "     -----------------------------------------------------------------------------\n                                                                                  "

echo "                   Minimum supported vSphere version for VMware components"
echo -e "     -----------------------------------------------------------------------------\n     | Hypervisor                    | vSphere 7.0 Update 2 or later             |"
echo -e                                                                                     "     |                               | vSphere 8.0 Update 1 or later             |"
echo -e                                                                                     "     |                               | with virtual hardware version 15          |"
echo -e "     -----------------------------------------------------------------------------\n     | Optional: Networking (NSX-T)  | vSphere 7.0 Update 2 or later; vSphere    |"
echo -e                                                                                     "     |                               | 8.0 Update 1 or later                     |"
echo -e "     -----------------------------------------------------------------------------\n     | CPU micro-architecture        | x86-64-v2 or higher                       |"
echo -e "     -----------------------------------------------------------------------------\n                                                                                  "

echo -e "\033[90m### You must ensure that the time on your ESXi hosts is synchronized before you install OpenShift Container Platform.\n"

echo -e "### You must configure the network connectivity between machines to allow OpenShift Container Platform cluster components to communicate:\n"
echo -e "     Ports used for all machine to all machine communications\n     VRRP --> N/A\n     ICMP --> N/A\n     TCP --> 1936,9000-9999,10250-10259"
echo -e "     UDP --> 4789,6081,9000-9999,500,4500\n     TCP/UDP --> 30000-32767\n     ESP --> N/A\n"
echo -e "     Ports used for all machibe to control plane communications\n     TCP --> 6443\n"
echo -e "     Ports used for control plane to control plane communicatios\n     TCP --> 2379-2380\n"

echo -e "### Make sure that no third-party vSphere CSI driver already installed in the cluster. OpenShift Container Platform does not overwrite it!\n### Note: The VMware vSphere CSI Driver Operator is supported only on clusters deployed with platform: vsphere in the installation manifest...\n"

echo -e "### The installation program requires access to an account with privileges to read and create the required resources.\n### Using an account that has global administrative privileges is the simplest way to access all of the necessary permissions.\n"

echo -e "### Make sure that you have at least 856 GB free storage on your ESXi host for following resources to create (for more compute nodes please consider more storage)\n"

echo -e "### A standard OpenShift Container Platform installation creates the following vCenter resources:\n     1.One Folder\n     2.One Tag category\n     3.One Tag\n     4.Virtual Machines: - 1 Template - 1 Bootstrap node - 3 Control Plane nodes - 3 Compute nodes\n"

echo -e "### Network Requirements:\n### Use DHCP for the network and ensure that the DHCP server is configured to provide persistent IP addresses to the cluster machines."
echo -e "### Note: You do not need to use the DHCP for the network if you want to provision nodes with static IP addresses."
echo -e "### Configure the default gateway to use the DHCP server. All nodes must be in the same VLAN. You cannot scale the cluster using a second VLAN as a Day 2 operation."
echo -e "### Note: It is recommended that each OpenShift Container Platform node in the cluster must have access to a Network Time Protocol server that is discoverable via DHCP."
echo -e "### For a network that uses DHCP, an installer-provisioned vSphere installation requires two static IP addresses:\n### 1.API --> cluster API   2.Ingress --> Ingress cluster traffic"
echo -e "### You must provide these IP addresses to the installation program when you install the OpenShift Container Platform cluster."
echo -e "### You must create DNS records for two static IP addresses in the appropriate DNS server for the vCenter instance that hosts your OpenShift Container Platform cluster:\n"
echo -e "\n\033[0m                                                                     Required DNS records"
echo -e "     ------------------------------------------------------------------------------------------------------------------------------------------------------"
echo -e "     | Component   | Record                                | Description                                                                                  |"
echo -e "     |----------------------------------------------------------------------------------------------------------------------------------------------------|"
echo -e "     | API VIP     | api.<cluster_name>.<base_domain>.     | This DNS A/AAAA or CNAME (Canonical Name) record must point to the load balancer for the     |"
echo -e "     |             |                                       | control plane machines. This record must be resolvable by both clients external to the       |"
echo -e "     |             |                                       | cluster and from all the nodes within the cluster.                                           |"
echo -e "     |----------------------------------------------------------------------------------------------------------------------------------------------------|"
echo -e "     | Ingress VIP | *.apps.<cluster_name>.<base_domain>.  | A wildcard DNS A/AAAA or CNAME record that points to the load balancer that targets the      |"
echo -e "     |             |                                       | machines that run the Ingress router pods, which are the worker nodes by default. This       |"
echo -e "     |             |                                       | record must be resolvable by both clients external to the cluster and from all the nodes     |"
echo -e "     |             |                                       | within the cluster.                                                                          |"
echo -e "     ------------------------------------------------------------------------------------------------------------------------------------------------------"

echo -e "\n\n\033[90m### Static IP addresses for vSphere nodes (I use this method):\n"
echo -e "### You can provision bootstrap, control plane, and compute nodes to be configured with static IP addresses in environments where DHCP does not exist"
echo -e "### To configure this environment, you must provide values to the platform.vsphere.hosts.role parameter in the install-config.yaml file. (That we use later)"
echo -e "### Point: After you deployed your cluster to run nodes with static IP addresses, you can scale a machine to use one of these static IP addresses."
echo -e "### Additionally, you can use a machine set to configure a machine to use one of the configured static IP addresses.\033[0m\n\n\n"

echo -e "\033[31m### Please make sure that you have download pull-secret.txt file from source https://console.redhat.com/openshift/install/vsphere/installer-provisioned \n and place it in $HOME/Downloads"
echo -e "### You can also install non FIPS version of installer if you think that it is better...(Anyway I will continue with FIPS version compatible with RHEL 9)\n"

read -p "### Do you agree with this conditions? (Y/N)" condition

if [[ "$condition" != "Y" && "$condition" != "y" ]]; then
    echo -e "\033[90m### Exiting installer...\033[0m"
    exit 1
fi

echo -e "\033[90m### Preparing to install a cluster..."

if ! command -v openshift-install-fips &> /dev/null ; then
    wget https://mirror.openshift.com/pub/openshift-v4/x86_64/clients/ocp/stable/openshift-install-rhel9-amd64.tar.gz
    tar zxvf openshift-install-rhel9-amd64.tar.gz
    chmod 551 openshift-install-fips
    sudo mv openshift-install-fips /usr/local/bin
    rm -f openshift-install-rhel9-amd64.tar.gz
fi

if ! command -v oc &> /dev/null ; then
    wget https://mirror.openshift.com/pub/openshift-v4/x86_64/clients/ocp/stable/openshift-client-linux.tar.gz
    tar zxvf openshift-client-linux.tar.gz
    chmod 551 oc
    chmod 551 kubectl
    sudo mv oc /usr/local/bin
    sudo mv kubectl /usr/local/bin
    rm -f README.md openshift-client-linux.tar.gz
fi

if ! command -v oc-mirror &> /dev/null ; then    
    wget https://mirror.openshift.com/pub/openshift-v4/x86_64/clients/ocp/latest/oc-mirror.rhel9.tar.gz
    tar zxvf oc-mirror.rhel9.tar.gz
    chmod 551 oc-mirror
    sudo mv oc-mirror /usr/local/bin
    rm -f oc-mirror.rhel9.tar.gz
fi

if ! ( command -v openshift-install-fips &> /dev/null ) && ! ( command -v oc &> dev/null ) && ! ( command -v oc-mirror &> /dev/null ) ; then
    echo "Binaries failed to install. Please try again..."
    exit 1
fi

ssh-keygen -t rsa -N '' -f $HOME/.ssh/id_openshift
eval "$(ssh-agent -s)"
ssh-add $HOME/.ssh/id_openshift

mkdir -p ~/.docker/
cat ~/Downloads/pull-secret | jq > ~/.docker/pull-secret.json

sh quay-registry.sh

mkdir cluster-config
cd cluster-config

cat << EOF > install-config.yaml
apiVersion: v1
baseDomain: example.ir
compute:
- architecture: amd64
  hyperthreading: Enabled
  name: worker
  platform: {}
  replicas: 0
controlPlane:
  architecture: amd64
  hyperthreading: Enabled
  name: master
  platform: {}
  replicas: 3
metadata:
  creationTimestamp: null
  name: hb
networking:
  clusterNetwork:
  - cidr: 10.128.0.0/14
    hostPrefix: 23
  machineNetwork:
  - cidr: 192.168.254.0/24
  networkType: OVNKubernetes
  serviceNetwork:
  - 172.30.0.0/16
platform:
  vsphere:
    failureDomains:
    - name: openshift-failure-domain
      region: openshift-region
      server: 192.168.254.217
      topology:
        computeCluster: /Datacenter-openshift/host/cluster-openshift
        datacenter: Datacenter-openshift
        datastore: /Datacenter-openshift/datastore/DS1
        networks:
        - VM Network
        resourcePool: /Datacenter-openshift/host/cluster-openshift/Resources
      zone: openshift-zone
    vcenters:
    - datacenters:
      - Datacenter-openshift
      password: password
      port: 443
      server: 192.168.254.217
      user: administrator@vsphere.local
    hosts:
    - role: bootstrap
      networkDevice:
        ipAddrs:
        - 192.168.254.213/24
        gateway: 192.168.254.254
        nameservers:
        - 192.168.254.216
    - role: control-plane
      networkDevice:
        ipAddrs:
        - 192.168.254.210/24
        gateway: 192.168.254.254
        nameservers:
        - 192.168.254.216/24
    - role: control-plane
      networkDevice:
        ipAddrs:
        - 192.168.254.211/24
        gateway: 192.168.254.254/24
        nameservers:
        - 192.168.254.216
    - role: control-plane
      networkDevice:
        ipAddrs:
        - 192.168.254.212/24
        gateway: 192.168.254.254/24
        nameservers:
        - 192.168.254.216
    diskType: thin
    clusterOSImage: http://registry.example.ir/openshift/rhcos-vmware.x86_64.ova
publish: External
pullSecret: '{"auths":{"registry.example.ir:5000":{"auth":"auth..."}}}'
sshKey: 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC4tJUZgXaokuo9DXGybcfoR7wnLhOMtoUdlpQq45N0ISUTgixvUNrAiVwONDy3LPyhqbnIqHk7hQGphE8nHIeubciMm9GCITcq+8kWddazQU1vDks9KfHnsbgYa8bgBdCVkViTmx5WRMciC4rTLwd6DA7lWF14rUTxCnHJz3N0Xx9pHDPsIvPI7u0U39oo5oeQMo1b3lVWxqrMjuUXux/2IRCrHCDeQ7mag9IbSelT0ivSqQp9HguJTKkCemTTKXanmzwEZsosx/kWUP/Z0B1cLXtSC3yNlxtDKrathEXpgm4hJiyQqX+nmatlod7ZmR6VPYurUBGDH0qZyDcALkr5 arisariana@mirror-host'
additionalTrustBundle: | 
  -----BEGIN CERTIFICATE-----
  MIID3.....
  -----END CERTIFICATE-----
imageDigestSources:
  - mirrors:
    - registry.example.ir:5000/openshift
    source: quay.io/openshift-release-dev/ocp-release
  - mirrors:
    - registry.example.ir:5000/openshift
    source: quay.io/openshift-release-dev/ocp-v4.0-art-dev
    EOF

    openshift-install create cluster --dir .
```
