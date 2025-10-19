# [Red Hat OpenShift GitOps](https://docs.redhat.com/en/documentation/red_hat_openshift_gitops/1.18)
# Install the Operator with console.
## Obtain the password for the Argo CD instance:
* Use the navigation panel to go to the Workloads `Secrets` page.
* Use the Project drop-down list and select the namespace where the Argo CD instance is created.
* Select the `<argo_CD_instance_name>-cluster` instance to display the password.
* On the Details tab, copy the password under Data `admin.password`.
* Use `admin` as the `Username` and the copied `password` as the `Password` to log in to the Argo CD UI in the new window.

---

# GitLab
## Create new repo and add the ssh key 
## Create a directory and push all your manifest file there.
Sample
```
└── git-repo/
    ├── k8s/
    │   ├── deployment.yaml
    │   ├── service.yaml
    │   ├── route.yaml
    │   ├── hpa.yaml
```

---

# Create namespace and label
```bash
oc label namespace <namespace-name> argocd.argoproj.io/managed-by=openshift-gitops
```

---

# In Argo CD UI:
## 1. Create Project
### **Settings → Projects → New Project**
edit the Project → DESTINATIONS → namespace

### 2. **Settings → Add Repository certificates and know hosts**
### 2.1. ADD SSH KNOWN HOSTS
```bash
# 2222 is the ssh port of my gitlab
ssh-keyscan -p 2222 gitlab.example.com > /tmp/gitlab_known_hosts
cat /tmp/gitlab_known_hosts
```
Copy and Paste the valuse of `/tmp/gitlab_known_hosts` 

### 2.2. ADD TLS CERTIFICATE
Download the `pem` tls file from url of your gitlab (`gitlab.example.com`).

### 3. Create ArgoCD Application:
**Settings → Repositories → Connect Repo**
**REPOSITORY** → `ssh://git@gitlab.example.com:2222/user/test.git`
**Private SSH Key** value is the that private key that you use in `install-config.yaml`
```bash
cat ~/.ssh/id_openshift
```
Sample
```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: mellat-test
  namespace: openshift-gitops
spec:
  project: mellat-test-proj # create AppProject in argoCD
  source:
    repoURL: 'ssh://git@gitlab.example.com:2222/user/test.git'
    targetRevision: main
    path: k8s
  destination:
    server: 'https://kubernetes.default.svc'
    namespace: namespace-name
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
      - CreateNamespace=true
      - PruneLast=true
      - Validate=true
```
### 4. Give access to **serviceaccount**
```bash
oc adm policy add-role-to-user edit \
  system:serviceaccount:openshift-gitops:openshift-gitops-argocd-application-controller \
  -n <namespace-name>
```

---

# Create the secret for image.
**Secrets → New Secrets → pull image**
**User the name of this secret in deployment `spec.imagePullSecrets`**
```yaml
      imagePullSecrets:
        - name: nexus
```
