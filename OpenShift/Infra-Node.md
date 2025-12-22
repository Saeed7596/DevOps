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
    enableUserWorkload: true

    nodeSelector:
      node-role.kubernetes.io/infra: ""
    tolerations:
    - key: "node-role.kubernetes.io/infra"
      operator: "Exists"
      effect: "NoSchedule"

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
```

## Verification
```bash
oc get pods -n openshift-monitoring -o wide

# ClusterOperator
oc get co monitoring
```
## Edit User Workload
```bash
oc edit configmap user-workload-monitoring-config -n openshift-user-workload-monitoring
```
```yaml
data:
  config.yaml: |
    nodeSelector:
      node-role.kubernetes.io/infra: ""
    tolerations:
    - key: node-role.kubernetes.io/infra
      operator: Exists
      effect: NoSchedule
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
