# Rook-Ceph on OpenShift 4.18 — Complete Deployment Guide
### Air-Gapped | Bare Metal | Agent-Based | OpenShift Virtualization Ready

---

> **Environment Summary**
>
> | Item | Value |
> |---|---|
> | OpenShift Version | 4.18.30 |
> | Installation Method | Agent-Based Installer |
> | Network | Air-Gapped |
> | Infrastructure | Bare Metal (HP ProLiant G10) |
> | Rook Version | v1.16.6 |
> | Ceph Version | v19.2.x (Squid) |
> | Use Case | OpenShift Virtualization |

---

## Table of Contents

1. [Cluster Nodes](#1-cluster-nodes)
2. [Storage Requirements for OCP Virtualization](#2-storage-requirements-for-ocp-virtualization)
3. [Required Images for Air-Gap](#3-required-images-for-air-gap)
4. [Pre-Deployment Checklist](#4-pre-deployment-checklist)
5. [Manifest File Locations on GitHub](#5-manifest-file-locations-on-github)
6. [Step-by-Step Deployment](#6-step-by-step-deployment)
   - [Step 1 — Wipe Disks](#step-1--wipe-disks-if-needed)
   - [Step 2 — Label Nodes](#step-2--label-nodes)
   - [Step 3 — Apply CRDs and Common](#step-3--apply-crds-and-common)
   - [Step 4 — Apply CSI Operator](#step-4--apply-csi-operator)
   - [Step 5 — Apply Operator (OpenShift)](#step-5--apply-operator-openshift-specific)
   - [Step 6 — Apply CephCluster](#step-6--apply-cephcluster)
   - [Step 7 — Deploy Toolbox and Verify](#step-7--deploy-toolbox-and-verify)
   - [Step 8 — Create StorageClass](#step-8--create-storageclass)
   - [Step 9 — Configure StorageProfile](#step-9--configure-storageprofile-for-ocp-virt)
7. [Manifest Reference](#7-manifest-reference)
   - [cluster.yaml](#clusteryaml)
   - [StorageClass RBD](#storageclass-rbd)
8. [Verification](#8-verification)
9. [Troubleshooting](#9-troubleshooting)

---

## 1. Cluster Nodes

| Hostname | Role | IP | OSD Disk |
|---|---|---|---|
| master-1.ocp-bm.example.com | control-plane, master, worker | 172.29.97.194 | nvme9n1 |
| master-2.ocp-bm.example.com | control-plane, master, worker | 172.29.97.195 | nvme9n1 |
| master-3.ocp-bm.example.com | control-plane, master, worker | 172.29.97.196 | nvme9n1 |
| worker-1.ocp-bm.example.com | worker | 172.29.97.197 | nvme9n1 |
| worker-2.ocp-bm.example.com | worker | 172.29.97.198 | nvme9n1 |

> **Note:** worker-2 had existing partitions (`nvme9n1p1`, `nvme9n1p2`) that must be wiped before use.

---

## 2. Storage Requirements for OCP Virtualization

According to the OpenShift Virtualization documentation, the recommended storage configuration for VM disks is:

| Parameter | Recommended Value | Reason |
|---|---|---|
| **Access Mode** | `ReadWriteMany (RWX)` | Required for live migration |
| **Volume Mode** | `Block` | Better performance — no filesystem layer overhead |
| **Protocol** | Ceph RBD | Preferable over CephFS for VM disks |

### Why Only One StorageClass is Needed

Ceph RBD supports **RWX + Block mode** natively since OCP 4.12+. This means:

- `rook-ceph-block` (RBD) can serve **both** RWO and RWX
- CephFS StorageClass is **not required** for OCP Virtualization
- RBD Block mode has **significantly better performance** than CephFS Filesystem mode

```
VM disk I/O path comparison:

CephFS:  App → Filesystem layer → disk image file → CephFS → Ceph
RBD:     App → Block device → Ceph RBD   ← fewer layers, lower latency
```

---

## 3. Required Images for Air-Gap

Pull these images on an internet-connected machine, retag, and push to your mirror registry.

### Image List

| Image | Source Registry | Purpose |
|---|---|---|
| `rook/ceph:v1.16.6` | docker.io | Rook Operator |
| `ceph/ceph:v19.2.x` | quay.io | All Ceph daemons + Toolbox |
| `cephcsi/cephcsi:v3.16.2` | quay.io | Ceph CSI driver |
| `sig-storage/csi-node-driver-registrar:v2.16.0` | registry.k8s.io | Node CSI registrar |
| `sig-storage/csi-provisioner:v6.1.1` | registry.k8s.io | Dynamic PV provisioner |
| `sig-storage/csi-attacher:v4.11.0` | registry.k8s.io | Volume attach/detach |
| `sig-storage/csi-resizer:v2.1.0` | registry.k8s.io | Volume resize |
| `sig-storage/csi-snapshotter:v8.5.0` | registry.k8s.io | Volume snapshots |
| `csiaddons/k8s-sidecar:v0.11.0` | quay.io | CSI Addons sidecar |

### Mirror Script

```bash
#!/bin/bash
MIRROR="your-mirror-registry:5000"
ROOK_VER="v1.16.6"
CEPH_VER="v19.2.1"

IMAGES=(
  "docker.io/rook/ceph:${ROOK_VER}"
  "quay.io/ceph/ceph:${CEPH_VER}"
  "quay.io/cephcsi/cephcsi:v3.16.2"
  "registry.k8s.io/sig-storage/csi-node-driver-registrar:v2.16.0"
  "registry.k8s.io/sig-storage/csi-provisioner:v6.1.1"
  "registry.k8s.io/sig-storage/csi-attacher:v4.11.0"
  "registry.k8s.io/sig-storage/csi-resizer:v2.1.0"
  "registry.k8s.io/sig-storage/csi-snapshotter:v8.5.0"
  "quay.io/csiaddons/k8s-sidecar:v0.11.0"
)

for IMAGE in "${IMAGES[@]}"; do
  echo "Pulling $IMAGE ..."
  podman pull $IMAGE
  SHORT=$(echo $IMAGE | sed 's|docker.io/||;s|quay.io/||;s|registry.k8s.io/||')
  podman tag $IMAGE ${MIRROR}/${SHORT}
  podman push ${MIRROR}/${SHORT}
done
```

---

## 4. Pre-Deployment Checklist

```
[ ] All nodes are healthy:         oc get nodes
[ ] CephCluster health OK:         oc get cephcluster -n rook-ceph
[ ] nvme9n1 is raw on all nodes:   lsblk -f (no FSTYPE column)
[ ] worker-2 disk is wiped:        wipefs + sgdisk --zap-all
[ ] Mirror registry is reachable from all nodes
[ ] All 9 images are pushed to mirror registry
[ ] cluster-admin access:          oc whoami
```

---

## 5. Manifest File Locations on GitHub

Base tag: `https://github.com/rook/rook/blob/v1.16.6/deploy/examples/`

| File | Path in Repository |
|---|---|
| `crds.yaml` | `deploy/examples/crds.yaml` |
| `common.yaml` | `deploy/examples/common.yaml` |
| `csi-operator.yaml` | `deploy/examples/csi-operator.yaml` |
| `operator-openshift.yaml` | `deploy/examples/operator-openshift.yaml` |
| `cluster.yaml` | `deploy/examples/cluster.yaml` |
| `toolbox.yaml` | `deploy/examples/toolbox.yaml` |
| `filesystem.yaml` | `deploy/examples/filesystem.yaml` |
| `storageclass-rbd.yaml` | `deploy/examples/csi/rbd/storageclass.yaml` |
| `storageclass-cephfs.yaml` | `deploy/examples/csi/cephfs/storageclass.yaml` |

### Download All at Once

```bash
BASE="https://raw.githubusercontent.com/rook/rook/v1.16.6/deploy/examples"

wget ${BASE}/crds.yaml
wget ${BASE}/common.yaml
wget ${BASE}/csi-operator.yaml
wget ${BASE}/operator-openshift.yaml
wget ${BASE}/cluster.yaml
wget ${BASE}/toolbox.yaml
wget ${BASE}/filesystem.yaml
wget ${BASE}/csi/rbd/storageclass.yaml      -O storageclass-rbd.yaml
wget ${BASE}/csi/cephfs/storageclass.yaml   -O storageclass-cephfs.yaml
```

---

## 6. Step-by-Step Deployment

### Step 1 — Wipe Disks (If Needed)

> Required for **worker-2** which had existing partitions.

```bash
# Open a debug shell on the node
oc debug node/worker-2.ocp-bm.example.com

# Inside debug shell
chroot /host

# Wipe all signatures and partition table
wipefs -a /dev/nvme9n1
sgdisk --zap-all /dev/nvme9n1

# Verify clean (no FSTYPE, no partitions listed)
lsblk -f /dev/nvme9n1

exit && exit
```

---

### Step 2 — Label Nodes

The `cluster.yaml` uses `role=storage-node` as the node selector.

```bash
oc label node master-1.ocp-bm.example.com role=storage-node
oc label node master-2.ocp-bm.example.com role=storage-node
oc label node master-3.ocp-bm.example.com role=storage-node
oc label node worker-1.ocp-bm.example.com role=storage-node
oc label node worker-2.ocp-bm.example.com role=storage-node

# Verify — all 5 nodes must appear
oc get nodes -l role=storage-node
```

---

### Step 3 — Apply CRDs and Common

```bash
oc create -f crds.yaml
oc create -f common.yaml

# Verify namespace
oc get ns rook-ceph

# Verify CRDs (~25 expected)
oc get crd | grep ceph.rook.io | wc -l
```

---

### Step 4 — Apply CSI Operator

> **Critical for Rook v1.15+** — this was not mentioned on the OpenShift-specific page but is mandatory.
> Without this file, the cluster will fail with:
> `no matches for kind "CephConnection" in version "csi.ceph.io/v1"`

```bash
oc create -f csi-operator.yaml

# Verify CSI CRDs are now registered
oc get crd | grep csi.ceph.io
# Expected:
# cephconnections.csi.ceph.io
# operatorconfigs.csi.ceph.io
```

---

### Step 5 — Apply Operator (OpenShift-Specific)

> Use `operator-openshift.yaml` — **NOT** `operator.yaml`.
> The OpenShift version includes Security Context Constraints (SCC) required by RHCOS/SELinux.

Edit `operator-openshift.yaml` before applying:

```yaml
# 1. Change operator image
image: your-mirror-registry:5000/rook/ceph:v1.16.6

# 2. Ensure this is set (already in operator-openshift.yaml)
- name: ROOK_HOSTPATH_REQUIRES_PRIVILEGED
  value: "true"

# 3. Uncomment and set all CSI images (required for air-gap)
- name: ROOK_CSI_CEPH_IMAGE
  value: "your-mirror-registry:5000/cephcsi/cephcsi:v3.16.2"
- name: ROOK_CSI_REGISTRAR_IMAGE
  value: "your-mirror-registry:5000/sig-storage/csi-node-driver-registrar:v2.16.0"
- name: ROOK_CSI_RESIZER_IMAGE
  value: "your-mirror-registry:5000/sig-storage/csi-resizer:v2.1.0"
- name: ROOK_CSI_PROVISIONER_IMAGE
  value: "your-mirror-registry:5000/sig-storage/csi-provisioner:v6.1.1"
- name: ROOK_CSI_SNAPSHOTTER_IMAGE
  value: "your-mirror-registry:5000/sig-storage/csi-snapshotter:v8.5.0"
- name: ROOK_CSI_ATTACHER_IMAGE
  value: "your-mirror-registry:5000/sig-storage/csi-attacher:v4.11.0"
- name: ROOK_CSIADDONS_IMAGE
  value: "your-mirror-registry:5000/csiaddons/k8s-sidecar:v0.11.0"
```

```bash
oc create -f operator-openshift.yaml

# Wait for operator pod to be Running
oc get pods -n rook-ceph -w
# rook-ceph-operator-xxx   1/1   Running ✅
```

---

### Step 6 — Apply CephCluster

> See [Section 7](#7-manifest-reference) for the complete `cluster.yaml` tailored for this environment.

```bash
oc create -f cluster.yaml

# Monitor deployment (takes 5–10 minutes)
watch -n3 "oc get pods -n rook-ceph"

# Check CephCluster status
oc get cephcluster -n rook-ceph
```

Expected final state:

```
NAME        DATADIRHOSTPATH   MONCOUNT   PHASE   MESSAGE           HEALTH
rook-ceph   /var/lib/rook     3          Ready   Cluster created   HEALTH_OK
```

Expected running pods:

```
rook-ceph-operator-xxx                 1/1   Running   ← operator
rook-ceph-mon-a                        2/2   Running   ← monitors x3
rook-ceph-mon-b                        2/2   Running
rook-ceph-mon-c                        2/2   Running
rook-ceph-mgr-a                        3/3   Running   ← managers x2
rook-ceph-mgr-b                        3/3   Running
rook-ceph-osd-0                        2/2   Running   ← one OSD per node
rook-ceph-osd-1                        2/2   Running
rook-ceph-osd-2                        2/2   Running
rook-ceph-osd-3                        2/2   Running
rook-ceph-osd-4                        2/2   Running
csi-rbdplugin-provisioner-xxx          6/6   Running
csi-rbdplugin-xxx (DaemonSet)          2/2   Running   ← one per node
```

---

### Step 7 — Deploy Toolbox and Verify

```bash
# Edit toolbox.yaml: change image to your mirror
# image: your-mirror-registry:5000/ceph/ceph:v19.2.1

oc create -f toolbox.yaml

# Wait for toolbox
oc wait pod -n rook-ceph -l app=rook-ceph-tools \
  --for condition=Ready --timeout=120s

# Enter toolbox
oc -n rook-ceph exec -it deploy/rook-ceph-tools -- bash
```

Inside toolbox:

```bash
# Must show HEALTH_OK
ceph status

# Must show 5 OSDs: 5 up, 5 in
ceph osd tree

# Check available capacity
ceph df

exit
```

Expected `ceph status` output:

```
cluster:
  health: HEALTH_OK

services:
  mon: 3 daemons, quorum a,b,c
  mgr: a(active), b(standby)
  osd: 5 osds: 5 up, 5 in
```

---

### Step 8 — Create StorageClass

> Only **one StorageClass** is needed for OCP Virtualization.
> Ceph RBD with RWX + Block mode covers all VM workload requirements.
> CephFS StorageClass is **not required**.

```bash
# Apply CephBlockPool + StorageClass
oc apply -f storageclass-rbd.yaml

# Verify
oc get cephblockpool -n rook-ceph
oc get storageclass
```

Expected:

```
NAME              PROVISIONER                      DEFAULT
rook-ceph-block   rook-ceph.rbd.csi.ceph.com       true ✅
```

---

### Step 9 — Configure StorageProfile for OCP-Virt

OCP Virtualization reads the `StorageProfile` object to know which access and volume modes to use automatically when creating VM disks.

```bash
# Check current profile
oc get storageprofile rook-ceph-block -o yaml
```

Patch it to enable RWX + Block mode:

```bash
oc patch storageprofile rook-ceph-block \
  --type=merge \
  -p '{
    "spec": {
      "claimPropertySets": [
        {
          "accessModes": ["ReadWriteMany"],
          "volumeMode": "Block"
        },
        {
          "accessModes": ["ReadWriteOnce"],
          "volumeMode": "Block"
        }
      ]
    }
  }'
```

Verify:

```bash
oc get storageprofile rook-ceph-block \
  -o jsonpath='{.status.claimPropertySets}' | jq .
```

Expected output:

```json
[
  { "accessModes": ["ReadWriteMany"], "volumeMode": "Block" },
  { "accessModes": ["ReadWriteOnce"],  "volumeMode": "Block" }
]
```

---

## 7. Manifest Reference

### cluster.yaml

Complete `cluster.yaml` configured for this 5-node environment:

```yaml
apiVersion: ceph.rook.io/v1
kind: CephCluster
metadata:
  name: rook-ceph
  namespace: rook-ceph
spec:
  cephVersion:
    image: your-mirror-registry:5000/ceph/ceph:v19.2.1
    allowUnsupported: false

  dataDirHostPath: /var/lib/rook

  mon:
    count: 3
    allowMultiplePerNode: false

  mgr:
    count: 2
    allowMultiplePerNode: false
    modules:
      - name: pg_autoscaler
        enabled: true

  dashboard:
    enabled: true
    ssl: true

  crashCollector:
    disable: false

  logCollector:
    enabled: true
    periodicity: daily
    maxLogSize: 500M

  storage:
    useAllNodes: false
    useAllDevices: false
    nodes:
      - name: "master-1.ocp-bm.example.com"
        devices:
          - name: "nvme9n1"
      - name: "master-2.ocp-bm.example.com"
        devices:
          - name: "nvme9n1"
      - name: "master-3.ocp-bm.example.com"
        devices:
          - name: "nvme9n1"
      - name: "worker-1.ocp-bm.example.com"
        devices:
          - name: "nvme9n1"
      - name: "worker-2.ocp-bm.example.com"
        devices:
          - name: "nvme9n1"

  placement:
    all:
      nodeAffinity:
        requiredDuringSchedulingIgnoredDuringExecution:
          nodeSelectorTerms:
            - matchExpressions:
                - key: role
                  operator: In
                  values:
                    - storage-node

  resources:
    mgr:
      limits:
        cpu: "1"
        memory: "1Gi"
      requests:
        cpu: "500m"
        memory: "512Mi"
    mon:
      limits:
        cpu: "1"
        memory: "2Gi"
      requests:
        cpu: "500m"
        memory: "1Gi"
    osd:
      limits:
        cpu: "2"
        memory: "4Gi"
      requests:
        cpu: "1"
        memory: "2Gi"
    prepareosd:
      limits:
        cpu: "500m"
        memory: "400Mi"
      requests:
        cpu: "200m"
        memory: "200Mi"

  disruptionManagement:
    managePodBudgets: true
    osdMaintenanceTimeout: 30
    pgHealthCheckTimeout: 0

  healthCheck:
    daemonHealth:
      mon:
        disabled: false
        interval: 45s
      osd:
        disabled: false
        interval: 60s
      status:
        disabled: false
        interval: 60s
```

---

### StorageClass RBD

Complete `storageclass-rbd.yaml` optimized for OCP Virtualization:

```yaml
apiVersion: ceph.rook.io/v1
kind: CephBlockPool
metadata:
  name: replicapool
  namespace: rook-ceph
spec:
  failureDomain: host
  replicated:
    size: 3
    requireSafeReplicaSize: true
---
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: rook-ceph-block
  annotations:
    storageclass.kubernetes.io/is-default-class: "true"
provisioner: rook-ceph.rbd.csi.ceph.com
parameters:
  clusterID: rook-ceph
  pool: replicapool
  imageFormat: "2"
  imageFeatures: layering
  mapOptions: "lock_on_read,queue_depth=1024"
  csi.storage.k8s.io/provisioner-secret-name: rook-csi-rbd-provisioner
  csi.storage.k8s.io/provisioner-secret-namespace: rook-ceph
  csi.storage.k8s.io/controller-expand-secret-name: rook-csi-rbd-provisioner
  csi.storage.k8s.io/controller-expand-secret-namespace: rook-ceph
  csi.storage.k8s.io/node-stage-secret-name: rook-csi-rbd-node
  csi.storage.k8s.io/node-stage-secret-namespace: rook-ceph
  csi.storage.k8s.io/fstype: ext4
reclaimPolicy: Delete
allowVolumeExpansion: true
volumeBindingMode: Immediate
```

---

## 8. Verification

### Full Deployment Verification

```bash
# 1. All nodes ready
oc get nodes

# 2. All rook-ceph pods running
oc get pods -n rook-ceph | grep -v Completed

# 3. CephCluster HEALTH_OK
oc get cephcluster -n rook-ceph

# 4. StorageClass exists and is default
oc get sc

# 5. StorageProfile configured correctly
oc get storageprofile rook-ceph-block -o jsonpath='{.status.claimPropertySets}'

# 6. Ceph internal health (via toolbox)
oc -n rook-ceph exec -it deploy/rook-ceph-tools -- ceph status
```

### Test PVC Creation

```bash
# Test RWO Block PVC
cat <<EOF | oc apply -f -
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: test-rwo-block
  namespace: default
spec:
  accessModes: [ReadWriteOnce]
  volumeMode: Block
  storageClassName: rook-ceph-block
  resources:
    requests:
      storage: 1Gi
EOF

# Test RWX Block PVC (for live migration)
cat <<EOF | oc apply -f -
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: test-rwx-block
  namespace: default
spec:
  accessModes: [ReadWriteMany]
  volumeMode: Block
  storageClassName: rook-ceph-block
  resources:
    requests:
      storage: 1Gi
EOF

# Both must show Bound
oc get pvc -n default
```

Expected:

```
NAME            STATUS   STORAGECLASS      CAPACITY   ACCESS MODES   VOLUMEMODE
test-rwo-block  Bound    rook-ceph-block   1Gi        RWO            Block
test-rwx-block  Bound    rook-ceph-block   1Gi        RWX            Block
```

---

## 9. Troubleshooting

### Common Issues and Fixes

| Symptom | Root Cause | Fix |
|---|---|---|
| `no matches for kind "CephConnection"` | `csi-operator.yaml` not applied | `oc create -f csi-operator.yaml` then restart operator pod |
| `no matches for kind "OperatorConfig"` | Same as above | Same fix |
| OSD pod on worker-2 in `CrashLoopBackOff` | Disk not fully wiped | `wipefs -a` + `sgdisk --zap-all` on `/dev/nvme9n1` |
| MON pods `Pending` | Node label missing | Re-check `role=storage-node` label on all 5 nodes |
| `ErrImagePull` on any pod | Mirror registry path wrong | Verify all image env vars in `operator-openshift.yaml` |
| `HEALTH_WARN: too many PGs` | pg_autoscaler not active | Run in toolbox: `ceph config set global osd_pool_default_pg_autoscale_mode on` |
| OSD prepare job fails on masters | SCC / SELinux issue | Confirm `operator-openshift.yaml` was used (not plain `operator.yaml`) |
| StorageProfile shows empty claimPropertySets | OCP-Virt not auto-detecting profile | Manually patch StorageProfile as shown in Step 9 |
| CephCluster stuck in `Progressing` after 15min | Multiple possible causes | Check: `oc logs -n rook-ceph deploy/rook-ceph-operator --tail=100` |

### Useful Diagnostic Commands

```bash
# Operator logs (most important for debugging)
oc logs -n rook-ceph deploy/rook-ceph-operator --tail=100 -f

# OSD prepare job logs
oc logs -n rook-ceph -l app=rook-ceph-osd-prepare --tail=50

# Check all events in rook-ceph namespace
oc get events -n rook-ceph --sort-by='.lastTimestamp'

# Ceph detailed status (inside toolbox)
oc -n rook-ceph exec -it deploy/rook-ceph-tools -- ceph status
oc -n rook-ceph exec -it deploy/rook-ceph-tools -- ceph osd tree
oc -n rook-ceph exec -it deploy/rook-ceph-tools -- ceph osd df
oc -n rook-ceph exec -it deploy/rook-ceph-tools -- ceph health detail

# Check CSI driver pods
oc get pods -n rook-ceph | grep csi

# Check StorageProfile status
oc get storageprofile -o wide
```

---

### Apply Order — Quick Reference

```bash
# Complete apply order — do NOT skip or reorder
oc create -f crds.yaml
oc create -f common.yaml
oc create -f csi-operator.yaml          # mandatory for Rook v1.15+
oc create -f operator-openshift.yaml    # OpenShift-specific, includes SCC
# → wait for operator pod: Running
oc create -f cluster.yaml
# → wait for: PHASE=Ready, HEALTH=HEALTH_OK (5-10 min)
oc create -f toolbox.yaml
# → verify with: ceph status
oc apply  -f storageclass-rbd.yaml      # includes CephBlockPool
# → patch StorageProfile for OCP-Virt
```

---

*Document generated for OpenShift 4.18.30 + Rook-Ceph v1.16.6 deployment.*
*Cluster: ocp-bm.example.com | 5 nodes | Air-gapped | Bare Metal*
