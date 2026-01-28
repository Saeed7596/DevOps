# [NetWork Policy](https://docs.redhat.com/en/documentation/openshift_container_platform/4.17/html/network_security/network-policy)
If you want to control traffic flow at the IP address or port level (OSI layer 3 or 4), NetworkPolicies allow you to specify rules for traffic flow within your cluster, and also between Pods and the outside world.

---

# Usage:

* inside the cluster → `podSelector`
* out of the cluster → `ipBlock`
* Multiple Sources → `matchExpressions` (In)

---

# Note:
If destination namespace enforces ingress isolation, a matching ingress policy must exist.

* Egress on source
* Ingress on destination

---

## Deny All in OpenShift
```yaml
kind: NetworkPolicy
apiVersion: networking.k8s.io/v1
metadata:
  name: default-deny-all
  namespace: wallet
spec:
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          # Allows ingress traffic from OpenShift Routers
          policy-group.network.openshift.io/ingress: ""
  egress:
  - ports:
    - protocol: UDP
      port: 5353
    to:
      - namespaceSelector:
          matchLabels:
            # Allows egress traffic to OpenShift DNS 
            kubernetes.io/metadata.name: openshift-dns
  podSelector: {} # Apply on all Pods within the namespace
  policyTypes:
  - Ingress
  - Egress
```

### Only accept connections from pods within a project:
```yaml
kind: NetworkPolicy
apiVersion: networking.k8s.io/v1
metadata:
  name: allow-same-namespace
spec:
  podSelector: {}
  ingress:
  - from:
    - podSelector: {}
```

---

## Egress Sample
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: <name>
  namespace: <namespace>
spec:
  podSelector:
    matchLabels:
      app: <SOURCE_APP>
  policyTypes:
  - Egress
  egress:
  - to:
    - podSelector:
        matchLabels:
          app: <DEST_APP>
    ports:
    - protocol: TCP
      port: <PORT>
  - to:
    - ipBlock: 
        cidr: <DEST_IP/32>
    ports:
    - protocol: TCP
      port: <PORT>
```

---

## Ingress Sample
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: <name>
  namespace: <namespace>
spec:
  podSelector:
    matchLabels:
      app: <DEST_APP>
  policyTypes:
  - Ingress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: <SOURCE_APP>
    ports:
    - protocol: TCP
      port: <PORT>
  - from:
    - ipBlock: 
        cidr: <DEST_IP/32>
    ports:
    - protocol: TCP
      port: <PORT>
```

---

# matchExpressions
When designing your network policy, refer to the following guidelines:  
For network policies with the same `spec.podSelector` spec, it is more efficient to use one network policy with multiple `ingress` or `egress` rules, than multiple network policies with subsets of `ingress` or `egress` rules.  
Every `ingress` or `egress` rule based on the `podSelector` or `namespaceSelector` spec generates the number of OVS flows proportional to `number of pods selected by network policy + number of pods selected by ingress or egress rule`. Therefore, it is preferable to use the `podSelector` or `namespaceSelector` spec that can select as many pods as you need in one rule, instead of creating individual rules for every pod.  
For example, the following policy contains two rules:
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: test-network-policy
spec:
  podSelector: {}
  ingress:
  - from:
    - podSelector:
        matchLabels:
          role: frontend
  - from:
    - podSelector:
        matchLabels:
          role: backend
```
The following policy expresses those same two rules as one:
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: test-network-policy
spec:
  podSelector: {}
  ingress:
  - from:
    - podSelector:
        matchExpressions:
        - {key: role, operator: In, values: [frontend, backend]}
```
The same guideline applies to the spec.podSelector spec. If you have the same ingress or egress rules for different network policies, it might be more efficient to create one network policy with a common spec.podSelector spec. For example, the following two policies have different rules:
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: policy1
spec:
  podSelector:
    matchLabels:
      role: db
  ingress:
  - from:
    - podSelector:
        matchLabels:
          role: frontend
---
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: policy2
spec:
  podSelector:
    matchLabels:
      role: client
  ingress:
  - from:
    - podSelector:
        matchLabels:
          role: frontend
```
The following network policy expresses those same two rules as one:
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: policy3
spec:
  podSelector:
    matchExpressions:
    - {key: role, operator: In, values: [db, client]}
  ingress:
  - from:
    - podSelector:
        matchLabels:
          role: frontend
```
You can apply this optimization when only multiple selectors are expressed as one. In cases where selectors are based on different labels, it may not be possible to apply this optimization. In those cases, consider applying some new labels for network policy optimization specifically.

---

# Access to a Sevice from Another namespace
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-from-left-namespace-from-specific-pod
spec:
  podSelector: 
    matchLabels:
      deployment: richard
  policyTypes:
  - Ingress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          projectName: left
      podSelector:
        matchLabels:
          deployment: mark
    ports:
    - protocol: TCP
      port: 80
    - protocol: TCP
      port: 443     
```

---

# Product Example
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: <microservice>-<namespace>
  namespace: <namespace>
spec:
  podSelector:
    matchLabels:
      app: frontend # microservice label
  egress:
  # Internal Pods
  - to:
    - podSelector:
        matchLabels:
          app: office
    ports:
    - protocol: TCP
      port: 3000
  - to:
    - podSelector:
        matchLabels:
          app: core
    ports:
    - protocol: TCP
      port: 8090
  - to:
    - podSelector:
        matchLabels:
          app.kubernetes.io/name: redis
    ports:
    - protocol: TCP
      port: 6379
  # External DataBase
  - to:
    - ipBlock:
        cidr: <DEST_IP/32>
    - ipBlock:
        cidr: <DEST_IP/32>
    - ipBlock:
        cidr: <DEST_IP/32>
    ports:
    - protocol: TCP
      port: 27017
  ingress:
  - from:
    - podSelector:
        matchExpressions:
          - {key: app, operator: In, values: [dispatcher, payment-back]}
    ports:
    - protocol: TCP
      port: 3000 # Target Port of microservice (frontend)
  policyTypes: 
    - Egress
    - Ingress
```
### Allow ingress redis from another namespace
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-redis-from-<another-namespace>
  namespace: <namespace name that have redis>
spec:
  podSelector:
    matchLabels:
      app.kubernetes.io/name: redis
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          kubernetes.io/metadata.name: <another-namespace>
      podSelector:
        matchExpressions:
          - {key: app, operator: In, values: [dispatcher, partnermanage, backoffice-backend, tsp]}
    ports:
    - protocol: TCP
      port: 6379
  policyTypes: 
    - Ingress
```