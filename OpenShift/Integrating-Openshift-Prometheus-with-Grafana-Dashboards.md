# [Integrating Openshift Prometheus with Grafana Dashboards](https://medium.com/@peaceworld.abbas/integrating-openshift-prometheus-with-grafana-dashboards-ba45ddc9239e)

---

## Step 1: Create `cluster-monitonig-config` configMaps

Check `cluster-monitonig-config` configMaps in `openshift-monitoring` namespace: 
* [Doc](https://docs.redhat.com/en/documentation/openshift_container_platform/4.20/html/monitoring/configuring-user-workload-monitoring)
```yaml
data:
  config.yaml: |
    enableUserWorkload: true
```

---

## Step 2: Create Secret Based Token
```bash
nano secret-base-token.yaml
```
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: prometheus-robot-secret
  namespace: openshift-monitoring
  annotations:
    kubernetes.io/service-account.name: prometheus-k8s
type: kubernetes.io/service-account-token
```
```bash
oc apply -f secret-base-token.yaml
```

---

## Step 3: Obtain Prometheus Route and Credentials
```bash
oc get routes -n openshift-monitoring
```
This will give you the Prometheus URL (e.g., `https://prometheus-k8s-openshift-monitoring.apps.example.com`).

---

## Step 4: Get Bearer Token for authentication:
```bash
oc get sa -n openshift-monitoring
```
```bash
oc create token prometheus-k8s -n openshift-monitoring
```

---

## Step 5: Add Prometheus as a Data Source:
* In the Grafana UI, go to `Configuration -> Data Sources -> Add Data Source`.
* Select `Prometheus` from the list of data sources.
* URL: Use the Prometheus route obtained earlier (e.g., https://prometheus-k8s-openshift-monitoring.apps.example.com).
* Authentication:
* Choose `Forward OAuth Identity as the authentication` method
* TLS/SSL Settings:
  * Enable `Skip TLS Certificate Validation` if you’re using `self-signed` certificates for Prometheus in your cluster.
* On HTTP Headers, add Header:
  * Fill in the Header with `Authorization`
* Fill in the value with the output of this following command.
```bash
TOKEN=$(oc -n openshift-monitoring extract secret/prometheus-robot-secret --to=- --keys=token)

echo "Bearer $TOKEN"
```
