# [Cert-Manager](cert-manager.io) 
# [cert-manager Operator for Red Hat OpenShift](https://docs.redhat.com/en/documentation/openshift_container_platform/4.18/html/security_and_compliance/cert-manager-operator-for-red-hat-openshift)
**Note1:Don't install these at the same time:**
```
cert-manager Operator for Red Hat OpenShift  ≠ community cert-manager Operator
```

**Note2: Install in only one namespace.**

---

# Install Verification
## Procedure
```text
1. Log in to the OpenShift Container Platform web console.
2. Navigate to Operators  OperatorHub.
3. Enter cert-manager Operator for Red Hat OpenShift into the filter box.
4. Select the cert-manager Operator for Red Hat OpenShift
5. Select the cert-manager Operator for Red Hat OpenShift version from Version drop-down list, and click Install.
6. On the Install Operator page:
   i.Update the Update channel, if necessary. The channel defaults to stable-v1, which installs the latest stable release of the cert-manager Operator for Red Hat      OpenShift.
   ii. Choose the Installed Namespace for the Operator. The default Operator namespace is cert-manager-operator.
   If the cert-manager-operator namespace does not exist, it is created for you.
   iii. Select an Update approval strategy.
        * The Automatic strategy allows Operator Lifecycle Manager (OLM) to automatically update the Operator when a new version is available.
        * The Manual strategy requires a user with appropriate credentials to approve the Operator update.
7. choose the AllNamespaces installation mode
8. Click Install.
```
Verify 
1. Navigate to **Operators** -> **Installed Operators**.
2. Verify that **cert-manager Operator for Red Hat OpenShift** is listed with a **Status** of **Succeeded** in the `cert-manager-operator` namespace.
3. Verify that cert-manager pods are up and running by entering the following command:
```bash
oc get pods -n cert-manager
```
Example output
```text
NAME                                       READY   STATUS    RESTARTS   AGE
cert-manager-bd7fbb9fc-wvbbt               1/1     Running   0          3m39s
cert-manager-cainjector-56cc5f9868-7g9z7   1/1     Running   0          4m5s
cert-manager-webhook-d4f79d7f7-9dg9w       1/1     Running   0          4m9s
```

---

# Custom CA

##  1. Deleting a TLS secret automatically upon Certificate removal 
You can enable the --enable-certificate-owner-ref flag for the cert-manager Operator for Red Hat OpenShift by adding a spec.controllerConfig section in the CertManager resource. The --enable-certificate-owner-ref flag sets the certificate resource as an owner of the secret where the TLS certificate is stored.

### 1.1 Check that the `Certificate` object and its secret are available by running
```bash
oc get certificate
```
Example output:
```text
NAME                                             READY   SECRET                                           AGE
certificate-from-clusterissuer-route53-ambient   True    certificate-from-clusterissuer-route53-ambient   8h
```
### 1.2 Edit the `CertManager` resource
```bash
oc edit certmanager cluster
```
### 1.3 Add a spec.controllerConfig section with the following override arguments:
```yaml
apiVersion: operator.openshift.io/v1alpha1
kind: CertManager
metadata:
  name: cluster
# ...
spec:
# ...
  controllerConfig:
    overrideArgs:
      - '--enable-certificate-owner-ref'
```
### 1.4 Save your changes and quit the text editor to apply your changes.
### 1.5 Verification
```bash
oc get pods -l app.kubernetes.io/name=cert-manager -n cert-manager -o yaml
```
Example output
```yaml
# ...
  metadata:
    name: cert-manager-6e4b4d7d97-zmdnb
    namespace: cert-manager
# ...
  spec:
    containers:
    - args:
      - --enable-certificate-owner-ref
```

---

## 2. Overriding CPU and memory limits for the cert-manager components 
After installing the cert-manager Operator for Red Hat OpenShift, you can configure the CPU and memory limits from the cert-manager Operator for Red Hat OpenShift API for the cert-manager components such as cert-manager controller, CA injector, and Webhook.

