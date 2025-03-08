# Helm
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
## Install
```bash
curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3
chmod 700 get_helm.sh
./get_helm.sh
```
```bash
helm help
helm version

helm search [subcommand] [keyword]
# [subcommmand] One of the following two options:
# 1- Repo: Search in the Helm tanks you've added earlier.
# 2- HUB: Search in Helm Hub, which contains a set of Helm general tanks.
# [Keyword]: The name of the chart or the word you want to search.
helm search repo nginx
helm search hub nginx
helm search hub consul | grep hashicorp

helm repo list
helm repo ls
helm repo add <repo-name> <repo-url>
# repo-name: The custom name you set for the repository.
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update <repo-name> -n <namespace-name>

helm repo remove <repo_name>
helm repo rm <repo_name>
helm repo rm bitnami

helm install <release-name> bitnami/apache # install Chart
helm install amaze-surf bitnami/apache

helm list # Show installed <release-name>
helm ls -A
helm ls -n <namespace-name>
helm uninstall <release-name>

helm history <release-name>

helm upgrade <release-name> <chart-name> [flags]
helm upgrade dazzling-web bitnami/nginx --version 18.3.6

helm rollback <release-name>
helm rollback dazzling-web
```
