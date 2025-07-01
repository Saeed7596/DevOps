# Cert-Manager

**Note1:Don't install these at the same time:**
```
cert-manager Operator for Red Hat OpenShift  ≠ community cert-manager Operator
```

**Note2: Install in only one namespace.**

---

# Cert-Manager in Disconnected Environments

This guide explains how to configure cert-manager in offline/disconnected environments where public certificate authorities (like Let's Encrypt) are unavailable.

## Why Doesn't Let's Encrypt Work in Disconnected Environments?
Requires internet access for ACME challenges (HTTP-01/DNS-01).

In offline environments, you must use private ACME servers instead.

So, Use internal Issuers (Private ACME, CA, Self-Signed, or Vault).

## Supported Issuer Types for Disconnected Environments

### 1. Private ACME Server
#### When to Use:
- When you need automatic certificate management using ACME protocol but can't access public ACME services

#### Implementation:
1. **Set up a private ACME server**:
   - Recommended solutions:
     - [Step CA](https://smallstep.com/docs/step-ca)
     - [Buypass Go SSL](https://www.buypass.com/ssl/products/acme)

2. **Configure ClusterIssuer**:
   ```yaml
   apiVersion: cert-manager.io/v1
   kind: ClusterIssuer
   metadata:
     name: internal-acme
   spec:
     acme:
       server: https://internal-acme.example.com  # Your internal ACME server
       email: admin@example.com
       privateKeySecretRef:
         name: internal-acme-key
       solvers:
       - http01:
           ingress:
             class: nginx
    ```

### 2. Internal Certificate Authority (CA)
When to Use:
* When you have an existing PKI infrastructure (e.g., OpenSSL, Microsoft AD CS)

#### Implementation:
1. **Generate CA certificate and key**:
    ```bash
    openssl req -x509 -newkey rsa:4096 -keyout ca.key -out ca.crt -days 365 -nodes -subj "/CN=My Internal CA"
    ```

2. **Create Kubernetes secret**:
    ```bash
    kubectl create secret tls ca-key-pair --cert=ca.crt --key=ca.key -n cert-manager
    ```

3. **Configure Issuer**:
    ```yaml
    apiVersion: cert-manager.io/v1
    kind: Issuer
    metadata:
    name: ca-issuer
    spec:
    ca:
        secretName: ca-key-pair
    ```

### 3. Self-Signed Certificates
When to Use:
* For testing or internal development environments

#### Implementation:
1. **Configure Self-Signed Issuer**:
    ```yaml
    apiVersion: cert-manager.io/v1
    kind: Issuer
    metadata:
    name: selfsigned-issuer
    spec:
    selfSigned: {}
    ```
2. **Request Certificate**:
    ```yaml
    apiVersion: cert-manager.io/v1
    kind: Certificate
    metadata:
    name: selfsigned-cert
    spec:
    secretName: selfsigned-cert-tls
    issuerRef:
        name: selfsigned-issuer
    dnsNames:
        - example.internal
    ```

### 4. HashiCorp Vault
When to Use:
* When you need enterprise-grade certificate management

#### Implementation:
1. **Set up Vault**:
* Follow Vault documentation

2. **Configure Vault Issuer**:
    ```yaml
    apiVersion: cert-manager.io/v1
    kind: Issuer
    metadata:
    name: vault-issuer
    spec:
    vault:
        server: https://vault.example.com
        path: pki/sign/example-dot-com
        auth:
        tokenSecretRef:
            name: vault-token
            key: token
    ```

---

## Why Public ACME (Let's Encrypt) Doesn't Work Offline
* Requires internet access for domain validation challenges (HTTP-01/DNS-01)
* Needs connectivity to public ACME API endpoints
* Solution: Use private ACME servers instead

### Summary Table
| Issuer Type |	Primary Use Case |	Requirements |
|-------------|------------------|---------------|
|Private ACME |	Let's Encrypt alternative   | Internal ACME server |
|Internal CA  |	Organizational certificates | Existing PKI infrastructure |
|Self-Signed  |	Testing/Development | No special requirements |
|Vault        | Enterprise security | HashiCorp Vault installation |

**Note: Never install both Red Hat's cert-manager Operator and community cert-manager Operator in the same cluster.**
