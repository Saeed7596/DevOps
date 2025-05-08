# Config helm
```bash
helm create deploy
```
This command will be create a deploy directory.

---

## Change this parameters!
```bash
nano deploy/Chart.yaml
```
```yaml
name: myapp
```
---
```bash
nano deploy/values.yaml
```
```yaml
replicaCount: 3
image:
  repository: registry.nexus.ir/image-name
  tag: v1
imagePullSecrets:
  - name: my-secret-nexus
ingress:
  enabled: true
  className: nginx
  hosts:
    - host: saeed.example.ir
      paths:
        - path: /
          pathType: ImplementationSpecific
```

---

## Create a secret for your docker registry
```bash
kubectl create secret docker-registry my-secret-nexus \
  --docker-username=username \
  --docker-password=password \
  --docker-server=https://registry.nexus.ir \
  --docker-email=your-email@example.com -n <namespace-name>
```
