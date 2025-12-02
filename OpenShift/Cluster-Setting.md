# Check Cluster
```bash
# nodes and versions
oc get nodes -o wide
oc get clusterversion

# cluster operators health
oc get co
oc get clusteroperators

# etcd endpoints status (run on master where etcd pod exists)
oc -n openshift-etcd get pods
oc -n openshift-etcd exec -it etcd-<pod> -- etcdctl endpoint status --cluster
```

---

# Setting
## Disabling the default OperatorHub catalog sources 
in console **`Administrator -> Cluster Setting -> Configuration ->  OperatorHub`**

add this
```yaml
spec: 
  disableAllDefaulSources: true
```
or
```bash
oc patch OperatorHub cluster --type json \
    -p '[{"op": "add", "path": "/spec/disableAllDefaultSources", "value": true}]'
```

in console **`Administrator -> Cluster Setting -> Configuration ->  ClusterVersion details`**

remove spec.channel
```yaml
spec:
  channel: stable-4.17
```

---

# CronJob fot etcd ❗❗❗
```bash
apiVersion: batch/v1
kind: CronJob
metadata:
  name: etcd-snapshot
  namespace: openshift-etcd
spec:
  schedule: "0 */6 * * *"
  jobTemplate:
    spec:
      template:
        spec:
          serviceAccountName: etcd
          containers:
          - name: snapshot
            image: registry.access.redhat.com/ubi8/etcd:latest
            command:
            - /bin/sh
            - -c
            - |
              ETCDCTL_API=3 etcdctl snapshot save /backup/snap-$(date +%Y%m%d%H%M).db \
                --endpoints=https://127.0.0.1:2379 --cacert=/etc/etcd/ca.crt \
                --cert=/etc/etcd/etcd-client.crt --key=/etc/etcd/etcd-client.key
            volumeMounts:
            - mountPath: /backup
              name: backup
          restartPolicy: OnFailure
          volumes:
          - name: backup
            persistentVolumeClaim:
              claimName: etcd-backup-pvc
```

---

## [Scale Up Node Resource](https://docs.redhat.com/en/documentation/openshift_container_platform/4.20/html/updating_clusters/performing-a-cluster-update#updating-virtual-hardware-on-vsphere_updating-hardware-on-nodes-running-in-vsphere)
```bash
oc get nodes
```
**Note**: Not necessary because `drain` automatically use `cordon`
```bash
oc adm cordon <node_name>
```
```bash
oc adm drain <node_name> --ignore-daemonsets --delete-emptydir-data

oc adm drain <node_name> --grace-period 1 --ignore-daemonsets --delete-emptydir-data

oc adm drain <node_name> --grace-period 1 --ignore-daemonsets --delete-emptydir-data --force
```
1. Shut down the virtual machine (VM) associated with the compute node. Do this in the vSphere client by right-clicking the VM and selecting `Power -> Shut Down Guest OS`. Do not shut down the VM using Power Off because it might not shut down safely.

2. Edit Resources

3. Save!

4. Turn On the VM in vCenter.

5. Wait for the node to report as `Ready`
```bash
oc wait --for=condition=Ready node/<node_name>
```

```bash
oc adm uncordon <node_name>
```

---

# Monitoring
## [Enable User Workload Monitoring](https://docs.redhat.com/en/documentation/openshift_container_platform/4.20/html/monitoring/configuring-user-workload-monitoring)

---

## Edit the `cluster-monitoring-config` `ConfigMap` object:

```bash
oc -n openshift-monitoring edit configmap cluster-monitoring-config
```
Add `enableUserWorkload: true` under `data/config.yaml`:
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: cluster-monitoring-config
  namespace: openshift-monitoring
data:
  config.yaml: |
    enableUserWorkload: true 
```

---

# Verify 
```bash
oc -n openshift-user-workload-monitoring get pod
```
```text
NAME                                   READY   STATUS        RESTARTS   AGE
prometheus-operator-6f7b748d5b-t7nbg   2/2     Running       0          3h
prometheus-user-workload-0             4/4     Running       1          3h
prometheus-user-workload-1             4/4     Running       1          3h
thanos-ruler-user-workload-0           3/3     Running       0          3h
thanos-ruler-user-workload-1           3/3     Running       0          3h
```

---
