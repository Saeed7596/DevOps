# [Update Path](https://access.redhat.com/labs/ocpupgradegraph/update_path)
Use this link to figure the next available version. Find your update path.

---

# [Updating a cluster in a disconnected environment](https://docs.redhat.com/en/documentation/openshift_container_platform/4.18/html/disconnected_environments/updating-a-cluster-in-a-disconnected-environment)


**Important**:  
If you installed an earlier version of `oc`, you cannot use it to complete all of the commands in OpenShift Container Platform.  
Download and install the new version of `oc`. If you are updating a cluster in a disconnected environment, install the `oc` version that you plan to update to.

---

# Mirroring resources using the oc-mirror plugin
See [Mirroring images for a disconnected installation by using the oc-mirror plugin v2](https://docs.redhat.com/en/documentation/openshift_container_platform/4.18/html/disconnected_environments/about-installing-oc-mirror-v2) for additional details. 

## Generate ImageSet Config
Find operator channel and release information
```bash
oc mirror list operators --catalogs --version=4.18
```
* **Note**: Add `graph: true` to build and push the graph-data image to the mirror registry. The graph-data image is required to create **OpenShift Update Service (OSUS)**. The `graph: true` field also generates the `UpdateService` custom resource manifest. The `oc` command-line interface (CLI) can use the `UpdateService` custom resource manifest to create OSUS. For more information, see About the OpenShift Update Service.

oc-mirror v2 with operator Sample:
```yaml
kind: ImageSetConfiguration
apiVersion: mirror.openshift.io/v2alpha1
mirror:
  platform:
    channels:
    - name: stable-4.18
      type: ocp
      minVersion: 4.18.30
      maxVersion: 4.18.30
    graph: true
  operators:
  - catalog: registry.redhat.io/redhat/redhat-operator-index:v4.18
    packages:
    - name: cincinnati-operator
      channels:
      - name: v1
    - name: cluster-logging 
      channels:
      - name: stable-6.2
    - name: cluster-observability-operator 
      channels:
      - name: stable
    - name: container-security-operator
      channels:
      - name: stable-3.14
    - name: devspaces
      channels:
      - name: stable
    - name: devworkspace-operator
      channels:
      - name: fast
    - name: file-integrity-operator
      channels:
      - name: stable
    - name: jaeger-product
      channels:
      - name: stable
    - name: kiali-ossm
      channels:
      - name: stable
    - name: kubevirt-hyperconverged
      channels:
      - name: stable
    - name: loki-operator 
      channels:
      - name: stable-6.2
    - name: netobserv-operator 
      channels:
      - name: stable
    - name: openshift-cert-manager-operator
      channels:
      - name: stable-v1
    - name: openshift-gitops-operator
      channels:
      - name: latest
    - name: opentelemetry-product 
      channels:
      - name: stable
    - name: redhat-oadp-operator 
      channels:
      - name: stable-1.4
    - name: servicemeshoperator 
      channels:
      - name: stable
    - name: tempo-product 
      channels:
      - name: stable
  helm: {}
```
1. Save the images as a .tar file:​
```bash
oc mirror --config=./imageset-config.yaml file://local-mirror --v2
```
2. In the disconnected environment, transfer the images to the destination registry
```bash
oc mirror -c <image_set_config_yaml> --from file://<oc_mirror_workspace_path> docker://<mirror_registry_url> --v2

oc mirror -c imageset-config.yaml --from file:///home/<user>/local-mirror/ docker://registry.example.com --v2
```
After you have mirrored your image set to the mirror registry, you must apply the generated `ImageDigestMirrorSet` (IDMS), `ImageTagMirrorSet` (ITMS), `CatalogSource`, and `UpdateService` to the cluster.  
```bash
ls /home/<user>/local-mirror/working-dir/cluster-resources/

cc-redhat-operator-index-v4-18.yaml  cs-redhat-operator-index-v4-18.yaml  idms-oc-mirror.yaml  itms-oc-mirror.yaml  signature-configmap.json  signature-configmap.yaml
```

### **Note**: 
* If wants to apply new **cluster-resources**
* you should keep the old one `/working-dir/cluster-resources/*`
* important file is `ImageDigestMirrorSet` (IDMS) - `idms-oc-mirror.yaml`
* Before apply the new one you should merge it with the old one.
* then apply!
1. Create a backup from old version:
```bash
mkdir -p ~/ocp<version>-backup/cluster-resources

cp -r <path_to_old_oc-mirror_workspace>/working-dir/cluster-resources/* ~/ocp<version>-backup/cluster-resources

cat <path_to_old_oc-mirror_workspace>/working-dir/cluster-resources/idms-oc-mirror.yaml
```
2. Find Diff:
```bash
diff -y ~/ocp<version>-backup/cluster-resourcesidms-oc-mirror.yaml \
     <path_to_new_oc-mirror_workspace>/working-dir/cluster-resources/idms-oc-mirror.yaml
```
3. Merge!
```bash
nano <path_to_new_oc-mirror_workspace>/working-dir/cluster-resources/idms-oc-mirror.yaml
```
4. Apply the new one:
```bash
oc apply -f <path_to_new_oc-mirror_workspace>/working-dir/cluster-resources/
```

---

# Performing a cluster update in a disconnected environment 
You can use one of the following procedures to update a disconnected OpenShift Container Platform cluster:
1. Updating a cluster in a disconnected environment using the OpenShift Update Service
2. Updating a cluster in a disconnected environment without the OpenShift Update Service

---

# 1. Updating a cluster in a disconnected environment using the OpenShift Update Service 
To get an update experience similar to connected clusters, you can use the following procedures to install and configure the **OpenShift Update Service (OSUS)** in a disconnected environment.  
The following steps outline the high-level workflow on how to update a cluster in a disconnected environment using OSUS:

1. Configure access to a secured registry.  
We use root CA while installing the cluster.

2. Update the global cluster pull secret to access your mirror registry.  
You can update the global pull secret for your cluster by either replacing the current pull secret or appending a new pull secret.  
`It's Not Necessary`

3. Install the OSUS Operator.  
Operator Name: `cincinnati-operator:v1`

4. Create a graph data container image for the OpenShift Update Service.  
**Note**: The oc-mirror OpenShift CLI (oc) plugin creates this graph data container image in addition to mirroring release images. If you used the oc-mirror plugin to mirror your release images, you can skip this procedure.  
But I think if you set `graph: true` in image set configuration file.
So maybe need to apply this (if don't use `graph: true`): follow this [link](https://docs.redhat.com/en/documentation/openshift_container_platform/4.18/html/disconnected_environments/updating-a-cluster-in-a-disconnected-environment#update-service-graph-data_updating-disconnected-cluster-osus)  
Summary Steps:
    * Create a Dockerfile 
    * Build graph image 
    * Push graph image

5. Install the OSUS application and configure your clusters to use the OpenShift Update Service in your environment.  
Creating an OpenShift Update Service application by using the web console.   
You can use the OpenShift Container Platform web console to create an OpenShift Update Service application by using the OpenShift Update Service Operator.

    **Prerequisites**
    * The OpenShift Update Service Operator has been installed.
    * The OpenShift Update Service graph data container image has been created and pushed to a repository that is accessible to the OpenShift Update Service.
    * The current release and update target releases have been mirrored to a registry in the disconnected environment.

    **Procedure**
    1. In the web console, click **Operators** > **Installed Operators**.
    2. Choose **OpenShift Update Service** from the list of installed Operators.
    3. Click the **Update Service** tab.
    4. Click **Create UpdateService**.
    5. Enter a name in the **Name** field, for example, `service`.
    6. Enter the local pullspec in the **Graph Data Image** field to the graph data container image created in "Creating the OpenShift Update Service graph data container image", for example, `registry.example.com/openshift/graph-data:latest`.
    7. In the **Releases** field, enter the registry and repository created to contain the release images in "Mirroring the OpenShift Container Platform image repository", for example, `registry.example.com/ocp4/openshift4-release-images`.
    8. Enter `2` in the **Replicas** field.
    9. Click **Create** to create the OpenShift Update Service application.
    10. Verify the OpenShift Update Service application:
        * From the **UpdateServices** list in the **Update Service** tab, click the Update Service application just created.
        * Click the **Resources** tab.
        * Verify each application resource has a status of **Created**.

    **Note**: The policy engine route name must not be more than 63 characters based on RFC-1123. If you see `ReconcileCompleted` status as `false` with the reason `CreateRouteFailed` caused by `host must conform to DNS 1123 naming convention and must be no more than 63 characters`, try creating the Update Service with a shorter name.

---

## Configuring the Cluster Version Operator [(CVO)](https://docs.redhat.com/en/documentation/openshift_container_platform/4.18/html/disconnected_environments/updating-a-cluster-in-a-disconnected-environment#update-service-configure-cvo) 


---

# ✅ 2. Updating a cluster in a disconnected environment without the OpenShift Update Service

## Prerequisites
1. Take a full [etcd backup](https://github.com/Saeed7596/DevOps/blob/main/OpenShift/etcd.md)
2. You have updated all Operators previously installed through Operator Lifecycle Manager (OLM) to a version that is compatible with your target release. Updating the Operators ensures they have a valid update path when the default OperatorHub catalogs switch from the current minor version to the next during a cluster update. See [Updating installed Operators](https://docs.redhat.com/en/documentation/openshift_container_platform/4.18/html-single/operators/#olm-upgrading-operators) for more information on how to check compatibility and, if necessary, update the installed Operators.

# Steps
1. pause MHC
2. upgrade cluster
3. verify MCP Updated
4. unpause MHC

## Pausing a MachineHealthCheck resource 
During the update process, nodes in the cluster might become temporarily unavailable. In the case of worker nodes, the `MachineHealthCheck` resources might identify such nodes as unhealthy and reboot them. **To avoid rebooting** such nodes, pause all the `MachineHealthCheck` resources before updating the cluster.

1. To list all the available `MachineHealthCheck` resources that you want to pause, run the following command:
```bash
oc get machinehealthcheck -n openshift-machine-api
```
2. To pause the machine health checks, add the `cluster.x-k8s.io/paused=""` annotation to the `MachineHealthCheck` resource. Run the following command:
```bash
oc -n openshift-machine-api annotate mhc <mhc-name> cluster.x-k8s.io/paused=""
```
```bash
for m in $(oc get mhc -n openshift-machine-api -o name); do
  oc -n openshift-machine-api annotate $m cluster.x-k8s.io/paused=""
done
```
The annotated `MachineHealthCheck` resource resembles the following YAML file:
```yaml
apiVersion: machine.openshift.io/v1beta1
kind: MachineHealthCheck
metadata:
  name: example
  namespace: openshift-machine-api
  annotations:
    cluster.x-k8s.io/paused: ""
spec:
  selector:
    matchLabels:
      role: worker
  unhealthyConditions:
  - type:    "Ready"
    status:  "Unknown"
    timeout: "300s"
  - type:    "Ready"
    status:  "False"
    timeout: "300s"
  maxUnhealthy: "40%"
status:
  currentHealthy: 5
  expectedMachines: 5
```
#### **Important**
Resume the machine health checks after updating the cluster. To resume the check, remove the pause annotation from the MachineHealthCheck resource by running the following command:
```bash
oc -n openshift-machine-api annotate mhc <mhc-name> cluster.x-k8s.io/paused-
```

## Retrieving a release image digest 
In order to update a cluster in a **disconnected environment** using the `oc adm upgrade` command with the `--to-image` option, you must reference the sha256 digest that corresponds to your targeted release image

1. Run the following command on a device that is connected to the internet:
```bash
oc adm release info -o 'jsonpath={.digest}{"\n"}' quay.io/openshift-release-dev/ocp-release:${OCP_RELEASE_VERSION}-${ARCHITECTURE}
```
For `{OCP_RELEASE_VERSION}`, specify the version of OpenShift Container Platform to which you want to update, such as `4.18.30`.  
For `{ARCHITECTURE}`, specify the architecture of the cluster, such as `x86_64`, `aarch64`, `s390x`, or `ppc64le`.
```bash
oc adm release info -o 'jsonpath={.digest}{"\n"}' quay.io/openshift-release-dev/ocp-release:4.18.x-x86_64
```
Example output
```text
sha256:a8bfba3b6dddd1a2fbbead7dac65fe4fb8335089e4e7cae327f3bad334add31d
```

## ✅ Find your digest in you local registry (**Nexus**)
```bash
cp nexus-ca.pem /etc/pki/ca-trust/source/anchors/
update-ca-trust extract
```
```bash
oc adm release info \
  registry.example.com/openshift/release-images:4.18.0-x86_64 \
  -o 'jsonpath={.digest}{"\n"}'
```
Compare the output with the value of:
```bash
cat /home/<user>/local-mirror/working-dir/cluster-resources/signature-configmap.yaml`
```

2. Copy the sha256 digest for use when updating your cluster.

## Updating the disconnected cluster
#### Prerequisites
* You mirrored the images for the new release to your registry.
* You applied the release image signature ConfigMap for the new release to your cluster.
  ```
  Note
  The release image signature config map allows the Cluster Version Operator (CVO) to ensure the integrity of release images by verifying that the actual image signatures match the expected signatures.
  ```
* You obtained the sha256 digest for your targeted release image.
* You installed the OpenShift CLI (`oc`).
* You paused all `MachineHealthCheck` resources.

#### Procedure

Update the cluster:
```bash
oc adm upgrade --allow-explicit-upgrade --to-image <defined_registry>/<defined_repository>@<digest>
```
Where:  
`<defined_registry>`  
Specifies the name of the mirror registry you mirrored your images to.  
`<defined_repository>`  
Specifies the name of the image repository you want to use on the mirror registry.  
`<digest>`  
Specifies the sha256 digest for the targeted release image, for example, `sha256:81154f5c03294534e1eaf0319bef7a601134f891689ccede5d705ef659aa8c92`.
```bash
oc adm upgrade --allow-explicit-upgrade --to-image=registry.example.com/openshift/release-images@sha256:5e06105a6ba80d04eb5d8d3f9a672fb743ce4710876d99a375c2d9f7b7eaa783 
```

---

Note  
See **"Mirroring OpenShift Container Platform images"** to review how your mirror registry and repository names are defined.  
If you used an `ImageContentSourcePolicy` or `ImageDigestMirrorSet`, you can use the canonical registry and repository names instead of the names you defined. The canonical registry name is `quay.io` and the canonical repository name is `openshift-release-dev/ocp-release`.  
You can only configure global pull secrets for clusters that have an `ImageContentSourcePolicy`, `ImageDigestMirrorSet`, or `ImageTagMirrorSet` object. You cannot add a pull secret to a project.

---

# Mirrored Configuration
To check that the mirrored configuration settings are applied, do the following on one of the nodes.
```bash
oc get imagecontentsourcepolicy -o yaml

oc get imagedigestmirrorset -o yaml
```
```bash
oc get nodes
```
```bash
oc debug node/<node-name>
```
```bash
chroot /host

cat /etc/containers/registries.conf
```

---

# 🔍 Monitor the upgrade status
```bash
watch oc get clusterversion
watch oc get clusteroperators
watch oc get mcp
watch oc get nodes
```
```bash
oc get mhc -n openshift-machine-api
oc get machines -n openshift-machine-api
```
✅ When everything is `Available=True`, `Progressing=False`, `Degraded=False`, the upgrade is complete.

```bash
oc logs -n openshift-cluster-version deployment/cluster-version-operator -f
```