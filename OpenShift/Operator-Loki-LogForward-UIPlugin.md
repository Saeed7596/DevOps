# [Loki Operator](https://docs.redhat.com/en/documentation/openshift_container_platform/4.17/html/logging/index)

[Quickstart](https://www.opensourcerers.org/2025/07/21/openshift-logging-a-quickstart-guide-with-loki-stack/)

[Github rbaumgar Openshift Logging](https://github.com/rbaumgar/openshift-logging/blob/main/README.md)

---

# 1. Install Loki Operator

# 2. Install MinIO for OpenShift Logging

2.1. Create a New MinIO Project
```bash
MINIO_NAMESPACE=minio
oc new-project $MINIO_NAMESPACE
```
2.2 Create minio admin password
```bash
MINIO_ADMIN_PWD=`openssl rand -base64 12`
```
```bash
cat <<EOF | oc apply -f -
apiVersion: v1
kind: Secret
type: Opaque
metadata:
  annotations: {}
  name: minio-access-secrets
  namespace: minio
stringData:
  minioPassword: $MINIO_ADMIN_PWD
  minioUser: minio
  minioConsoleAddress: ":44645"
EOF
```
2.3 Create PVC
```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  labels:
    app.kubernetes.io/name: minio
  name: minio-home-claim
  namespace: minio
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 500Gi
  storageClassName: thin-csi
---
kind: PersistentVolumeClaim
apiVersion: v1
metadata:
  labels:
    app.kubernetes.io/name: minio
  name: minio-config-claim
  namespace: minio
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi
```
2.4 Create Service
```yaml
apiVersion: v1
kind: Service
metadata:
  labels:
    app.kubernetes.io/name: minio
  name: minio
  namespace: minio
spec:
  type: NodePort
  selector:
    app.kubernetes.io/name: minio
  ports:
    - name: web
      port: 9000
      targetPort: 9000
    - name: console
      port: 44645
      targetPort: 44645
```
2.5 Create Deployment
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    app.kubernetes.io/name: minio
  name: minio-server
  namespace: minio
spec:
  selector:
    matchLabels:
      app.kubernetes.io/name: minio
  template:
    metadata:
      labels:
        app.kubernetes.io/name: minio
    spec:
      containers:
        - name: minio
          env:
            - name: MINIO_ROOT_USER
              valueFrom:
                secretKeyRef:
                  name: minio-access-secrets
                  key: minioUser
            - name: MINIO_ROOT_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: minio-access-secrets
                  key: minioPassword
            - name: MINIO_CONSOLE_ADDRESS
              valueFrom:
                secretKeyRef:
                  name: minio-access-secrets
                  key: minioConsoleAddress     
          image: quay.io/minio/minio:latest
          args:
            - server
            - /data
          ports:
            - containerPort: 9000
              protocol: TCP
              name: web
          volumeMounts:
            - name: home
              mountPath: /data
            - name: config
              mountPath: /root/.minio
      volumes:
        - name: home
          persistentVolumeClaim:
            claimName: minio-home-claim
        - name: config
          persistentVolumeClaim:
            claimName: minio-config-claim
```
2.6 Create Route
```yaml
apiVersion: route.openshift.io/v1
kind: Route
metadata:
  labels:
    app.kubernetes.io/name: minio
  name: minio-console
  namespace: minio
spec:
  port:
    targetPort: 44645
  tls:
    termination: edge
  to:
    kind: Service
    name: minio
    weight: 100
  wildcardPolicy: None
---
apiVersion: route.openshift.io/v1
kind: Route
metadata:
  labels:
    app.kubernetes.io/name: minio
  name: minio-server
  namespace: minio
spec:
  port:
    targetPort: 9000
  tls:
    termination: edge
  to:
    kind: Service
    name: minio
    weight: 100
  wildcardPolicy: None
```
2.7. Verify
```bash
oc get pod
```
```txt
NAME                           READY   STATUS    RESTARTS   AGE
minio-server-cf8c6c9c4-cvwwv   1/1     Running   0          3d2h
```
```bash
oc logs deployments/minio-server -n minio
```
```txt
INFO: WARNING: MINIO_ACCESS_KEY and MINIO_SECRET_KEY are deprecated.
         Please use MINIO_ROOT_USER and MINIO_ROOT_PASSWORD
MinIO Object Storage Server
Copyright: 2015-2025 MinIO, Inc.
License: GNU AGPLv3 - https://www.gnu.org/licenses/agpl-3.0.html
Version: RELEASE.2024-12-18T13-15-44Z (go1.23.4 linux/amd64)

API: http://10.128.4.14:9000  http://127.0.0.1:9000 
WebUI: http://10.128.4.14:44645 http://127.0.0.1:44645   

Docs: https://docs.min.io
```
2.8 Create a `bucket` and `user` for the `Lokistack`
```bash
BUCKET=openshift-logging 
# create loki user secret
BUCKET_SECRET=`openssl rand -base64 12`

# Create an alias for the connection
oc rsh deployments/minio-server mc alias set myminio http://localhost:9000 minio $MINIO_ADMIN_PWD
# Output: Added `myminio` successfully.

# Create an access-policy file
$ cat >bucket-access-policy.json <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
             "Action": ["s3:*"],
             "Effect": "Allow",
             "Resource": ["arn:aws:s3:::${BUCKET}",
                          "arn:aws:s3:::${BUCKET}/*"]
        }
    ]
}
EOF

