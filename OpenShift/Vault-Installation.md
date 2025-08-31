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

#### Auto Complete
```bash
vault -autocomplete-install
```

---

### Step 2: Create Vault Configuration

```hcl
# /etc/vault.d/vault.hcl
ui = true

api_addr = "https://<vault-ip>:8200"

storage "file" {
  path = "/opt/vault/data"
}

listener "tcp" {
  address       = "0.0.0.0:8200"
  tls_cert_file = "/opt/vault/tls/tls.crt"
  tls_key_file  = "/opt/vault/tls/tls.key"
}
```
**Note**: `api_addr` should be the same as what `cert-manager` is going to use. `IP` or `DNS` accessible from within the cluster.
**Note**: Use `https` for `api_addr` because we have tls.crt & tls.key in listener tcp.

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
cluster_addr = "https://127.0.0.1:8201"  # For HA or replication
ui = true
```

### Step 3: Enable and Start Vault

```bash
sudo mkdir -p /opt/vault/data /opt/vault/tls/
sudo cp vault.crt vault.key /opt/vault/tls/
sudo chmod 600 /opt/vault/tls/*
vault server -config=/etc/vault.d/vault.hcl
```

In another terminal:

```bash
export VAULT_ADDR=https://<vault-ip>:8200
export VAULT_SKIP_VERIFY=true                # Temporary only! Delete after initial setup.
vault operator init
vault operator unseal
vault login <root_token>
```
#### What should I do after changing the vault.hcl file?
1. Test the config file (optional but useful):
```bash
vault server -config=/etc/vault.d/vault.hcl -log-level=debug
```
* This will run Vault in the foreground. Useful for testing but not for production

2. Restart the Vault service:
```bash
sudo systemctl daemon-reexec
sudo systemctl restart vault
```
if don't use systemd:
```bash
pkill vault
vault server -config=/etc/vault.d/vault.hcl
```
3. Check the status:
```bash
sudo systemctl status vault
# or
vault status
```

### Step 4: Open the Port
```bash
sudo firewall-cmd --list-ports
sudo firewall-cmd --list-services

sudo firewall-cmd --add-port=8200/tcp --permanent
sudo firewall-cmd --reload
```

---

## 2. Enable and Configure PKI Backend

```bash
vault secrets enable pki
vault secrets tune -max-lease-ttl=87600h pki

vault write pki/root/generate/internal common_name="vault.example.com" alt_names="vault.example.com,localhost" ip_sans="<vault-ip>" ttl=87600h

vault write pki/config/urls issuing_certificates="https://<vault-ip>:8200/v1/pki/ca" crl_distribution_points="https://<vault-ip>:8200/v1/pki/crl"

vault write pki/roles/cert-manager allowed_domains="*.example.com,192.168.252.0/24,192.168.254.0/24,*.openshift.example.com,svc.cluster.local,cluster.local" allow_subdomains=true allow_ip_sans=true max_ttl="72h"
```

**Note**: If you want more specific domains to be supported (e.g. apps.infra.local), add them to allowed_domains.
* `common_name`: Same as Vault's main DNS (preferably the internal bank name or registered DNS)

* `alt_names`: This is so that the same name is in DNS on the SAN.

* `ip_sans`: The actual IP address you connect to Vault from the cluster (important!)

**Note**: If you're using Vault's own TLS certificate (not the PKI one), make sure it includes the IP address:

* Option A: Add IP SAN to existing Vault TLS certificate

```bash
# Check current Vault TLS configuration
vault read sys/config/state/sanitized

# Update Vault config with proper TLS certificate that includes IP SANs
```

* Option B: Temporarily disable TLS verification (not recommended for production)
```yaml
# In your cert-manager configuration, add:
spec:
  issuerRef:
    name: vault-issuer
  vault:
    server: https://<vaul-ip>:8200
    path: pki/sign/cert-manager
    caBundle: <your-ca-cert>
    # Add this line to skip TLS verification (development only)
    skipTLSVerify: true
```

---

## 3. Configure Kubernetes Auth in Vault

### Prerequisites

```bash
oc create sa cert-manager -n cert-manager
oc adm policy add-cluster-role-to-user system:auth-delegator -z cert-manager -n cert-manager

export K8S_HOST=$(oc config view -o jsonpath='{.clusters[0].cluster.server}')
export SA_JWT=$(oc create token cert-manager -n cert-manager --audience=vault)
export K8S_CAB=$(oc get cm kube-root-ca.crt -n cert-manager -o jsonpath='{.data.ca\.crt}')
```
Check the variables, Should not be empyt!
```bash
echo $K8S_HOST
echo $SA_JWT
echo $K8S_CAB
```

  * Note: After create sa, check the sa to have token. `oc get sa cert-manager -n cert-manager`
  * `oc describe sa cert-manager -n cert-manager`
    * if Tokens = none **but if the `echo $SA_JWT` and `oc get sa cert-manager -n cert-manager` return value, you don't need to apply this!**
      * Method 1:
      ```bash
      # Create secret with service account token
      oc create secret generic cert-manager-vault-token -n cert-manager --from-literal=token=$(oc create token cert-manager -n cert-manager --audience=vault --duration=8760h)

      # Verify the secret was created
      oc get secret cert-manager-vault-token -n cert-manager -o yaml

      # Check the token exists
      oc get secret cert-manager-vault-token -n cert-manager -o jsonpath='{.data.token}' | base64 -d
      ```
      Method 2:
      ```bash
      kubectl apply -f - <<EOF
      apiVersion: v1
      kind: Secret
      metadata:
        name: vault-token-sa
        namespace: cert-manager
        annotations:
          kubernetes.io/service-account.name: cert-manager
      type: kubernetes.io/service-account-token
      EOF
      ```
      
### Configure auth method in Vault
```bash
vault auth enable kubernetes

vault write auth/kubernetes/config token_reviewer_jwt="$SA_JWT" kubernetes_host="$K8S_HOST" kubernetes_ca_cert="$K8S_CAB" disable_local_ca_jwt=false
```
```bash
vault policy write cert-manager-policy - <<EOF
path "pki/sign/cert-manager" {
  capabilities = ["create", "update"]
}
path "pki/roles/cert-manager" {
  capabilities = ["read"]
}
EOF
```
* ❗ Important Note: Only the `pki/sign/cert-manager` and `pki/roles/cert-manager` paths should be accessible. Avoid giving full access to `pki/*` except in testing.
```bash
vault policy write cert-manager-policy - <<EOF
path "pki/*" {
  capabilities = ["read", "list", "create", "update"]
}
EOF
```

### **Create Vault Role**
```bash
vault write auth/kubernetes/role/cert-manager bound_service_account_names=cert-manager bound_service_account_namespaces=cert-manager policies=cert-manager-policy ttl=24h audience=vault
```

---

## 4. Define Vault Role, Rolebinding, ClusterIssuer
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: cert-manager-token-role
  namespace: cert-manager
rules:
  - apiGroups: [""]
    resources: ["serviceaccounts/token"]
    verbs: ["create"]
```
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: cert-manager-token-binding
  namespace: cert-manager
subjects:
  - kind: ServiceAccount
    name: cert-manager
    namespace: cert-manager
roleRef:
  kind: Role
  name: cert-manager-token-role
  apiGroup: rbac.authorization.k8s.io
```
```yaml
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: vault-cluster-issuer
spec:
  vault:
    server: https://<vault-ip>:8200
    path: pki/sign/cert-manager
    caBundle: <BASE64_ENCODED_CA_CERT>
    # Add this line to skip TLS verification (development only)
    skipTLSVerify: true
    auth:
      kubernetes:
        mountPath: /v1/auth/kubernetes
        # mountPath: /var/run/secrets/kubernetes.io/serviceaccount
        role: cert-manager
        serviceAccountRef:
          name: cert-manager
          namespace: cert-manager
```

`caBundle` = the `issuing_ca` content after runnig `vault write pki/root/generate/internal`
To get CA in base64:
* save `<issuing_ca_content>"` as a file like `is_ca.crt`:
```bash
cat is_ca.crt | base64 -w0
# Or
echo "<issuing_ca_content>" | base64 -w0
```
Verify:
```bash
openssl x509 -in /opt/vault/tls/tls.crt -text -noout | grep CA

openssl x509 -in is_ca.crt -text -noout | grep CA 
```

### 4.2 ClusterIssuer with secretRef:
```yaml
# vault-issuer.yaml
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: vault-cluster-issuer
spec:
  vault:
    server: https://vault.example.com:8200
    path: pki/sign/cert-manager
    auth:
      kubernetes:
        mountPath: /v1/auth/kubernetes
        role: cert-manager
        secretRef:
          name: cert-manager-vault-token
          key: token
```
Verify ClusterIssuer Status
```bash
oc describe clusterissuer vault-cluster-issuer
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
  secretName: test-tls
  issuerRef:
    name: vault-cluster-issuer
    kind: ClusterIssuer
  commonName: test.example.com
  dnsNames:
    - test.example.com
    - www.test.example.com
  duration: 24h
  renewBefore: 6h
```
Verify:
```bash
oc get certificate -n cert-manager
oc describe certificate test-cert -n default
```
Check Generated Secret
```bash
oc get secret test-tls -n cert-manager -o yaml
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

## Restart & Describe
```bash
oc rollout restart deploy cert-manager -n cert-manager
oc describe clusterissuer vault-cluster-issuer
```

---

## Delete
#### On the Vault server:
```bash
# Disable PKI engine (Delete the CA you created)
vault secrets disable pki

# Disable Kubernetes auth (Delete auth method)
vault auth disable kubernetes

# Delete policy
vault policy delete cert-manager-policy
```
#### On the OpenShift cluster:
```bash
# Delete ClusterIssuer
oc delete clusterissuer vault-cluster-issuer

# Delete ServiceAccount
oc delete sa cert-manager-vault -n cert-manager

# Delete Role and RoleBinding
oc delete role cert-manager-vault-token-role -n cert-manager
oc delete rolebinding cert-manager-vault-token-binding -n cert-manager
```

---

# Troubleshooting
Common Issues and Solutions
1. TLS Certificate Validation Error
Error: `x509: cannot validate certificate for IP because it doesn't contain any IP SANs`

Solution:

```bash
# Regenerate Vault certificate with IP SANs
vault write pki/root/generate/internal \
  common_name="vault.example.com" \
  ip_sans="192.168.252.223" \
  alt_names="vault.example.com" \
  ttl=87600h
```
2. Authentication Errors
Error: permission denied or service account not found

Solution:

```bash
# Verify service account exists
oc get sa cert-manager -n cert-manager

# Check Vault role configuration
vault read auth/kubernetes/role/cert-manager
```
3. Token Expiration
Error: `token expired` or `permission denied`

Solution:

```bash
# Renew the secret token
oc delete secret cert-manager-vault-token -n cert-manager
oc create secret generic cert-manager-vault-token \
  -n cert-manager \
  --from-literal=token=$(oc create token cert-manager -n cert-manager --audience=vault --duration=8760h)
```
Debug Commands
```bash
# Check Vault authentication
vault login -method=kubernetes role=cert-manager

# Test PKI signing
vault write pki/sign/cert-manager common_name="test.example.com" ttl="24h"

# Check cert-manager logs
oc logs -f deployment/cert-manager -n cert-manager

# Check Vault auth logs
vault read auth/kubernetes/role/cert-manager
```
Maintenance
1. Token Rotation
Create a script for token rotation:

```bash
#!/bin/bash
# rotate-vault-token.sh
oc delete secret cert-manager-vault-token -n cert-manager --ignore-not-found
oc create secret generic cert-manager-vault-token \
  -n cert-manager \
  --from-literal=token=$(oc create token cert-manager -n cert-manager --audience=vault --duration=8760h)
echo "Vault token rotated successfully"
```

---

# DNS Alternative
Using `/etc/hosts` is sufficient for testing and development, but for production OpenShift clusters, you'll need a more robust solution.

Using `/etc/hosts` (Development/Testing)
Yes, it's enough for testing - you can add the entry to /etc/hosts on each node:
```bash
# Add to /etc/hosts on all OpenShift nodes
192.168.252.223 vault.example.com
```
But there are limitations:
* Manual maintenance required on all nodes
* Not scalable
* Changes aren't persistent across node reboots/recreates
* Only works for the nodes where you've updated the hosts file

## Production Solutions
For production OpenShift clusters, use one of these methods:

1. OpenShift DNS Operator (Recommended)
Create a DNS entry in the cluster's DNS:
```yaml
apiVersion: config.openshift.io/v1
kind: DNS
metadata:
  name: cluster
spec:
  baseDomain: example.com
  privateZone:
    tags:
      Name: my-cluster-dns
```
2. Cluster DNS Configuration
Add a DNS entry to the cluster's CoreDNS/Custom DNS:
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: coredns-custom
  namespace: openshift-dns
data:
  vault.server: |
    hosts {
      192.168.252.223 vault.example.com
      fallthrough
    }
```
3. Service and Route/Ingress (Best Practice)
Create a Service and Route for Vault:
```yaml
apiVersion: v1
kind: Service
metadata:
  name: vault-service
  namespace: vault
spec:
  ports:
  - port: 8200
    targetPort: 8200
  selector:
    app: vault
---
apiVersion: route.openshift.io/v1
kind: Route
metadata:
  name: vault-route
  namespace: vault
spec:
  host: vault.example.com
  port:
    targetPort: 8200
  to:
    kind: Service
    name: vault-service
  tls:
    termination: passthrough
```
4. External DNS Service
Use an external DNS service like `Bind`, `AWS Route53`, or `CloudDNS`:

### Immediate Solution for Testing
For immediate testing, update `/etc/hosts` on your helper node and test:
```bash
# Add to /etc/hosts
echo "192.168.252.223 vault.example.com" | sudo tee -a /etc/hosts

# Test DNS resolution
nslookup vault.example.com
ping -c 1 vault.example.com

# Update your Vault configuration to use hostname
vault write pki/config/urls issuing_certificates="https://vault.example.com:8200/v1/pki/ca" crl_distribution_points="https://vault.example.com:8200/v1/pki/crl"
```

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

---

# ✅ Vault Certificate Expiration Check Script
```bash
nano check-vault-cert.sh
```
```sh
#!/bin/bash

CERT_PATH="/opt/vault/tls/tls.crt"
DAYS_LEFT_THRESHOLD=30

if [ ! -f "$CERT_PATH" ]; then
  echo "❌ Certificate file not found at $CERT_PATH"
  exit 1
fi

# Extract expiration date
EXPIRY_DATE=$(openssl x509 -in "$CERT_PATH" -noout -enddate | cut -d= -f2)
EXPIRY_EPOCH=$(date -d "$EXPIRY_DATE" +%s)
NOW_EPOCH=$(date +%s)

# Calculate the number of days remaining
DAYS_LEFT=$(( (EXPIRY_EPOCH - NOW_EPOCH) / 86400 ))

echo "✅ Certificate expires on: $EXPIRY_DATE"
echo "📆 Days left: $DAYS_LEFT"

if [ "$DAYS_LEFT" -le "$DAYS_LEFT_THRESHOLD" ]; then
  echo "⚠️ WARNING: Certificate expires in $DAYS_LEFT days!"

# Here you can set an automatic renewal order or send an email/Slack.

else
  echo "✅ Certificate is still valid for more than $DAYS_LEFT_THRESHOLD days."
fi
```
```bash
chmod +x check-vault-cert.sh
```
```bash
./check-vault-cert.sh
```
```bash
crontab -e
```
```bash
# Every day at 7:00 AM
0 7 * * * /path/to/check-vault-cert.sh >> /var/log/vault-cert-check.log 2>&1
```

---

# ✅ Complete auto-renewal script:
So if you want Vault to request a certificate for its own TLS from Vault (self-renew), it is recommended to create a special role like the following:
```bash
vault write pki/roles/vault-tls-role \
  allowed_domains="vault.infra.local" \
  allow_subdomains=true \
  allow_ip_sans=true \
  max_ttl="8760h"
```
## ✅ Initial setup commands
1. Create token file for secure use:
```bash
echo "<your_root_token>" > /root/.vault-token
chmod 600 /root/.vault-token
```
2. Install `jq`:
```bash
sudo yum install -y jq
```
3. Code:
```sh
#!/bin/bash

CERT_PATH="/opt/vault/tls/tls.crt"
KEY_PATH="/opt/vault/tls/tls.key"
CERT_DIR="/opt/vault/tls"
DAYS_LEFT_THRESHOLD=30
VAULT_ADDR="https://<cault-ip>:8200"
VAULT_ROLE="vault-tls-role"
COMMON_NAME="vault.infra.local"

# Enter root token or read from secure file
VAULT_TOKEN_FILE="/root/.vault-token"
if [ ! -f "$VAULT_TOKEN_FILE" ]; then
  echo "❌ Vault token not found at $VAULT_TOKEN_FILE"
  exit 1
fi
VAULT_TOKEN=$(cat "$VAULT_TOKEN_FILE")

# Check current certificate
if [ ! -f "$CERT_PATH" ]; then
  echo "❌ Certificate file not found at $CERT_PATH"
  exit 1
fi

EXPIRY_DATE=$(openssl x509 -in "$CERT_PATH" -noout -enddate | cut -d= -f2)
EXPIRY_EPOCH=$(date -d "$EXPIRY_DATE" +%s)
NOW_EPOCH=$(date +%s)
DAYS_LEFT=$(( (EXPIRY_EPOCH - NOW_EPOCH) / 86400 ))

echo "📆 Certificate expires on: $EXPIRY_DATE ($DAYS_LEFT days left)"

if [ "$DAYS_LEFT" -gt "$DAYS_LEFT_THRESHOLD" ]; then
  echo "✅ Certificate still valid. No renewal needed."
  exit 0
fi

echo "⚠️ Renewing certificate via Vault..."

# Request a new certificate from Vault
RESPONSE=$(curl -s --insecure \
  --header "X-Vault-Token: $VAULT_TOKEN" \
  --request POST \
  --data "{\"common_name\": \"$COMMON_NAME\", \"ttl\": \"8760h\"}" \
  "$VAULT_ADDR/v1/pki/issue/$VAULT_ROLE")

NEW_CERT=$(echo "$RESPONSE" | jq -r '.data.certificate')
NEW_KEY=$(echo "$RESPONSE" | jq -r '.data.private_key')

if [ -z "$NEW_CERT" ] || [ -z "$NEW_KEY" ]; then
  echo "❌ Failed to retrieve new certificate from Vault"
  exit 1
fi

# Backup the current certificate
cp "$CERT_PATH" "$CERT_PATH.bak"
cp "$KEY_PATH" "$KEY_PATH.bak"

# Certificate and key replacement
echo "$NEW_CERT" > "$CERT_PATH"
echo "$NEW_KEY" > "$KEY_PATH"
chmod 600 "$CERT_PATH" "$KEY_PATH"

echo "✅ New certificate installed."

# Restart Vault
systemctl restart vault
echo "🔁 Vault restarted."
```

---

### Note:
Create the cert-manager namespace
```bash
oc create ns cert-manager
```
Output: 
```text
namespace/cert-manager created
```
**Label the namespace to disable OpenShift’s default security policy**
**This allows cert-manager’s web hooks to run properly**:
```bash
oc label namespace cert-manager cert-manager.io/disable-validation=true
```
**Note**: Above step not required in case of other kubernetes environment. It is possible to store cert-manager using operatorHub with openShift

---