### 2.1 Check that the deployments of the cert-manager controller, CA injector, and Webhook are available by entering the following command:
```bash
oc get deployment -n cert-manager
```
Example output
```text
NAME                      READY   UP-TO-DATE   AVAILABLE   AGE
cert-manager              1/1     1            1           53m
cert-manager-cainjector   1/1     1            1           53m
cert-manager-webhook      1/1     1            1           53m
```
```bash
oc get deployment -n cert-manager -o yaml
```
The `spec.resources` field is empty by default. The cert-manager components do not have CPU and memory limits.
```yaml
          resources: {}
```

### 2.2 To configure the CPU and memory limits for the cert-manager controller, CA injector, and Webhook, enter the following command:
```bash
$ oc patch certmanager.operator cluster --type=merge -p="
spec:
  controllerConfig:
    overrideResources:
      limits: 
        cpu: 200m 
        memory: 64Mi 
      requests: 
        cpu: 10m 
        memory: 16Mi 
  webhookConfig:
    overrideResources:
      limits: 
        cpu: 200m 
        memory: 64Mi 
      requests: 
        cpu: 10m 
        memory: 16Mi 
  cainjectorConfig:
    overrideResources:
      limits: 
        cpu: 200m 
        memory: 64Mi 
      requests: 
        cpu: 10m 
        memory: 16Mi 
"
```
Example output
```bash
certmanager.operator.openshift.io/cluster patched
```

### 2.3 Verification
```bash
oc get deployment -n cert-manager -o yaml
```

---

## 3. Configuring scheduling overrides for cert-manager components 
You can configure the pod scheduling from the cert-manager Operator for Red Hat OpenShift API for the cert-manager Operator for Red Hat OpenShift components such as cert-manager controller, CA injector, and Webhook.

### 3.1 Procedure
Update the `certmanager.operator` custom resource to configure pod scheduling overrides for the desired components by running the following command. Use the `overrideScheduling` field under the `controllerConfig`, `webhookConfig`, or `cainjectorConfig` sections to define `nodeSelector` and `tolerations` settings.
```bash
oc patch certmanager.operator cluster --type=merge -p="
spec:
  controllerConfig:
    overrideScheduling:
      nodeSelector:
        node-role.kubernetes.io/control-plane: ''  1 
      tolerations:
        - key: node-role.kubernetes.io/master
          operator: Exists
          effect: NoSchedule  2 
  webhookConfig:
    overrideScheduling:
      nodeSelector:
        node-role.kubernetes.io/control-plane: ''  3 
      tolerations:
        - key: node-role.kubernetes.io/master
          operator: Exists
          effect: NoSchedule  4 
  cainjectorConfig:
    overrideScheduling:
      nodeSelector:
        node-role.kubernetes.io/control-plane: ''  5 
      tolerations:
        - key: node-role.kubernetes.io/master
          operator: Exists
          effect: NoSchedule"  6
```
```text
1 Defines the nodeSelector for the cert-manager controller deployment.
2 Defines the tolerations for the cert-manager controller deployment.
3 Defines the nodeSelector for the cert-manager webhook deployment.
4 Defines the tolerations for the cert-manager webhook deployment.
5 Defines the nodeSelector for the cert-manager cainjector deployment.
6 Defines the tolerations for the cert-manager cainjector deployment.
```

