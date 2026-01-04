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
```bash
oc apply -f <path_to_oc-mirror_workspace>/working-dir/cluster-resources
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

# 2. Updating a cluster in a disconnected environment without the OpenShift Update Service