# copy policy file to pod
$ cat bucket-access-policy.json | \
  oc exec deployments/minio-server -i -- sh -c "cat /dev/stdin > /tmp/bucket-access-policy.json"

# create new policy
oc rsh deployments/minio-server \
         mc admin policy create myminio $BUCKET-access-policy /tmp/bucket-access-policy.json

# Output: Created policy `openshift-logging-access-policy` successfully.

# cleanup: remove policy file
$ oc rsh deployments/minio-server rm /tmp/bucket-access-policy.json
$ rm bucket-access-policy.json

# (optional) create list all policies
$ oc rsh deployments/minio-server \
         mc admin policy ls myminio
readonly
readwrite
writeonly
consoleAdmin
diagnostics
openshift-logging-access-policy

# create openshift-logging bucket
$ oc rsh deployments/minio-server \
         mc mb myminio/$BUCKET
Bucket created successfully `myminio/openshift-logging`.

# (optional) list all buckets
$ oc rsh deployments/minio-server \
         mc ls myminio
[2025-01-09 11:28:51 UTC]     0B openshift-logging/

# create user
$ oc rsh deployments/minio-server \
         mc admin user add myminio $BUCKET $BUCKET_SECRET
Added user `loki-user` successfully.

# (optional) list all users
$ oc rsh deployments/minio-server \
         mc admin user ls myminio
enabled    loki-user

# attach openshift-logging-acccess-policy to user openshift-logging
$ oc rsh deployments/minio-server \
         mc admin policy attach myminio $BUCKET-access-policy --user $BUCKET
Attached Policies: [openshift-logging-access-policy]
To User: openshift-logging

# (optional) if you want displays information on a MinIO server
$ oc rsh deployments/minio-server \
         mc admin info myminio
●  localhost:9000
   Uptime: 1 week 
   Version: 2024-12-18T13:15:44Z
   Network: 1/1 OK 
   Drives: 1/1 OK 
   Pool: 1

┌──────┬────────────────────────┬─────────────────────┬──────────────┐
│ Pool │ Drives Usage           │ Erasure stripe size │ Erasure sets │
│ 1st  │ 95.3% (total: 750 GiB) │ 1                   │ 1            │
└──────┴────────────────────────┴─────────────────────┴──────────────┘

16 GiB Used, 2 Buckets, 18,610 Objects
1 drive online, 0 drives offline, EC:0 

