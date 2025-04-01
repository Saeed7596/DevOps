* This makes Docker use the Docker daemon inside Minikube, instead of the one on your local machine, for building and running images.
* "Running `docker build -t flask-app:latest .` creates the image in your local Docker. But Minikube is a virtual environment, so that image isn't available inside it. `eval $(minikube docker-env)` makes Docker build directly in the Minikube environment, avoiding the need to `push` and `pull` from an external registry.
* Note: `eval $(minikube docker-env --unset)`
```bash
eval $(minikube docker-env)
docker build -t flask-app:latest .
docker build -f Dockerfile.postgres -t custom-postgres:latest .
```
```bash
kubectl apply -f 00-pod.yaml
kubectl apply -f 00-postgres-service.yaml
```
Test Database
```bash
kubectl exec -it flask-postgres-pod -c postgres-db -- psql -U myuser -d mydatabase -c "\dt"
```
```bash
kubectl port-forward pod/flask-postgres-pod 5000:5000
```
