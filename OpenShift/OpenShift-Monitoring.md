# Monitoring
## [Enable User Workload Monitoring](https://docs.redhat.com/en/documentation/openshift_container_platform/4.20/html/monitoring/configuring-user-workload-monitoring)

---

## Edit the `cluster-monitoring-config` `ConfigMap` object:

```bash
oc -n openshift-monitoring edit configmap cluster-monitoring-config
```
Add `enableUserWorkload: true` under `data/config.yaml`:
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: cluster-monitoring-config
  namespace: openshift-monitoring
data:
  config.yaml: |
    enableUserWorkload: true 
```

---

## Enable alerts custom
```yaml
alertmanager:
  enabled: true
  nodeSelector:
    node-role.kubernetes.io/infra: ""
  tolerations:
  - key: "node-role.kubernetes.io/infra"
    operator: "Exists"
    effect: "NoSchedule"
```

---

# Verify 
```bash
oc -n openshift-user-workload-monitoring get pod
```
```text
NAME                                   READY   STATUS        RESTARTS   AGE
prometheus-operator-6f7b748d5b-t7nbg   2/2     Running       0          3h
prometheus-user-workload-0             4/4     Running       1          3h
prometheus-user-workload-1             4/4     Running       1          3h
thanos-ruler-user-workload-0           3/3     Running       0          3h
thanos-ruler-user-workload-1           3/3     Running       0          3h
```

---

# [Integrating Openshift Prometheus with Grafana Dashboards](https://github.com/Saeed7596/DevOps/blob/main/OpenShift/Integrating-Openshift-Prometheus-with-Grafana-Dashboards.md)
# [Link](https://shonpaz.medium.com/monitor-your-application-metrics-using-the-openshift-monitoring-stack-862cb4111906)
# [Link](https://medium.com/@theodor2311/get-started-with-openshift-monitoring-for-user-defined-projects-b46351b15ad7)
### Monitoring for User-Defined Projects: (Monitoring Your app Metrics)
1. Telling Prometheus Where To Scrape  
In Openshift, if we want to central Prometheus to scrape metrics from a specific target, we can create a `ServiceMonitor` object, that will tell Prometheus how it should access the exporter service.
```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  labels:
    k8s-app: prometheus-demo
  name: prometheus-demo
spec:
  endpoints:
  - interval: 30s
    path: /metrics
    targetPort: 8080
    scheme: http
  selector:
    matchLabels:
      app: prometheus-demo
```
Now, make sure that you see it in your Openshift Console, by navigating to `Observe` --> `Targets`:  
As you can see, its status is `Up`, and it points to our pod using the exporter service that we have provided.

2. Viewing Your Metrics  
To review your metrics, you can go to `Observe -> Metrics`, this is accessible from both Administrator and Developer view. In this tab, you can choose “Custom query” and use the Prometheus query syntax `PormQL` to query your metrics.  
For example, you can use the following PromQL syntax to get the metrics we created earlier.
```bash
sum(rate(http_requests_total{method="GET"}[1m]))
```
3. Add Prometheus as a Data Source:
  * In the Grafana UI, go to `Configuration -> Data Sources -> Add Data Source`.
  * Select `Prometheus` from the list of data sources.
  * URL: Use the `Thanos Querier` route (e.g., https://thanos-query-k8s-openshift-monitoring.apps.example.com).
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

---

# Add new PrometheusRule
* Search for `PrometheusRule` in API Explore -> add new instance
## Example Rule for Minio PVC 

```yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: minio-storage-alerts
  namespace: openshift-monitoring
spec:
  groups:
  - name: minio.rules
    rules:
    - alert: MinioPVCFillingUp
      expr: |
        (
          kubelet_volume_stats_used_bytes{persistentvolumeclaim="minio-home-claim", namespace="minio"}
          /
          kubelet_volume_stats_capacity_bytes{persistentvolumeclaim="minio-home-claim", namespace="minio"}
        ) > 0.8
      for: 10m
      labels:
        severity: warning
      annotations:
        summary: "MinIO PVC usage > 80%"
        description: "PVC minio-home-claim is above 80% utilization"

    - alert: MinioPVCAlmostFull
      expr: |
        (
          kubelet_volume_stats_used_bytes{persistentvolumeclaim="minio-home-claim", namespace="minio"}
          /
          kubelet_volume_stats_capacity_bytes{persistentvolumeclaim="minio-home-claim", namespace="minio"}
        ) > 0.95
      for: 5m
      labels:
        severity: critical
      annotations:
        summary: "MinIO PVC almost full (>95%)"
        description: "Immediate action required"
```
