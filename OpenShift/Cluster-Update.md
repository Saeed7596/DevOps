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

## 🚀 OpenShift Cluster Update Steps
## ✅ Prerequisites
1. Take a full etcd backup

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
