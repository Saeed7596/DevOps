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

## [Scale Up Node Resource](https://docs.redhat.com/en/documentation/openshift_container_platform/4.20/html/updating_clusters/performing-a-cluster-update#updating-virtual-hardware-on-vsphere_updating-hardware-on-nodes-running-in-vsphere)
```bash
oc get nodes
```
#### **Note**: For master node, run this command and not necessary use `drain`
```bash
oc adm cordon <control_plane_node>
```
#### For worker node
**Note**: Not necessary to run `oc adm cordon <node_name>` because `drain` automatically use `cordon`
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

## Enable alerts custom
```yaml
alertmanager:
  enabled: true
  nodeSelector:
    node-role.kubernetes.io/infra: ""
  tolerations:
  - key: "node-role.kubernetes.io/infra"
    operator: "Exists"
    effect: "NoSchedule"
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

# [AlertManager](https://docs.redhat.com/en/documentation/openshift_container_platform/4.17/html/postinstallation_configuration/configuring-alert-notifications)


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

# [Good Docs about infra](https://docs.redhat.com/en/documentation/openshift_container_platform/4.20/html/machine_management/creating-infrastructure-machinesets)

# Typical Workloads for Infra Nodes in OpenShift

Infra nodes are dedicated nodes designed to isolate critical cluster services and network-facing workloads from general worker workloads.  
Typical workloads placed on infra nodes include:

- **Ingress / Router**
  - All routes and IngressController pods
  - Handles incoming user traffic (HTTP/HTTPS)

- **Registry / Image Registry**
  - Resource-intensive storage workloads
  - Keeps worker nodes free for application pods

- **Monitoring / Metrics / Logging**
  - Prometheus, Alertmanager, Grafana
  - Loki, EFK, or cluster logging components
  - User workload monitoring (if desired on infra)

- **Service Mesh Components** (Optional)
  - OpenShift Service Mesh / Istio control plane pods

- **Other critical cluster services**
  - Cluster Operators requiring dedicated resources
  - Certificate management pods (e.g., cert-manager)

---

# Infra Node Setting

## Designated two worker nodes as infra nodes
```bash
oc label node <node_name> node-role.kubernetes.io/infra=""

oc label node worker-0 node-role.kubernetes.io/infra=""
oc label node worker-1 node-role.kubernetes.io/infra=""


oc get nodes -L node-role.kubernetes.io/infra

oc get nodes -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.metadata.labels["node-role.kubernetes.io/infra"]}{"\n"}{end}'
```
## Taint these node
```bash
oc adm taint nodes worker-0 node-role.kubernetes.io/infra:NoSchedule
oc adm taint nodes worker-1 node-role.kubernetes.io/infra:NoSchedule
```
```bash
oc describe node <node-name> | grep Taints
```
## Note: After applying these changes, update your `HAProxy` configuration so that ports `80` and `443` point to the `IP addresses` of these `infra nodes`. <br />

---

# 1. Ingress Route.
Ensure router replicas >= number of infra nodes (recommended: 2)
```bash
oc get deployment router-default -n openshift-ingress
```
```bash
oc scale deployment/router-default -n openshift-ingress --replicas=2
```

## Edit ingress controller
**In console -> Administrator -> Cluster Settings -> Configuration -> ingress controller**
```bash
oc get pods -n openshift-ingress -o wide

oc edit ingresscontroller default -n openshift-ingress-operator
```
```yaml
spec:
  nodePlacement:
    nodeSelector:
      matchLabels:
        node-role.kubernetes.io/infra: ""
    tolerations:
    - key: "node-role.kubernetes.io/infra"
      operator: "Exists"
      effect: "NoSchedule"
```

## Make sure all pods are up on the `infra nodes`.
```bash
oc get pods -n openshift-ingress -o wide
```

---

# 2. Cluster Monitoring
## Edit configmap or created first.
```bash
oc edit configmap cluster-monitoring-config -n openshift-monitoring
```
```yaml
data:
  config.yaml: |
    <component>
      tolerations:
        <tolerations-specification>