# cleanup: remove the alias for the connection
$ oc rsh deployments/minio-server \
         mc alias remove myminio
Removed `myminio` successfully.
```
NOTE:
* The configuration of the MinIO server is not HA. There is also a MinIO operator available.

* If you have networkpolicies in use, allow the project openshift-logging access to the project minio on port 9000.

2.9 Create a Secret for Loki
* [Create an Object Storage secret with keys as follows:](https://loki-operator.dev/docs/object_storage.md/#minio)

* If you use a different object store, you should define the secret differently. [See](https://github.com/grafana/loki/blob/main/operator/docs/lokistack/object_storage.md)

Loki requires a secret to define how to access the MinIO object store.
```bash
kubectl create secret generic lokistack-dev-minio \
  --from-literal=bucketnames="<BUCKET_NAME>" \
  --from-literal=endpoint="<MINIO_BUCKET_ENDPOINT>" \
  --from-literal=access_key_id="<MINIO_ACCESS_KEY_ID>" \
  --from-literal=access_key_secret="<MINIO_ACCESS_KEY_SECRET>"
```bash
kubectl create secret generic lokistack-loki-s3 -n openshift-logging\
          --from-literal=bucketnames="openshift-logging" \
          --from-literal=endpoint="http://minio.$MINIO_NAMESPACE.svc:9000" \
          --from-literal=access_key_id="$BUCKET" \
          --from-literal=access_key_secret="$BUCKET_SECRET"
```
2.10. Uninstall MinIO
```bash
oc delete ns $MINIO_NAMESPACE 
```

---  

# 3. Configure LokiStack
```yaml
apiVersion: loki.grafana.com/v1
kind: LokiStack
metadata:
  name: lokistack-example
  namespace: openshift-logging
  labels:
    app: logging
spec:
  hashRing:
    type: memberlist
  limits:
    global:
      ingestion:
        ingestionBurstSize: 16
      queries:
        queryTimeout: 3m
      retention: 
        days: 180
  managementState: Managed
  size: 1x.small
  storage:
    schemas:
      - effectiveDate: '2026-02-21'
        version: v13
    secret:
      name: lokistack-loki-s3
      type: s3
  storageClassName: thin-csi
  template:
    compactor:
      nodeSelector:
        node-role.kubernetes.io/infra: ''
      tolerations:
        - effect: NoSchedule
          key: node-role.kubernetes.io/infra
    distributor:
      nodeSelector:
        node-role.kubernetes.io/infra: ''
      tolerations:
        - effect: NoSchedule
          key: node-role.kubernetes.io/infra
    gateway:
      nodeSelector:
        node-role.kubernetes.io/infra: ''
      tolerations:
        - effect: NoSchedule
          key: node-role.kubernetes.io/infra
    indexGateway:
      nodeSelector:
        node-role.kubernetes.io/infra: ''
      tolerations:
        - effect: NoSchedule
          key: node-role.kubernetes.io/infra
    ingester:
      nodeSelector:
        node-role.kubernetes.io/infra: ''
      tolerations:
        - effect: NoSchedule
          key: node-role.kubernetes.io/infra
    querier:
      nodeSelector:
        node-role.kubernetes.io/infra: ''
      tolerations:
        - effect: NoSchedule
          key: node-role.kubernetes.io/infra
    queryFrontend:
      nodeSelector:
        node-role.kubernetes.io/infra: ''
      tolerations:
        - effect: NoSchedule
          key: node-role.kubernetes.io/infra
    ruler:
      nodeSelector:
        node-role.kubernetes.io/infra: ''
      tolerations:
        - effect: NoSchedule
          key: node-role.kubernetes.io/infra
  tenants:
    mode: openshift-logging
```

---

