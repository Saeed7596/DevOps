# [Helm](https://helm.sh/)
Helm is a Package Manager for Kubernetes that helps manage and deploy applications in a Kubernetes cluster in a versatile and efficient manner.
## Helm Benefits
- `Easier management of Kubernetes YAMLs`: With Charts, there is no need to write multiple YAML files.
- `Reusability`: Ability to reuse Helm Charts to quickly deploy similar applications.
- `Release Management`: Ability to upgrade, rollback, and manage different versions of an application.
- `Reduced complexity`: Instead of defining multiple Manifests, you only run one Helm Chart.
## Concepts:
- `Chart`: A package containing all the resources Kubernetes needs to run an application.
- `Release`: An installed instance of a Chart in Kubernetes.
- `Repository`: A place to store and distribute Charts.
- `Values.yaml`: A file to configure variables in a Chart.

## Install Helm
```bash
curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3
chmod 700 get_helm.sh
./get_helm.sh
```
## Basic Commands

| Task                          | Command                                                      |
| ----------------------------- | ------------------------------------------------------------ |
| Help                          | `helm help`                                                  |
| Helm Version                  | `helm version`                                               |
| Add a Chart Repository        | `helm repo add [repo-name] [repo-url]`                       |
| Update Repositories           | `helm repo update`                                           |
| Remove a added Repository     | `helm repo remove [repo-name]` or `helm repo rm [repo-name]` |
| Search for Charts             | `helm search repo [keyword]`                                 |
| Install a Chart               | `helm install [release-name] [chart]`                        |
| Upgrade a Release             | `helm upgrade [release-name] [chart] [flags]`                |
| Uninstall a Release           | `helm uninstall [release-name]`                              |
| List Installed Releases       | `helm list` or `helm ls`                                     |
| List Added Helm Repositories  | `helm repo list` or `helm repo ls`                           |
| Show Installed Release Status | `helm status [release-name]`                                 |
| Get Release Values            | `helm get values [release-name]`                             |
| Create a new Helm chart       | `helm create [chart-name]`                                   |
| Renders Helm chart templates  | `helm template [RELEASE_NAME] [CHART] [flags]`               |

Note:
- `repo-name` is custom name that you set for the repository.

---

**Search Example:**
```bash
helm search [subcommand] [keyword]
```
- [subcommmand] One of the following two options:
  - `repo`: Search in the Helm tanks you've added earlier.
  - `hub`: Search in Helm Hub, which contains a set of Helm general tanks.
- [Keyword]: The name of the chart or the word you want to search.
```bash
helm search repo nginx
helm search hub nginx
helm search hub consul | grep hashicorp
```
**Some Example:**
```bash
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update <repo-name> -n <namespace-name>

helm repo rm bitnami

helm upgrade dazzling-web bitnami/nginx --version 18.3.6
helm rollback <release-name>
helm rollback dazzling-web

helm install amaze-surf bitnami/apache

helm list # Show installed <release-name>
helm ls -A
helm ls -n <namespace-name>

helm history <release-name>
```
**helm Template**
```bash
# Render a chart locally
helm template myapp ./mychart
helm template myapp . --namespace [namespace-name]

# Render with specific values file
helm template myapp ./mychart -f values-production.yaml

# Save output to files
helm template myapp ./mychart > output.yaml
```

---

## Example Workflow

```bash
# Add stable repository
helm repo add stable https://charts.helm.sh/stable

# Update repositories
helm repo update

# Install nginx ingress controller
helm install my-nginx-ingress ingress-nginx/ingress-nginx

# Upgrade release
helm upgrade my-nginx-ingress ingress-nginx/ingress-nginx

# Uninstall release
helm uninstall my-nginx-ingress
```

---

## Important Files in a Chart

| File        | Purpose                                             |
| ----------- | --------------------------------------------------- |
| Chart.yaml  | Metadata about the chart (name, version, etc).      |
| values.yaml | Default configuration values.                       |
| templates/  | Directory containing Kubernetes manifest templates. |

---

## Useful Flags

| Flag        | Description                                               |
| ----------- | --------------------------------------------------------- |
| `--set`     | Override values inline (e.g., `--set key=value`).         |
| `-f`        | Specify a custom values file (e.g., `-f my-values.yaml`). |
| `--dry-run` | Simulate install/upgrade without applying changes.        |
| `--debug`   | Enable verbose output.                                    |

---

## Notes

* Helm 3 does not require Tiller (no server-side component).
* Charts can be customized extensively using `values.yaml`.
* Always run `helm repo update` to get the latest chart versions.

---

> **Tip:** For production, always pin specific chart versions instead of using `latest`.

---

## Resources

* [Helm Official Website](https://helm.sh/)
* [ArtifactHub (Chart Repository)](https://artifacthub.io/)


---

# Create a Helm Chart for a Flask App

This guide shows how to create a simple Helm chart for a **Flask** application.

---

## 1. Create a New Chart

```bash
helm create flask-app
```

This will create a folder `flask-app/` with the standard Helm structure.

---

## 2. Customize Chart.yaml

Edit `flask-app/Chart.yaml`:

```yaml
apiVersion: v2
name: flask-app
description: A simple Flask application
version: 0.1.0
appVersion: "1.0"
```

---

## 3. Customize values.yaml

Edit `flask-app/values.yaml`:

```yaml
replicaCount: 1

image:
  repository: your-dockerhub-username/flask-app
  pullPolicy: IfNotPresent
  tag: "latest"

service:
  type: ClusterIP
  port: 5000

resources: {}

nodeSelector: {}

```

---

## 4. Customize templates/deployment.yaml

Focus on the container port `5000` (Flask default):

```yaml
containers:
- name: {{ .Chart.Name }}
  image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
  ports:
  - containerPort: 5000
```

---

## 5. Deploy the Chart

```bash
helm install flask-app ./flask-app
```

Check resources:

```bash
kubectl get all
```

---

## 6. Upgrade / Uninstall

To upgrade:

```bash
helm upgrade flask-app ./flask-app
```

To uninstall:

```bash
helm uninstall flask-app
```

---

## Summary

| Command                 | Purpose                             |
| ----------------------- | ----------------------------------- |
| `helm create flask-app` | Create a new Helm chart             |
| `helm install`          | Deploy the app on Kubernetes        |
| `helm upgrade`          | Update the deployed release         |
| `helm uninstall`        | Remove the release from the cluster |