```
## Find Component
```bash
oc get pods -n openshift-monitoring
```
```yaml
data:
  config.yaml: |
    enableUserWorkload: true

    prometheusK8s:
      nodeSelector:
        node-role.kubernetes.io/infra: ""
      tolerations:
      - key: "node-role.kubernetes.io/infra"
        operator: "Exists"
        effect: "NoSchedule"

    alertmanagerMain:
      nodeSelector:
        node-role.kubernetes.io/infra: ""
      tolerations:
      - key: "node-role.kubernetes.io/infra"
        operator: "Exists"
        effect: "NoSchedule"

    prometheusOperator:
      nodeSelector:
        node-role.kubernetes.io/infra: ""
      tolerations:
      - key: "node-role.kubernetes.io/infra"
        operator: "Exists"
        effect: "NoSchedule"

    kubeStateMetrics:
      nodeSelector:
        node-role.kubernetes.io/infra: ""
      tolerations:
      - key: "node-role.kubernetes.io/infra"
        operator: "Exists"
        effect: "NoSchedule"

    openshiftStateMetrics:
      nodeSelector:
        node-role.kubernetes.io/infra: ""
      tolerations:
      - key: "node-role.kubernetes.io/infra"
        operator: "Exists"
        effect: "NoSchedule"

    metricsServer:
      nodeSelector:
        node-role.kubernetes.io/infra: ""
      tolerations:
      - key: "node-role.kubernetes.io/infra"
        operator: "Exists"
        effect: "NoSchedule"

    monitoringPlugin:
      nodeSelector:
        node-role.kubernetes.io/infra: ""
      tolerations:
      - key: "node-role.kubernetes.io/infra"
        operator: "Exists"
        effect: "NoSchedule"

    thanosQuerier:
      nodeSelector:
        node-role.kubernetes.io/infra: ""
      tolerations:
      - key: "node-role.kubernetes.io/infra"
        operator: "Exists"
        effect: "NoSchedule"
```

## Delete Pod (if needed)
```
oc project openshift-monitoring

oc get pods -o wide

oc get pods -o name | xargs oc delete
```

## Verification
```bash
oc get pods -n openshift-monitoring -o wide

# ClusterOperator
oc get co monitoring
```
## Log
```bash
oc logs -f prometheus-operator-... -n openshift-monitoring
```

---

## Edit User Workload
```bash
oc edit configmap user-workload-monitoring-config -n openshift-user-workload-monitoring
```
```yaml
data:
  config.yaml: |
    prometheusOperator:
      nodeSelector:
        node-role.kubernetes.io/infra: ""
      tolerations:
      - key: "node-role.kubernetes.io/infra"
        operator: "Exists"
        effect: "NoSchedule"
    prometheus:
      nodeSelector:
        node-role.kubernetes.io/infra: ""
      tolerations:
      - key: "node-role.kubernetes.io/infra"
        operator: "Exists"
        effect: "NoSchedule"
    thanosRuler:
      nodeSelector:
        node-role.kubernetes.io/infra: ""
      tolerations:
      - key: "node-role.kubernetes.io/infra"
        operator: "Exists"
        effect: "NoSchedule"
```
## Enable alerts custom
```bash
alertmanager:
  enabled: true
  nodeSelector:
    node-role.kubernetes.io/infra: ""
  tolerations:
  - key: "node-role.kubernetes.io/infra"
    operator: "Exists"
    effect: "NoSchedule"
```
## Delete Pod (id needed)
```
oc project openshift-monitoring

oc get pods -o wide

oc get pods -o name | xargs oc delete
```
## Verification
```bash
oc get pods -n openshift-user-workload-monitoring -o wide
```

---

# 3. Image Registry
**Note**: Ensure the image registry uses persistent storage (PVC).<br />
Do NOT use emptyDir in production.
```bash
oc get configs.imageregistry.operator.openshift.io cluster -o yaml | grep -A5 storage:
```
If `emptyDir` → this document is incomplete for prod
## Enable image-registry
### Create PVC
```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: image-registry-storage
  namespace: openshift-image-registry
spec:
  accessModes:
  - ReadWriteOnce
  resources:
    requests:
      storage: 100Gi
  storageClassName: thin-csi  # storageClass vSphere
```
## Edit Image Registry Operator
```bash
oc edit configs.imageregistry.operator.openshift.io cluster
```
```yaml
spec:
  managementState: Managed
  storage:
    pvc:
      claim: image-registry-storage
```

---

## Edit 
```bash
oc edit configs.imageregistry.operator.openshift.io cluster
```
```yaml
spec:
  nodeSelector:
    node-role.kubernetes.io/infra: ""
  tolerations:
  - key: "node-role.kubernetes.io/infra"
    operator: "Exists"
    effect: "NoSchedule"