# Configure the ClusterLogForwarder for LokiStack
In order to have the logs correctly routed to Loki, we need to configure the OpenShift ClusterLogForwarder appropriately, by doing each of these steps:
```bash
$ oc project openshift-logging
$ oc create sa collector
serviceaccount/collector created

$ oc adm policy add-cluster-role-to-user cluster-logging-write-application-logs -z collector 
clusterrole.rbac.authorization.k8s.io/cluster-logging-write-application-logs added: "collector"

$ oc adm policy add-cluster-role-to-user cluster-logging-write-audit-logs -z collector
clusterrole.rbac.authorization.k8s.io/cluster-logging-write-audit-logs added: "collector"

$ oc adm policy add-cluster-role-to-user cluster-logging-write-infrastructure-logs -z collector
clusterrole.rbac.authorization.k8s.io/cluster-logging-write-infrastructure-logs added: "collector"

$ oc adm policy add-cluster-role-to-user collect-application-logs -z collector
clusterrole.rbac.authorization.k8s.io/collect-application-logs added: "collector"

$ oc adm policy add-cluster-role-to-user collect-audit-logs -z collector
clusterrole.rbac.authorization.k8s.io/collect-audit-logs added: "collector"

$ oc adm policy add-cluster-role-to-user collect-infrastructure-logs -z collector
clusterrole.rbac.authorization.k8s.io/collect-infrastructure-logs added: "collector"

$ oc apply -f operators/logging/clusterlogforwarder.yaml
clusterlogforwarder.observability.openshift.io/collector created
```
You only need to apply the roles for your required log types (application, audit, and infrastructure).
```bash
$ oc get clusterlogforwarders.observability.openshift.io collector --template='{{printf "%-55s %7s %-30sn" "Type" "Status" "Reason/Message"}}{{range .status.conditions}}{{printf "%-55s %7s %s/%sn" .type .status .reason .message}}{{end}}'
Type                                                     Status Reason/Message                
observability.openshift.io/ValidLokistackOTLPOutputs       True ValidationSuccess/
observability.openshift.io/Authorized                      True ClusterRolesExist/permitted to collect log types: [application audit infrastructure]
observability.openshift.io/Valid                           True ValidationSuccess/
Ready                                                      True ReconciliationComplete/

# InputConditions
$ oc get clusterlogforwarders.observability.openshift.io collector --template='{{printf "%-55s %7s %-30sn" "Type" "Status" "Reason/Message"}}{{range .status.inputConditions}}{{printf "%-55s %7s %s/%sn" .type .status .reason .message}}{{end}}'
Type                                                     Status Reason/Message                
observability.openshift.io/ValidInput-application          True ValidationSuccess/input "application" is valid
observability.openshift.io/ValidInput-infrastructure       True ValidationSuccess/input "infrastructure" is valid
observability.openshift.io/ValidInput-audit                True ValidationSuccess/input "audit" is valid

# OutputConditions
$ oc get clusterlogforwarders.observability.openshift.io collector --template='{{printf "%-72s %7s %-30sn" "Type" "Status" "Reason/Message"}}{{range .status.outputConditions}}{{printf "%-72s %7s %s/%sn" .type .status .reason .message}}{{end}}'
Type                                                                      Status Reason/Message                
observability.openshift.io/ValidOutput-default-lokistack-application        True ValidationSuccess/output "default-lokistack-application" is valid
observability.openshift.io/ValidOutput-default-lokistack-audit              True ValidationSuccess/output "default-lokistack-audit" is valid
observability.openshift.io/ValidOutput-default-lokistack-infrastructure     True ValidationSuccess/output "default-lokistack-infrastructure" is valid

# PipelineCondition
$ oc get clusterlogforwarders.observability.openshift.io collector --template='{{printf "%-57s %7s %-30sn" "Type" "Status" "Reason/Message"}}{{range .status.pipelineConditions}}{{printf "%-57s %7s %s/%sn" .type .status .reason .message}}{{end}}'

$ oc get daemonsets.apps collector
NAME        DESIRED   CURRENT   READY   UP-TO-DATE   AVAILABLE   NODE SELECTOR            AGE
collector   6         6         6       6            6           kubernetes.io/os=linux   5d23h

$ oc get pod -l app.kubernetes.io/instance=collector
NAME              READY   STATUS    RESTARTS   AGE
collector-588b9   1/1     Running   0          3d19h
collector-88vc5   1/1     Running   0          3d19h
collector-bpj84   1/1     Running   0          3d19h
collector-fnbgr   1/1     Running   0          3d19h
collector-s858j   1/1     Running   0          3d19h
collector-scv4z   1/1     Running   0          3d19h
```