### 3.2 Verification
Check the deployments in the `cert-manager` namespace to confirm they have the correct `nodeSelector` and `tolerations` by running the following command:
```bash
oc get pods -n cert-manager -o wide
```
Example output
```text
NAME                                       READY   STATUS    RESTARTS   AGE   IP            NODE                         NOMINATED NODE   READINESS GATES
cert-manager-58d9c69db4-78mzp              1/1     Running   0          10m   10.129.0.36   ip-10-0-1-106.ec2.internal   <none>           <none>
cert-manager-cainjector-85b6987c66-rhzf7   1/1     Running   0          11m   10.128.0.39   ip-10-0-1-136.ec2.internal   <none>           <none>
cert-manager-webhook-7f54b4b858-29bsp      1/1     Running   0          11m   10.129.0.35   ip-10-0-1-106.ec2.internal   <none>           <none>
```
Check the nodeSelector and tolerations settings applied to deployments by running the following command:
```bash
oc get deployments -n cert-manager -o jsonpath='{range .items[*]}{.metadata.name}{"\n"}{.spec.template.spec.nodeSelector}{"\n"}{.spec.template.spec.tolerations}{"\n\n"}{end}'
```
Example output
```text
cert-manager
{"kubernetes.io/os":"linux","node-role.kubernetes.io/control-plane":""}
[{"effect":"NoSchedule","key":"node-role.kubernetes.io/master","operator":"Exists"}]

cert-manager-cainjector
{"kubernetes.io/os":"linux","node-role.kubernetes.io/control-plane":""}
[{"effect":"NoSchedule","key":"node-role.kubernetes.io/master","operator":"Exists"}]

cert-manager-webhook
{"kubernetes.io/os":"linux","node-role.kubernetes.io/control-plane":""}
[{"effect":"NoSchedule","key":"node-role.kubernetes.io/master","operator":"Exists"}]
```
Verify pod scheduling events in the cert-manager namespace by running the following command:
```bash
oc get events -n cert-manager --field-selector reason=Scheduled
```

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
     - [Step CA](https://smallstep.com/docs/step-ca) - [GitHub](https://github.com/smallstep/certificates)
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

---

# 🛠 Command to check the expiration of important certificates:
```bash
oc get csr
oc get certificatesigningrequests
oc get secret -n openshift-config
oc get secret -n openshift-ingress
oc get certificate -A
oc describe certificate -A
```
```bash
oc get secrets -n openshift-config-managed -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.data.tls\.crt}{"\n"}{end}' | while read name crt; do
  echo "$crt" | base64 -d | openssl x509 -noout -subject -enddate -issuer && echo "---"
done
```

---

✅ 🔐 Script to check the expiration date of OpenShift root CAs
```bash
nano check-ca-expiry.sh
```
```bash
#!/bin/bash

# Required tool: openssl, base64, oc

echo "🔍 Checking expiration dates of main CA certificates in your OpenShift cluster..."
echo "------------------------------------------------------------"

# Array of important secrets/configs that usually contain CA certs
CA_LOCATIONS=(
  "openshift-service-ca/service-ca"
  "openshift-ingress-operator/router-ca"
  "openshift-authentication/oauth-serving-cert"
  "openshift-kube-apiserver/kube-apiserver-client-ca"
  "openshift-kube-controller-manager/service-network-serving-cert-signer"
  "openshift-config/user-ca-bundle"
)

for item in "${CA_LOCATIONS[@]}"; do
  ns=$(echo "$item" | cut -d'/' -f1)
  name=$(echo "$item" | cut -d'/' -f2)

  echo -e "\n🔹 Inspecting: $ns/$name"

  # Try as secret first
  cert_data=$(oc get secret -n "$ns" "$name" -o jsonpath='{.data.ca\.crt}' 2>/dev/null)

  # Fallback: Try configmap
  if [ -z "$cert_data" ]; then
    cert_data=$(oc get configmap -n "$ns" "$name" -o jsonpath='{.data.ca\.crt}' 2>/dev/null)
  fi

  if [ -z "$cert_data" ]; then
    echo "  ❌ Certificate not found or doesn't contain ca.crt"
    continue
  fi

  # Decode and parse with openssl
  echo "$cert_data" | base64 -d | openssl x509 -noout -subject -issuer -enddate
done

echo -e "\n✅ Done. Review any expiration dates approaching soon."
```
```bash
chmod +x check-ca-expiry.sh
```
```bash
./check-ca-expiry.sh
```
