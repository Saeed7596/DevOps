# [Vault](https://developer.hashicorp.com/vault) Integration with cert-manager on OpenShift (Air-Gapped Environment)

## Scenario Overview

- **Use Case:** Use HashiCorp Vault as an internal Certificate Authority (CA) for all certificates in OpenShift, including internal TLS and Ingress.
- **Environment:** Air-gapped OpenShift cluster in a secure data center (e.g., banking environment).
- **Vault Location:** Installed on a separate VM within the same data center, outside the OpenShift cluster.

---

## 1. Install Vault on a Separate VM

### Step 1: Install Vault 
Ubuntu/Debian
```bash
wget -O - https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(grep -oP '(?<=UBUNTU_CODENAME=).*' /etc/os-release || lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
sudo apt update && sudo apt install vault
```
CentOS/RHEL
```bash
sudo yum install -y yum-utils
sudo yum-config-manager --add-repo https://rpm.releases.hashicorp.com/RHEL/hashicorp.repo
sudo yum -y install vault
```
or Install Binary
```bash
wget https://releases.hashicorp.com/vault/1.20.0/vault_1.20.0_linux_amd64.zip
unzip vault_1.15.2_linux_amd64.zip
sudo install vault /usr/local/bin/
```
#### Verify
```bash
vault -v
```

---

### Step 2: Create Vault Configuration

```hcl
# /etc/vault.d/vault.hcl
listener "tcp" {
  address = "0.0.0.0:8200"
  tls_cert_file = "/etc/vault/tls/vault.crt"
  tls_key_file  = "/etc/vault/tls/vault.key"
}
storage "file" {
  path = "/opt/vault/data"
}
ui = true
disable_mlock = true
```
Another One:
```hcl
listener "tcp" {
  address     = "0.0.0.0:8200"
  tls_disable = true
}
storage "raft" {
  path    = "./vault/data"
  node_id = "node1"
}
api_addr = "http://127.0.0.1:8200"
cluster_addr = "https://127.0.0.1:8201"
ui = true
```

### Step 3: Enable and Start Vault

```bash
sudo mkdir -p /opt/vault/data /etc/vault/tls
sudo cp vault.crt vault.key /etc/vault/tls/
sudo chmod 600 /etc/vault/tls/*
vault server -config=/etc/vault.d/vault.hcl
```

In another terminal:

```bash
export VAULT_ADDR=https://<vault-ip>:8200
vault operator init
vault operator unseal
vault login <root_token>
```

---

## 2. Enable and Configure PKI Backend

```bash
vault secrets enable pki
vault secrets tune -max-lease-ttl=87600h pki

vault write pki/root/generate/internal   common_name="vault.local"   ttl=87600h

vault write pki/config/urls   issuing_certificates="https://vault.infra.local:8200/v1/pki/ca"   crl_distribution_points="https://vault.infra.local:8200/v1/pki/crl"

vault write pki/roles/cert-manager   allowed_domains="svc.cluster.local,cluster.local"   allow_subdomains=true   max_ttl="72h"
```

---

## 3. Configure Kubernetes Auth in Vault

### Prerequisites

```bash
oc create sa cert-manager-vault -n cert-manager
oc adm policy add-cluster-role-to-user system:auth-delegator -z cert-manager-vault -n cert-manager

export K8S_HOST=$(oc config view -o jsonpath='{.clusters[0].cluster.server}')
export SA_JWT=$(oc sa get-token cert-manager-vault -n cert-manager)
export K8S_CAB=$(oc get cm kube-root-ca.crt -n cert-manager -o jsonpath='{.data.ca\.crt}')
```

### Configure Vault

```bash
vault auth enable kubernetes

vault write auth/kubernetes/config   token_reviewer_jwt="$SA_JWT"   kubernetes_host="$K8S_HOST"   kubernetes_ca_cert="$K8S_CAB"

vault policy write cert-manager-policy - <<EOF
path "pki/*" {
  capabilities = ["read", "list", "create", "update"]
}
EOF

vault write auth/kubernetes/role/cert-manager   bound_service_account_names=cert-manager-vault   bound_service_account_namespaces=cert-manager   policies=cert-manager-policy   ttl=24h
```

