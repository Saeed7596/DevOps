# Kubernetes User RBAC Automation Script

This document explains how the `rbac.py` script works step-by-step. It helps you to easily create a Kubernetes RBAC user, along with all required resources.

---

## 📅 What This Script Does

This script automatically:

1. **Generates a private key and CSR** (Certificate Signing Request) for the new user.
2. **Signs the CSR with Kubernetes CA** to issue a user certificate.
3. **Creates a Secret** to store the certificate and key in Kubernetes.
4. **Creates a Role** that grants permissions (CRUD access to Pods, Services, and ConfigMaps).
5. **Creates a RoleBinding** that binds the Role to the user.
6. **Generates a custom kubeconfig** for the user to access the cluster securely.

All these resources are saved in a **dedicated folder** named after the user.

---

## 🔧 Steps Explained

### 1. Load Kubernetes Cluster Info
- Load your current context and cluster server address from your default kubeconfig (`~/.kube/config`).
- Read the Kubernetes CA certificate (`/etc/kubernetes/pki/ca.crt`).

### 2. Get User Details
- Ask for a **username** and a **namespace**.
- Create a directory named after the user (e.g., `./saeed/`).

### 3. Generate User Key and CSR
- Use OpenSSL to:
  - Create a 2048-bit private key.
  - Create a CSR where:
    - `CN = username`
    - `O = namespace`

### 4. Sign the Certificate
- Sign the CSR with the Kubernetes CA key (`/etc/kubernetes/pki/ca.key`) to issue a user certificate valid for 1 year (365 days).

### 5. Create Kubernetes Secret
- Create a Kubernetes Secret (`kubernetes.io/tls`) containing the signed certificate and private key.
- Apply the Secret using `kubectl apply -f`.

### 6. Create Role
- Create a Role that allows the user to:
  - `get`, `watch`, `list`, `create`, `update`, and `delete` Pods, Services, and ConfigMaps within the specified namespace.
- Apply the Role using `kubectl apply -f`.

### 7. Create RoleBinding
- Create a RoleBinding to bind the new Role to the user.
- Apply the RoleBinding using `kubectl apply -f`.

### 8. Generate User-Specific Kubeconfig
- Create a lightweight kubeconfig containing only:
  - The cluster info.
  - The user credentials (certificate and private key).
  - The namespace as default context.

### 9. Outputs
- All files (`*.key`, `*.crt`, YAMLs, kubeconfig) are saved inside `./username/`.
- After each `kubectl apply`, the output is printed to the terminal.

---

## 📁 Folder and File Structure Example

```
./saeed/
    saeed-key.pem
    saeed.csr
    saeed.crt
    saeed-secret.yaml
    saeed-role.yaml
    saeed-rolebinding.yaml
    saeed-kubeconfig.yaml
```

---

## ⚡ Possible Future Improvements

- Auto-create namespace if it does not exist.
- Check if resources already exist and update them instead of failing.
- Add optional arguments to make the script fully non-interactive.
- Support additional resource types and custom Role rules.

---

## 📍 Prerequisites

- Python 3.x
- `kubectl` installed and configured.
- Access to Kubernetes CA files (`ca.crt` and `ca.key`).
- `openssl` installed.

---

## 📢 Notes

- This script assumes a **standard kubeadm** installation for Kubernetes.
- For production-grade use, consider certificate expiration and renewal strategies.

---

## 🔔 Quick Reminder

Always verify user permissions carefully to avoid security issues in your Kubernetes cluster!

---

# Differences to Apply When Using OpenShift CRC

| Aspect                   | Kubernetes (vanilla)                     | OpenShift CRC                                |
|--------------------------|----------------------------------------|---------------------------------------------|
| User Creation            | Create X.509 certs and manage keys     | Prefer using ServiceAccounts or set up local users with htpasswd |
| CA Certificate Location  | `/etc/kubernetes/pki/ca.crt`            | Use OpenShift CA or fetch from cluster config |
| CA Key Access            | Required for signing user certs         | Usually not accessible or recommended       |
| Authentication Setup     | Based on client certificates             | Uses OAuth with providers (htpasswd, LDAP, etc.) |
| User Management          | Create and bind Roles/RoleBindings       | Same, but often use ServiceAccounts or OpenShift users |
| kubeconfig Generation    | Embed client certs and keys              | Can embed tokens from OAuth or ServiceAccounts |
| Login Command            | `kubectl` with client cert                | `oc login` with token or username/password  |
| Namespace Defaulting     | Specified in Role/RoleBinding             | Same                                         |

---

# Happy Automating! 🌟

