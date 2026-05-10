# Add new PrometheusRule
* Search for `PrometheusRule` in API Explore -> add new instance
## Example Rule for Minio PVC 
```
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
