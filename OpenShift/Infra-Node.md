# Infra Node Setting

## Labeled the two worker node as infra
```bash
oc label node <node_name> node-role.kubernetes.io/infra=""

oc label node worker-0 node-role.kubernetes.io/infra=""
oc label node worker-1 node-role.kubernetes.io/infra=""


oc get nodes -L node-role.kubernetes.io/infra
```

## 1. Ingress Route.
Note: After applying these changes, update your `HAProxy` configuration so that ports `80` and `443` point to the `IP addresses` of these `infra nodes`.
## Taint these node
```bash
oc adm taint nodes worker-0 node-role.kubernetes.io/infra:NoSchedule
oc adm taint nodes worker-1 node-role.kubernetes.io/infra:NoSchedule
```

---

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

# Taint and Toleration Note❗❗❗
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