---

## 4. Define Vault ClusterIssuer

```yaml
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: vault-cluster-issuer
spec:
  vault:
    server: https://vault.infra.local:8200
    path: pki/sign/cert-manager
    caBundle: <BASE64_ENCODED_CA_CERT>
    auth:
      kubernetes:
        mountPath: /var/run/secrets/kubernetes.io/serviceaccount
        role: cert-manager
        serviceAccountRef:
          name: cert-manager-vault
          namespace: cert-manager
```

To get CA in base64:

```bash
base64 -w0 vault.crt
```

---

## 5. Requesting a Certificate (Test)

```yaml
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: test-cert
  namespace: default
spec:
  secretName: test-cert-tls
  issuerRef:
    name: vault-cluster-issuer
    kind: ClusterIssuer
  commonName: test.default.svc.cluster.local
  dnsNames:
    - test.default.svc.cluster.local
  duration: 24h
  renewBefore: 6h
```

---

## 6. Using Bank-Provided CA for Router

- You **can use** a bank-provided CA for OpenShift Ingress/Router separately from Vault.
- Upload the cert manually or through cert-manager if the bank provides a subordinate CA/API.
- Ensure **trust bundle** includes both Vault's CA and the bank's CA across all nodes and pods.

---

## Security Notes

- Enable audit logging in Vault.
- Use HSM or secure storage for Vault root keys.
- Restrict Vault's access only to required components and namespaces.
- Use short TTLs for certificates and rely on automatic rotation.

---

## Summary

- Vault acts as a full internal CA with secure integration via Kubernetes Auth.
- cert-manager handles issuance and renewal transparently.
- Optional: Use external CA (bank) for public-facing routes.

---

# 🎯 Another Way 

## ✅ 1. Prerequisites on the VM
* A Linux machine (preferably RHEL, CentOS Stream or Ubuntu)
* Root or sudo access
* Firewall open between this VM and the cluster (port 8200)
* A valid hostname and DNS setup (e.g. vault.infra.local)
* A valid TLS certificate installed (or a temporary self-signed one for testing)

## ✅ 2. Install Vault (Binary)
```bash
# Download latest version
curl -O https://releases.hashicorp.com/vault/1.20.0/vault_1.20.0_linux_amd64.zip
unzip vault_1.15.4_linux_amd64.zip
sudo mv vault /usr/local/bin/

# Create a Vault-specific user
sudo useradd --system --home /etc/vault.d --shell /bin/false vault
```
## ✅ 3. Setting Paths and Files
```bash
sudo mkdir -p /etc/vault.d /var/lib/vault /opt/vault/tls
sudo chown -R vault:vault /etc/vault.d /var/lib/vault /opt/vault
```
Place the TLS certificate (e.g. `/opt/vault/tls/vault.crt` & `vault.key`) and create the `vault.hcl` file:

* Note: The `vault.crt` and `vault.key` files must have been generated previously.
  * self-sign:
  ```bash
  openssl req -newkey rsa:2048 -nodes -keyout vault.key -x509 -days 365 \
    -out vault.crt -subj "/CN=vault.infra.local"
  ```
  ```bash
  sudo cp vault.crt vault.key /opt/vault/tls/
  sudo chmod 600 /opt/vault/tls/*
  ```
But it's better to use official CA.

## ✅ 4. Configuration file `/etc/vault.d/vault.hcl`
```bash
listener "tcp" {
  address       = "0.0.0.0:8200"
  tls_cert_file = "/opt/vault/tls/vault.crt"
  tls_key_file  = "/opt/vault/tls/vault.key"
}

storage "file" {
  path = "/var/lib/vault"
}

ui = true

api_addr = "https://vault.infra.local:8200"
cluster_addr = "https://vault.infra.local:8201"
```
If you want HA, you can change the backend to raft or postgresql.