---

# [ClusterLogForwarder](https://docs.redhat.com/en/documentation/red_hat_openshift_logging/6.3/html/configuring_logging/configuring-log-forwarding#logging-forward-splunk-http-event-collector_configuring-log-forwarding) 

# Other Helpful Links:
* [OpenShift Log Forwarding to Splunk](https://community.splunk.com/t5/Dashboards-Visualizations/OpenShift-Log-Forwarding-to-Splunk/m-p/635672)

```bash
oc -n openshift-logging create secret generic vector-splunk-secret --from-literal hecToken=<HEC_Token>
```
```yaml
apiVersion: observability.openshift.io/v1
kind: ClusterLogForwarder
metadata:
  name: collector
  namespace: openshift-logging
spec:
  collector:
    tolerations:
      - effect: NoSchedule
        key: node-role.kubernetes.io/infra
    filters:
      - drop:
          - test: 
            - field: .log_type
              notMatches: ^application$
        name: keep-app-logs
        type: drop
      - drop:
          - test: 
            - field: .kubernetes.namespace
              notMatches: ^(wallet|wallet-samt)$
        name: keep-wallet-namespaces
        type: drop
      - drop:
          - test: 
            - field: .kubernetes.pod_name
              matches: ^dispatcher$
            - field: .message
              notMatches: '"type"\s*:\s*"DISPATCHER_LOG"'
        name: keep-dispatcher-logs
        type: drop
      - drop:
          - test: 
            - field: .level
              matches: ^(INFO|DEBUG|WARN|UNKNOWN)$
            - field: .severity
              matches: ^(INFO|DEBUG|WARN|UNKNOWN)$
            - field: .structured.level
              matches: ^(INFO|DEBUG|WARN|UNKNOWN)$
        name: drop-log-level-severity
        type: drop
  managementState: Managed
  outputs:
    - lokiStack:
        authentication:
          token:
            from: serviceAccount
        target:
          name: lokistack-example
          namespace: openshift-logging
      name: default-lokistack
      tls:
        ca:
          configMapName: openshift-service-ca.crt
          key: service-ca.crt
      type: lokiStack
    - name: splunk-receiver
      splunk:
        authentication:
          token:
            key: hecToken
            secretName: vector-splunk-secret
        url: https://172.26.103.203:8088
      tls:
        insecureSkipVerify: true
      type: splunk
  pipelines:
    - filterRefs:
        - keep-app-logs
        - keep-wallet-namespaces
        - keep-dispatcher-logs
        - drop-log-level-severity
      inputRefs:
        - application
        - audit
        - infrastructure
      name: default-logstore
      outputRefs:
        - default-lokistack
    - inputRefs:
        - infrastructure
        - audit
      name: splunk-logstore
      outputRefs:
        - splunk-receiver
  serviceAccount:
    name: collector
```

---

# Install the Cluster Observability Operator
UI Plugin
```yaml
apiVersion: observability.openshift.io/v1alpha1
kind: UIPlugin
metadata:
  name: logging
spec:
  deployment:
    nodeSelector:
      node-role.kubernetes.io/infra: ''
    tolerations:
      - effect: NoSchedule
        key: node-role.kubernetes.io/infra
  logging:
    lokiStack:
      name: lokistack-example
  type: Logging
```
