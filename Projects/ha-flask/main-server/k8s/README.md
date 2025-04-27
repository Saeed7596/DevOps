* This makes Docker use the Docker daemon inside Minikube, instead of the one on your local machine, for building and running images.
* "Running `docker build -t flask-app:latest .` creates the image in your local Docker. But Minikube is a virtual environment, so that image isn't available inside it. `eval $(minikube docker-env)` makes Docker build directly in the Minikube environment, avoiding the need to `push` and `pull` from an external registry.
* Note: `eval $(minikube docker-env --unset)`
```bash
eval $(minikube docker-env)
docker build -t flask-app:latest .
docker build -f Dockerfile.postgres -t custom-postgres:latest .
```
Or
```bash
docker build -t flask-app:latest .
docker build -f Dockerfile.postgres -t custom-postgres:latest .
minikube image load flask-app:latest
minikube image load custom-postgres:latest
```

---

# 01
```bash
kubectl apply -f k8s/01-simple-pod
```
Test Database
```bash
kubectl exec -it flask-postgres-pod -c postgres-db -- psql -U myuser -d mydatabase -c "\dt"
```

```bash
kubectl port-forward pod/flask-postgres-pod 5000:5000
```

---

# 02
```bash
kubectl apply -f k8s/02-two-deployment-service/
kubectl get all
```
To access service within Minikube:
```bash
minikube service <service-name>
```
```bash
minikube service flask-app
```

---

# 03
```bash
kubectl apply -f k8s/03-nodePort-service/
minikube ip
http://<Minikube_IP>:30080
```

---

# 04
```bash
kubectl apply -f k8s/04-LoadBalancer-service/
```
### Important Note:
In Minikube, the LoadBalancer type is not truly implemented by default since Minikube is a local cluster. However, it provides a solution for testing:

To access a LoadBalancer service within Minikube:
```bash
minikube service flask-app
minikube service flask-app --url
```
This command will:
- Provide the URL
- Provide the Port
- Open the browser directly

---

# 05
```bash
kubectl apply -f k8s/05-full-project/namespace.yaml
kubectl apply -f k8s/05-full-project/secret.yaml
kubectl apply -f k8s/05-full-project/configmap.yaml
kubectl apply -f k8s/05-full-project/postgres-pv.yaml
kubectl apply -f k8s/05-full-project/postgres-pvc.yaml
kubectl apply -f k8s/05-full-project/postgres-deployment.yaml
kubectl apply -f k8s/05-full-project/postgres-service.yaml
kubectl apply -f k8s/05-full-project/flask-deployment.yaml
kubectl apply -f k8s/05-full-project/flask-service.yaml

minikube service flask-app -n flask-project
```

---


---

# 06
### install metrics-server
```bash
minikube addons enable metrics-server
kubectl get deployment metrics-server -n kube-system
# If have ImagePullBackOff error
kubectl delete pod -n kube-system -l k8s-app=metrics-server
```
For set the limits:
```bash
kubectl top pod -n flask-project
```
```bash
kubectl apply -f k8s/06-autoscale-hpa/namespace.yaml
kubectl apply -f k8s/06-autoscale-hpa/secret.yaml
kubectl apply -f k8s/06-autoscale-hpa/configmap.yaml
kubectl apply -f k8s/06-autoscale-hpa/postgres-pv.yaml
kubectl apply -f k8s/06-autoscale-hpa/postgres-pvc.yaml
kubectl apply -f k8s/06-autoscale-hpa/postgres-deployment.yaml
kubectl apply -f k8s/06-autoscale-hpa/postgres-service.yaml
kubectl apply -f k8s/06-autoscale-hpa/flask-deployment.yaml
kubectl apply -f k8s/06-autoscale-hpa/flask-service.yaml
kubectl apply -f k8s/06-autoscale-hpa/autoscale.yaml

minikube service flask-app -n flask-project
```
### Test HPA
Use some tools like:
* apache benchmark (ab)
* hey
* wrk
Or simply use
```bash
while true; do curl http://$(minikube ip):port; done
```
Or run the python app `python3 k8s/test-hpa.py `
* Note: Update the `minikube ip` in code.
### Watch result
```bash
kubectl top pod -n flask-project
kubectl get hpa -n flask-project
```
```bash
watch kubectl get hpa -n flask-project
```
```bash
kubectl events hpa -n flask-project | grep -i "ScalingReplicaSet"
kubectl events hpa -n flask-project | grep -i "FailedGetResourceMetric"
```
```bash
kubectl describe hpa flask-app-hpa -n flask-project
```

---

# 06 (OpenShift)
```bash
oc login -u developer -p developer
oc new-project flask-project
```
I used a nexus private registry to pull & push images.
Add insecure registry
```bash
sudo nano /etc/containers/registries.conf
```
```yaml
[[registry]]
location = "default-route-openshift-image-registry.apps-crc.testing"
insecure = true
```
Pull images
```bash
podman pull registry.nexus.com/flask-app:latest
podman pull registry.nexus.com/custom-postgres:latest
```
Login to crc local registry
```bash
podman login -u developer -p $(oc whoami -t) \
    default-route-openshift-image-registry.apps-crc.testing
```
```bash
oc login -u developer -p developer
oc project flask-project
```
The postgres Pod Maybe get CrashLoopBackOff error because of premission.
```bash
oc adm policy add-scc-to-user anyuid -z default -n flask-project
```
Tag and Push images to crc local registry
```bash
podman tag registry.nexus.com/flask-app:latest \
    default-route-openshift-image-registry.apps-crc.testing/flask-project/flask-app:latest
```
```bash
podman push \
    default-route-openshift-image-registry.apps-crc.testing/flask-project/flask-app:latest
```
```bash
podman tag registry.nexus.com/custom-postgres:latest \
    default-route-openshift-image-registry.apps-crc.testing/flask-project/custom-postgres:latest
```
```bash
podman push \
    default-route-openshift-image-registry.apps-crc.testing/flask-project/custom-postgres:latest
```
Edit `flask-deployment.yaml`
```bash
image: image-registry.openshift-image-registry.svc:5000/flask-project/flask-app:latest
```
Edit `postgres-deployment.yaml`
```bash
spec:
  template:
    spec:
      securityContext:
        fsGroup: 26
      containers:
        - name: postgres
          image: default-route-openshift-image-registry.apps-crc.testing/flask-project/custom-postgres:latest
```
In OpenShift CRC, services do not automatically create routes. So we create a route:
```bash
oc expose svc flask-app -n flask-project
oc get routes -n flask-project
```