## ✅ 5. Create the systemd file and start Vault
```bash
cat <<EOF | sudo tee /etc/systemd/system/vault.service
[Unit]
Description=Vault service
Requires=network-online.target
After=network-online.target

[Service]
User=vault
Group=vault
ExecStart=/usr/local/bin/vault server -config=/etc/vault.d/vault.hcl
ExecReload=/bin/kill --signal HUP \$MAINPID
KillMode=process
Restart=on-failure
LimitNOFILE=65536

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reexec
sudo systemctl enable vault
sudo systemctl start vault
```

## ✅ 6. Vault initialization
```bash
export VAULT_ADDR='https://vault.infra.local:8200'
vault operator init -key-shares=1 -key-threshold=1

# Output includes:
# - Unseal Key
# - Initial Root Token

vault operator unseal <UNSEAL_KEY>
vault login <ROOT_TOKEN>
```
**Note**:🔐 You should keep these keys secure. It is recommended to use key-shares=5 and threshold=3 for HA.

## ✅ 7. Enabling PKI in Vault
```bash
vault secrets enable pki
vault secrets tune -max-lease-ttl=87600h pki

vault write pki/root/generate/internal \
    common_name="vault-ca.infra.local" ttl=87600h

vault write pki/config/urls \
    issuing_certificates="https://vault.infra.local:8200/v1/pki/ca" \
    crl_distribution_points="https://vault.infra.local:8200/v1/pki/crl"
```

## ✅ 8. Create Role for cert-manager
```bash
vault write pki/roles/cert-manager \
    allowed_domains="svc.cluster.local,example.local" \
    allow_subdomains=true \
    max_ttl="72h"
```

# 🎯 Next step: Connect OpenShift to Vault and define VaultIssuer in cert-manager
## ✅ Prerequisites
First of all, make sure that:
* cert-manager is installed on OpenShift (with Red Hat Operator)
* Vault is accessible to OpenShift Pods on a TLS address like https://vault.infra.local:8200
* A Role is defined in Vault to issue certificates (like cert-manager)
* You have created a Token or Kubernetes Auth for cert-manager

## ✅ 1. Using Token Auth
In Vault, write a policy for cert-manager:
```bash
# in file -> cert-manager-policy.hcl
path "pki/*" {
  capabilities = ["read", "list", "create", "update"]
}
```
Then apply:
```bash
vault policy write cert-manager-policy cert-manager-policy.hcl
```

## ✅ 2. Create a token for cert-manager with this policy
```bash
vault token create -policy="cert-manager-policy" -ttl=8760h
```
Example output:
```bash
Key                  Value
---                  -----
token                s.RANDOMTOKENSTRING
```
Keep the token above, because we need it in OpenShift.

## ✅ 3. Create a Secret for the token in OpenShift
We assume your project (namespace) is `cert-manager`. If not, change it.
```bash
oc create secret generic vault-token \
  --from-literal=token=s.RANDOMTOKENSTRING \
  --namespace=cert-manager
```

## ✅ 4. Defining VaultIssuer or ClusterIssuer
```bash
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: vault-cluster-issuer
spec:
  vault:
    server: https://vault.infra.local:8200
    path: pki/sign/cert-manager
    caBundle: <VAULT_CA_BUNDLE_BASE64>
    auth:
      tokenSecretRef:
        name: vault-token
        key: token
```
🔹 Replace:
* `vault.infra.local` with the actual `Vault hostname` or `IP`
* Generate the caBundle value with the following command:
  ```bash
  # On the client, base64 the vault.crt file:
  base64 -w0 vault.crt
  ```

## ✅ 5. Test getting Certificate
```bash
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: test-cert
  namespace: default
spec:
  secretName: test-cert-tls
  issuerRef:
    name: vault-cluster-issuer
    kind: ClusterIssuer
  commonName: test.default.svc.cluster.local
  dnsNames:
    - test.default.svc.cluster.local
  duration: 24h
  renewBefore: 6h
```

## ✅ Result
After creating this Certificate, cert-manager contacts Vault, issues a cert, and stores it in Secret test-cert-tls.



