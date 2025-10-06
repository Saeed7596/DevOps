# [Openshift Container Platform (OCP) Installing on Oare Metal User Provisioned Infrastructure (UPI)](https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/installing_on_bare_metal/user-provisioned-infrastructure)

## Preparing
* Helper machine include these tools (`oc`, `oc-mirror`, `openshift-install`, `butane`)
  * ❗**Note**: Version of ocp must be equal to these tool. So download the correct [version](https://mirror.openshift.com/pub/openshift-v4/x86_64/clients/).
* DNS Record
* Generate self-sign TLS files with OpenSSL & Use a [CA Trust](https://github.com/Saeed7596/DevOps/blob/main/SSL%26TLS/OpenSSL%20CA%20Trust.md)
* Nexus as Docker Private Registry - [default.conf](https://github.com/Saeed7596/DevOps/blob/main/SSL%26TLS/OpenSSL%20CA%20Trust.md)
  * disktoMirror 
* HAproxy as load balancer

---

# Install two Red Hat 9.x. One of them using as nexus and hepler. And another one for HAProxy.

```bash
sudo hostnamectl set-hostname --static nexus

bash

hostname
```

```bash
sudo nano /etc/hosts
```
```
127.0.0.1   localhost
127.0.0.1   nexus
```

## Verify
```bash
cat /etc/hostname # output ===> nexus
ping nexus
```
Do this step on haproxy machine too.

---

# Chrony in Red Hat 9.x
```bash
sudo nano /etc/chrony.conf 
```
```nano
server <ntp-ip-address> iburst
```
```bash
sudo firewall-cmd --permanent --add-port=123/udp

sudo firewall-cmd --reload
```
```bash
sudo systemctl status chronyd
sudo systemctl restart chronyd
```
# Verify
```bash
chronyc sources -v 
chronyc tracking 
```
You should see the internal NTP server as `NTP source` and the status will show `^*` or `^+` indicating that it is synchronized.

And `Leap status` should be `Normal`.

---

# [HAProxy](https://github.com/Saeed7596/DevOps/blob/main/LoadBalancer/HAProxy-OpenShift.md)
**Note**: At the first for `443` and `80` use the master ip. After Scaling the cluster with worker change `443` and `80` with worker ip
If you are using HAProxy as a load balancer and SELinux is set to enforcing, you must ensure that the HAProxy service can bind to the configured TCP port by running 
`setsebool -P haproxy_connect_any=1`

If you are using HAProxy as a load balancer, you can check that the `haproxy` process is listening on ports `6443, 22623, 443, and 80` by running `netstat -nltupe` on the HAProxy node.

Open these ports:`6443, 22623, 443, and 80`
```bash
sudo firewall-cmd --permanent --add-port=6443/tcp
sudo firewall-cmd --permanent --add-port=22623/tcp
sudo firewall-cmd --permanent --add-port=443/tcp
sudo firewall-cmd --permanent --add-port=80/tcp

sudo firewall-cmd --reload

sudo firewall-cmd --list-ports
```

---
# [DNS](https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/installing_on_bare_metal/user-provisioned-infrastructure#installation-dns-user-infra_installing-restricted-networks-bare-metal) 
# Verify DNS Records
```bash
dig +noall +answer @<nameserver_ip> api.<cluster_name>.<base_domain>

dig +noall +answer @<nameserver_ip> api-int.<cluster_name>.<base_domain>

dig +noall +answer @<nameserver_ip> random.apps.<cluster_name>.<base_domain>

dig +noall +answer @<nameserver_ip> bootstrap.<cluster_name>.<base_domain>
```
```bash
dig +noall +answer @<nameserver_ip> -x <haproxy-ip-address>

#output:
5.1.168.192.in-addr.arpa. 604800	IN	PTR	api-int.ocp4.example.com. 
5.1.168.192.in-addr.arpa. 604800	IN	PTR	api.ocp4.example.com. 
```

---

# Install nodes with Red Hat Core OS live iso
```bash
ssh-keygen -t ed25519 -N '' -f <path>/<file_name>

# Specify the path and file name for your SSH private key, such as ~/.ssh/id-openshift

eval "$(ssh-agent -s)"

ssh-add <path>/<file_name>

#Example output
#Identity added: /home/<you>/<path>/<file_name> (<computer_name>)
```

```bash
mkdir <installation_directory>
```

You must name this configuration file `install-config.yaml`.

```bash
nano <installation_directory>/install-config.yaml
```
### install-config.yaml
```yaml
apiVersion: v1
baseDomain: example.com
compute: 
- hyperthreading: Enabled 
  name: worker
  replicas: 0 
controlPlane: 
  hyperthreading: Enabled 
  name: master
  replicas: 3 
metadata:
  name: openshift 
networking:
  clusterNetwork:
  - cidr: 10.128.0.0/14 
    hostPrefix: 23 
  networkType: OVNKubernetes 
  serviceNetwork: 
  - 172.30.0.0/16
platform:
  none: {} 
fips: false
# echo -n 'username:password' | base64 -w0 (username and password of docker.example.com)
pullSecret: '{"auths": {"docker.example.com": {"auth": "YW...=="}}}' 
# Your SSH public key (for accessing nodes)
sshKey: 'ssh-ed25519 AAAA...'
# Trust bundle for internal registry (e.g., self-signed cert)
additionalTrustBundle: | 
  -----BEGIN CERTIFICATE-----
  ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ
  (Use CA Trust if you are using self-sign TLS and paste the rootCA.crt here)
  -----END CERTIFICATE-----
# Copy from ~/local-mirror/working-dir/cluster-resources/idms-oc-mirror.yaml
imageDigestSources: 
- mirrors:
  - docker.example.com/<local_repository_name>/release
  source: quay.io/openshift-release-dev/ocp-release
- mirrors:
  - docker.example.com/<local_repository_name>/release
  source: quay.io/openshift-release-dev/ocp-v4.0-art-dev
```

```bash
openshift-install create manifests --dir <installation_directory>
```

## Configuring chrony time service
If the cluster is not running yet, after you generate manifest files, add the MachineConfig object file to the 
`<installation_directory>/openshift` directory, and then continue to create the cluster.
```bash
nano 99-master-chrony.bu
```
```bu
variant: openshift
version: 4.17.0
metadata:
  name: 99-master-chrony 
  labels:
    machineconfiguration.openshift.io/role: master 
storage:
  files:
  - path: /etc/chrony.conf
    mode: 0644 
    overwrite: true
    contents:
      inline: |
        server <ntp-ip-address> iburst 
        driftfile /var/lib/chrony/drift
        makestep 1.0 3
        rtcsync
        logdir /var/log/chrony
```

---

```bash
nano 99-worker-chrony.bu
```
```bu
variant: openshift
version: 4.17.0
metadata:
  name: 99-worker-chrony 
  labels:
    machineconfiguration.openshift.io/role: worker 
storage:
  files:
  - path: /etc/chrony.conf
    mode: 0644 
    overwrite: true
    contents:
      inline: |
        server <ntp-ip-address> iburst 
        driftfile /var/lib/chrony/drift
        makestep 1.0 3
        rtcsync
        logdir /var/log/chrony
```

```bash
butane 99-worker-chrony.bu -o 99-worker-chrony.yaml
```
Copy `99-master-chrony.yaml` & `99-worker-chrony.yaml` to `<installation_directory>/openshift` directory

**Note**: If cluster is running, apply to the cluster.
```bash
oc apply -f ./99-worker-chrony.yaml
```

---

# Create ignition files.
After run this command the manifest and openshift directory will be destroyed.
```bash
openshift-install create ignition-configs --dir <installation_directory>
```
Ignition config files are created for the `bootstrap`, `control plane`, and `compute` nodes in the installation directory:
```tree
.
├── auth
│   ├── kubeadmin-password
│   └── kubeconfig
├── bootstrap.ign
├── master.ign
├── metadata.json
└── worker.ign
```

## We need to spin up and HTTP server. We can do this by utilizing python.
```bash
sudo firewall-cmd --permanent --add-port=8080/udp

sudo firewall-cmd --reload
```
```bash
python3 -m http.server 8080
```

---

# Installing RHCOS by using an ISO image
Boot the Physical Server with `iLO` and mount the iso file.

ISO file names resemble the following example:

`rhcos-<version>-live.<architecture>.iso`

in rhcos live:
### For find the correct partition. For example `/dev/sda`
```bash
lsblk
```
### Config Network
```bash
sudo nmtui
```
Enter this value:
* Address: 192.168.1.10/26
  * IP/26 means: Subnet Mask = 255.255.255.192
* Gateway: 192.168.1.1
* DNS: <nameserver_ip>
* DNS: <nameserver_ip>

Go to `Activate a connection` Down and Up.
#### Verify
```bash
nmcli device status
ip -c a
```

```bash
curl -k http://<HTTP_server>:8080/bootstrap.ign
```

## coreos-installer install
```bash
sudo coreos-installer install \
  --ignition-url=http://<HTTP_server>:8080/bootstrap.ign \
  --insecure-ignition --copy-network \
  /dev/sda --offline
```

Install `bootstrap` and `masters`

---

# Monitoring the Installation
### On helper node
```bash
openshift-install wait-for bootstrap-complete --dir=install-dir --log-level=info
```
* To view different installation details, specify `warn`, `debug`, or `error` instead of `info`.

🔹 After the bootstrap process is `complete`, `remove` the bootstrap machine from the load balancer `(haproxy)`.
🔹 Now you cat **delete** the bootstrap machine.

---

```bash
export KUBECONFIG=<installation_directory>/auth/kubeconfig
```
# After this command you should see the `console` url and kubeadmin password
```bash
openshift-install wait-for install-complete --dir=install-dir --log-level=debug
```

---

# Verify Cluster
```bash
oc get nodes
```
## If don't see the some of the nodes (like `master2`)
```bash
oc get csr
```
To approve them individually, run the following command for each valid CSR:
```bash
oc adm certificate approve <csr_name>
```
To approve all **pending** CSRs, run the following command:
```bash
oc get csr -o go-template='{{range .items}}{{if not .status}}{{.metadata.name}}{{"\n"}}{{end}}{{end}}' | xargs --no-run-if-empty oc adm certificate approve
```
## Watch the cluster components come online:
```bash
watch -n5 oc get co

watch -n5 oc get clusteroperators
```

---

# Scaling a user-provisioned cluster with the Bare Metal Operator
Create a backup:
```bash
cp -r install-dir install-dir-backup-$(date +%Y%m%d-%H%M)
```
```bash
openshift-install create ignition-configs --help
```
```bash
openshift-install create manifests --dir install-dir
```
Copy `99-master-chrony.yaml` & `99-worker-chrony.yaml` to `install-dir/openshift`
```bash
install-dir/openshift/99-master-chrony.yaml
install-dir/openshift/99-worker-chrony.yaml
```
```bash
openshift-install create ignition-configs --dir <installation_directory> --overwrite
```
Now you can use the ignition files again. Because these file will be expired after 24 hours.