```
## Verification
```bash
# image-registry pods must be on infra
oc get pods -n openshift-image-registry -o wide

# Registry health
oc get co image-registry
```

---

# 4. OAuth is controlled by `Deployment`.
## Edit
```bash
oc patch deployment oauth-openshift \
  -n openshift-authentication \
  --type=merge \
  -p '{
    "spec": {
      "template": {
        "spec": {
          "nodeSelector": {
            "node-role.kubernetes.io/infra": ""
          },
          "tolerations": [{
            "key": "node-role.kubernetes.io/infra",
            "operator": "Exists",
            "effect": "NoSchedule"
          }]
        }
      }
    }
  }'
```
## Verification
```bash
oc get pods -n openshift-authentication -o wide
oc get co authentication
```
## Note
After upgrades, re-verify oauth-openshift deployment node placement.<br />
OAuth deployment is operator-managed and may be reconciled during upgrades.<br />
Check after Upgrade
```bash
oc get pods -n openshift-authentication -o wide
```
```bash
oc rollout history deployment/oauth-openshift -n openshift-authentication
```

---

# Overall Verification
```
oc adm top nodes

oc get pods -A -o wide | grep infra

oc get co
```

---

# Taint and Toleration Note❗❗❗
Depending on the object, you can use one or more of the following rule types:
* `nodeSelector`:  
  Allows pods to be scheduled on nodes that are labeled with the key-value pair or pairs that you specify in this field. The node must have labels that exactly match all listed pairs.
* `affinity`:  
  Enables you to use more expressive syntax to set rules that match nodes with pods. Affinity also allows for more nuance in how the rules are applied. For example, you can specify that a rule is a preference, not a requirement. If a rule is a preference, pods are still scheduled when the rule is not satisfied.
* `tolerations`:  
  Allows pods to be scheduled on nodes that have matching taints. If a taint is applied to a node, that node only accepts pods that tolerate the taint.

---

```yaml
tolerations:
- key: "node-role.kubernetes.io/infra"
  operator: "Exists"
  effect: "NoSchedule"
- key: "node-role.kubernetes.io/infra"
  operator: "Exists"
  effect: "NoExecute"
```
# Understanding Why Both `NoSchedule` and `NoExecute` Taints Are Needed

When configuring **infra nodes** in an OpenShift cluster (for workloads such as Ingress Controller, Registry, or Monitoring), it is common to use both `NoSchedule` and `NoExecute` taints.  
Although they may look similar, they provide different behaviors and complement each other.

---

## `NoSchedule`
This taint ensures:

- New pods **without matching tolerations** are **not scheduled** onto the infra node.
- Existing pods that are already running on the node **will remain**.

**Purpose:**  
Prevent non-infra workloads from being scheduled to infra nodes.

---

## `NoExecute`
This taint ensures:

- Pods **without matching tolerations** will **not be scheduled**, and  
- Existing non-tolerating pods on the node will be **evicted** (removed).

**Purpose:**  
Ensure only infra workloads remain on infra nodes, especially when taints change or during maintenance.

---

## Why Both Are Required

Using **only `NoSchedule`**:

- Prevents new pods from being scheduled
- BUT existing non-infra pods may continue running on the node  
  (undesirable when reconfiguring an infra node)

Using **only `NoExecute`**:

- Evicts pods without tolerations
- BUT does not prevent new non-infra pods from being scheduled later

---

## Conclusion

These taints are **not duplicates**.  
They work together to protect infra nodes:

- `NoSchedule` blocks new unwanted pods  
- `NoExecute` removes unwanted existing pods  

Together, they ensure infra nodes run only the workloads they are meant to serve.

---

# 🔍 Summary 

| Effect           | New pod without tolerance | Old pod without tolerance | Severity  |
|------------------|---------------------------|---------------------------|-----------|
| NoSchedule       | ❌ It doesn't let         | ✔ Stays                  | High      |
| PreferNoSchedule | ⚠ He prefers not to       | ✔ Stays                  | Low       |
| NoExecute        | ❌ It doesn't let         | ❌ Deletes               | Very High |

* If you want someone to not put a pod on the infra by mistake, but you haven't forced it = Use `PreferNoSchedule`.
* If you want no pod to come unless it has tolerance = Use `NoSchedule`.
* If you want to eject a pod even if it is on the node = Use `NoExecute`.

---
