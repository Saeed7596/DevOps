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

