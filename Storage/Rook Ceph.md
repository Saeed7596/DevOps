# [Rook Ceph](https://rook.io/)

---

## Quickstart
1. A simple Rook cluster is created for Kubernetes with the following kubectl commands and [example manifests](https://github.com/rook/rook/blob/release-1.18/deploy/examples).
```bash
git clone --single-branch --branch v1.18.8 https://github.com/rook/rook.git
cd rook/deploy/examples
kubectl create -f crds.yaml -f common.yaml -f csi-operator.yaml -f operator.yaml
kubectl create -f cluster.yaml
```
2. Cluster Environments. <br />
edit `cluster.yaml` file
```bash
cp cluster.yaml my-cluster.yaml

nano my-cluster.yaml
```
You must have already created the `sdb` partition.
```yaml
storage:
  useAllNodes: true
  useAllDevices: false
  devices: 
    - name: "sdb"
```
```bash
kubectl create -f my-cluster.yaml
```

---

3. Verify
```bash
kubectl get pods -n rook-ceph 
```
**Hint**: If the `rook-ceph-mon`, `rook-ceph-mgr`, or `rook-ceph-osd` pods are not created,
please refer to the [Ceph common issues](https://rook.io/docs/rook/latest-release/Troubleshooting/ceph-common-issues/) for more details and potential solutions.<br />

To verify that the cluster is in a healthy state, connect to the [Rook toolbox](https://rook.io/docs/rook/latest-release/Troubleshooting/ceph-toolbox/) and run the `ceph status` command.

* All mons should be in quorum
* A mgr should be active
* At least three OSDs should be up and in
* If the health is not HEALTH_OK, the warnings or errors should be investigated
```bash
$ ceph status
  cluster:
    id:     a0452c76-30d9-4c1a-a948-5d8405f19a7c
    health: HEALTH_OK

  services:
    mon: 3 daemons, quorum a,b,c (age 3m)
    mgr:a(active, since 2m), standbys: b
    osd: 3 osds: 3 up (since 1m), 3 in (since 1m)
[]...]
```

---

## Storage
For a walkthrough of the three types of storage exposed by Rook, see the guides for:

* `Block`: Create block storage to be consumed by a pod (RWO)
* `Shared Filesystem`: Create a filesystem to be shared across multiple pods (RWX)
* `Object`: Create an object store that is accessible with an S3 endpoint inside or outside the Kubernetes cluster

---

## Ceph Dashboard
Ceph has a dashboard to view the status of the cluster. See the [dashboard guide](https://rook.io/docs/rook/latest-release/Storage-Configuration/Monitoring/ceph-dashboard/).

---

## Create the [filesystem](https://rook.io/docs/rook/latest-release/Storage-Configuration/Shared-Filesystem-CephFS/filesystem-storage/) 
```bash
kubectl create -f filesystem.yaml
```
Or edit `filesystem.yaml`
```bash
cp filesystem.yaml my-filesystem.yaml

nano my-filesystem.yaml
```
```yaml
apiVersion: ceph.rook.io/v1
kind: CephFilesystem
metadata:
  name: myfs
  namespace: rook-ceph
spec:
  metadataPool:
    replicated:
      size: 3
  dataPools:
    - name: replicated
      replicated:
        size: 3
  preserveFilesystemOnDelete: true
  metadataServer:
    activeCount: 1
    activeStandby: true
```
```bash
kubectl create -f my-filesystem.yaml
```
## Verify
```bash
kubectl -n rook-ceph get pod -l app=rook-ceph-mds
```

---

# Provision Storage
```bash
nano my-storageclass.yaml
```

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: rook-cephfs
# Change "rook-ceph" provisioner prefix to match the operator namespace if needed
provisioner: rook-ceph.cephfs.csi.ceph.com
parameters:
  # clusterID is the namespace where the rook cluster is running
  # If you change this namespace, also change the namespace below where the secret namespaces are defined
  clusterID: rook-ceph

  # CephFS filesystem name into which the volume shall be created
  fsName: myfs

  # Ceph pool into which the volume shall be created
  # Required for provisionVolume: "true"
  pool: myfs-replicated

  # The secrets contain Ceph admin credentials. These are generated automatically by the operator
  # in the same namespace as the cluster.
  csi.storage.k8s.io/provisioner-secret-name: rook-csi-cephfs-provisioner
  csi.storage.k8s.io/provisioner-secret-namespace: rook-ceph
  csi.storage.k8s.io/controller-expand-secret-name: rook-csi-cephfs-provisioner
  csi.storage.k8s.io/controller-expand-secret-namespace: rook-ceph
  csi.storage.k8s.io/controller-publish-secret-name: rook-csi-cephfs-provisioner
  csi.storage.k8s.io/controller-publish-secret-namespace: rook-ceph
  csi.storage.k8s.io/node-stage-secret-name: rook-csi-cephfs-node
  csi.storage.k8s.io/node-stage-secret-namespace: rook-ceph

reclaimPolicy: Delete
```
```bash
kubectl create -f my-storageclass.yaml
```

---

## [Openshift](https://rook.io/docs/rook/latest-release/Getting-Started/ceph-openshift/)
```bash
oc create -f crds.yaml -f common.yaml -f csi-operator.yaml
oc create -f operator-openshift.yaml
```
```bash
cp cluster.yaml my-cluster.yaml

nano my-cluster.yaml
```
You must have already created the `sdb` partition.
```yaml
storage:
  useAllNodes: false
  useAllDevices: false
  nodes:
    - name: <node-name>
      devices: 
        - name: "sdb"
    - name: <node-name>
      devices: 
        - name: "sdb"
```
```yaml
placement:
  all:
    nodeAffinity:
      requiredDuringsSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
        - matchExpressions:
          - key: ceph-storage
            operator: In
            values:
            - "True"
    tolerations:
    - key: storage
      operator: Equal
      value: ceph
      effect: NoSchedule
```
```bash
oc create -f my-cluster.yaml
```

---
