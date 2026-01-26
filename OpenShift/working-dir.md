# Mirrored Configuration
```bash
cd ocp4-18/working-dir/cluster-resources/

ls
cc-redhat-operator-index-v4-18.yaml
cs-redhat-operator-index-v4-18.yaml
idms-oc-mirror.yaml
itms-oc-mirror.yaml
signature-configmap.json
signature-configmap.yaml
updateService.yaml
```

---

```bash
cat cc-redhat-operator-index-v4-18.yaml 
```
```yaml
apiVersion: olm.operatorframework.io/v1
kind: ClusterCatalog
metadata:
  name: cc-redhat-operator-index-v4-18
spec:
  priority: 0
  source:
    image:
      ref: registry.example.com/redhat/redhat-operator-index:v4.18
    type: Image
status: {}
```

---

```bash
cat cs-redhat-operator-index-v4-18.yaml 
```
```yaml
apiVersion: operators.coreos.com/v1alpha1
kind: CatalogSource
metadata:
  name: cs-redhat-operator-index-v4-18
  namespace: openshift-marketplace
spec:
  image: registry.example.com/redhat/redhat-operator-index:v4.18
  sourceType: grpc
status: {}
```

---

```bash
cat idms-oc-mirror.yaml 
```
```yaml
---
apiVersion: config.openshift.io/v1
kind: ImageDigestMirrorSet
metadata:
  name: idms-release-0
spec:
  imageDigestMirrors:
  - mirrors:
    - registry.example.com/openshift/release
    source: quay.io/openshift-release-dev/ocp-v4.0-art-dev
  - mirrors:
    - registry.example.com/openshift/release-images
    source: quay.io/openshift-release-dev/ocp-release
status: {}
---
apiVersion: config.openshift.io/v1
kind: ImageDigestMirrorSet
metadata:
  name: idms-operator-0
spec:
  imageDigestMirrors:
  - mirrors:
    - registry.example.com/openshift-service-mesh
    source: registry.redhat.io/openshift-service-mesh
  - mirrors:
    - registry.example.com/openshift-gitops-1
    source: registry.redhat.io/openshift-gitops-1
  - mirrors:
    - registry.example.com/openshift4
    source: registry.redhat.io/openshift4
  - mirrors:
    - registry.example.com/network-observability
    source: registry.redhat.io/network-observability
  - mirrors:
    - registry.example.com/rhel9
    source: registry.redhat.io/rhel9
  - mirrors:
    - registry.example.com/openshift-logging
    source: registry.redhat.io/openshift-logging
  - mirrors:
    - registry.example.com/cluster-observability-operator
    source: registry.redhat.io/cluster-observability-operator
status: {}
```

---

```bash
cat itms-oc-mirror.yaml 
```
```yaml
---
apiVersion: config.openshift.io/v1
kind: ImageTagMirrorSet
metadata:
  name: itms-operator-0
spec:
  imageTagMirrors:
  - mirrors:
    - registry.example.com/openshift4
    source: registry.redhat.io/openshift4
status: {}
---
apiVersion: config.openshift.io/v1
kind: ImageTagMirrorSet
metadata:
  name: itms-release-0
spec:
  imageTagMirrors:
  - mirrors:
    - registry.example.com/openshift/release-images
    source: quay.io/openshift-release-dev/ocp-release
status: {}
```

---

```bash
cat signature-configmap.json 
```
```json
{"kind":"ConfigMap","apiVersion":"v1","metadata":{"name":"mirrored-release-signatures","namespace":"openshift-config-managed","labels":{"release.openshift.io/verification-signatures":""}},"binaryData":{"sha256-5e06105a6ba80d04eb5d8d3f9a672fb743ce4710876d99a375c2d9f7b7eaa783-1":"owGbwMvMwMEoOU9/4l9n2UDG0wf6khgyiqzlq5WSizJLMpMTc5SsFKqVMnMT01PBrJT85OzUIt3cxLzMtNTiEt2UzHQgBZRSKs5INDI1szJNNTAzNDBNNEtKtDBIMTBJTTJNsUgxTrNMNDM3SksyNzFOTjUxNzSwMDdLsbRMNDY3TTZKsUwzTzJPTUw0tzBWqtVRUCqpLABZp5RYkp+bmayQnJ9XkpiZl1qkUJyZnpdYUlqUqgRUlZmSmleSWVKJ7LCi1LTUotS8ZLD2wtLESr3MfP38gtS84ozMtBKgdE5qYnGqbkpqmX5+cgGMb2WiZ2ihZ2SgW2FhFm9molQLckR+QUlmfh40BJKLUoGOKQKZGpSaouCRWKLgDzQ1GGSqQjDQVZl56QqOpSUZ+cBwq1Qw0DPQMwQa08kkw8LAyMHAxsoECl..."}}
```
```bash
cat signature-configmap.yaml 
```
```yaml
apiVersion: v1
binaryData:
  sha256-5e06105a6ba80d04eb5d8d3f9a672fb743ce4710876d99a375c2d9f7b7eaa783-1: owGbwMvMwMEoOU9/4l9n2UDG0wf6khgyiqzlq5WSizJLMpMTc5SsFKqVMnMT01PBrJT85OzUIt3cxLzMtNTiEt2UzHQgBZRSKs5INDI1szJNNTAzNDBNNEtKtDBIMTBJTTJNsUgxTrNMNDM3SksyNzFOTjUxNzSwMDdLsbRMNDY3TTZKsUwzTzJPTUw0tzBWqtVRUCqpLABZp5RYkp+bmayQnJ9XkpiZl1qkUJyZnpdYUlqUqgRUlZmSmleSWVKJ7LCi1LTUotS8ZLD2wtLESr3MfP38gtS84ozMtBKgdE5qYnGqbkpqmX5+cgGMb2WiZ2ihZ2SgW2FhFm9molQLckR+QUlmfh40BJKLUoGOKQKZGpSaouCRWKLgDzQ1GGSqQjDQVZl56QqOpSUZ+cBwq1Qw0DPQMwQa08kkw8LAyMHAxsoECl...
kind: ConfigMap
metadata:
  labels:
    release.openshift.io/verification-signatures: ""
  name: mirrored-release-signatures
  namespace: openshift-config-managed
```
