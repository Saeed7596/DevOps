
# OpenShift Port Mapping Guide

A clear table showing how **Deployment → Service → Route** must connect together.

---

## Port Mapping Table

| Component     | Value             | Description |
|---------------|-------------------|-------------|
| **Deployment (Pod)** | `containerPort = 8080` | The pod listens on this port. |
| **Service → targetPort** | `targetPort = 8080` | The service forwards traffic to this exact port inside the pod. Must match `containerPort`. |
| **Service → port** | `port = 8085` | The internal service port. Routes can only target this port. |
| **Route → spec.port.targetPort** | `8085` | The route must point to the service **port**, not the pod port. Must match `service.port`. |

---

## Visual Flow
```bash
Route (8085)
│
▼
Service (port=8085 → targetPort=8080)
│
▼
Pod (containerPort=8080)
```

## YAML Files
1. Deploymeny
```yaml
spec:
  template:
    spec:
      containers:
        - name: app
        image: your-image
        ports:
          - containerPort: 8080
```
2. Service
```yaml
spec:
  ports:
    - protocol: TCP
      port: 8085
      targetPort: 8080
```
3. Route
```yaml
spec:
  to:
    kind: Service
    name: app-service
  port:
    targetPort: 8085
```

---

## If Use Service with name:
1. Service
```yaml
spec:
  ports:
    - name: http
      port: 8085
      targetPort: 8080
```
2. Route
```yaml
spec:
  port:
    targetPort: http
```

---

## Summary

| From | To | Value |
|------|----|--------|
| Route | Service.port | 8085 |
| Service.targetPort | Deployment.containerPort | 8080 |

---

## With CLI
0. Create Namespace
```bash
oc new-project <your-project-name> 

oc project <your-project-name>
```
1. Create Deployment
```yaml
spec:
  containers:
    - name: app
      image: your-image
      ports:
        - containerPort: 8080
```
2. Create Service
```bash
oc expose deployment app --port=8085 --target-port=8080 --name=app-service
```
3. Create Route
```bash
oc expose service app-service --name=app-route
```
4. Get URL
```bash
oc get route app-route -o jsonpath='{.spec.host}'
```
