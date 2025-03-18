# OpenShift Documentation

## What is OpenShift?
OpenShift is a Kubernetes-based container platform developed by Red Hat. It provides a robust environment for deploying, managing, and scaling containerized applications with built-in security and automation features.

## Key Features of OpenShift:
- **Enterprise Kubernetes**: Built on Kubernetes with additional security and operational features.
- **Developer-Friendly**: Provides a seamless experience with CI/CD tools, automation, and developer-friendly interfaces.
- **Security & Compliance**: Integrated security policies, role-based access control (RBAC), and image scanning.
- **Hybrid & Multi-Cloud**: Deployable on-premise, public cloud, or in a hybrid model.
- **Operator Framework**: Enables simplified application management.

## OpenShift vs. Other Container Orchestration Platforms

| Feature             | OpenShift                           | Kubernetes                          | Docker Swarm | Rancher |
|---------------------|----------------------------------|----------------------------------|--------------|---------|
| Security           | Built-in security policies, RBAC | Requires manual configuration  | Basic security | Provides additional RBAC and security policies |
| CI/CD Integration  | Native support via OpenShift Pipelines | External tools like Jenkins needed | Limited support | Supports external CI/CD tools like Jenkins and GitLab |
| Enterprise Support | Yes                              | Community-driven                 | No official support | Yes |
| Multi-cloud        | Yes                              | Requires configuration           | No | Yes |
| GUI Dashboard      | Built-in                          | External dashboard needed       | Yes | Yes |

## Installing and Configuring OpenShift

### Prerequisites:
- Linux-based OS (RHEL, CentOS, Fedora, Ubuntu)
- Minimum 4 CPU cores, 8GB RAM
- Docker or Podman installed
- oc CLI installed

### Installation Steps:
Before proceeding with the installation, you must create an account on [Red Hat's website](https://access.redhat.com/) to obtain the necessary credentials and downloads.
#### Installing OpenShift with Local Sandbox
1. **Install the OpenShift CLI (oc)**:
   ```sh
   curl -LO https://mirror.openshift.com/pub/openshift-v4/clients/oc/latest/linux/oc.tar.gz
   tar -xvf oc.tar.gz -C /usr/local/bin/
   chmod +x /usr/local/bin/oc
   ```
2. **Deploy OpenShift Sandbox (Lightweight test environment)**:
   ```sh
   curl -LO https://developers.redhat.com/content-gateway/rest/mirror/pub/openshift-v4/clients/crc/latest/crc-linux-amd64.tar.xz
   tar -xvf crc-linux-amd64.tar.xz
   sudo mv crc /usr/local/bin/
   crc setup
   crc start
   ```
3. **Login to OpenShift**:
   ```sh
   oc login -u kubeadmin -p <password> --server=<openshift_api_url>
   ```

## OpenShift Concepts
### Deployment Config
A **DeploymentConfig** is an OpenShift-specific resource that extends Kubernetes Deployments. It allows automatic rollbacks, triggers, and manual scaling.

### Image Streams
**ImageStreams** track images across different registries, ensuring that deployments use the latest verified images.

### Build and Build Config
**BuildConfig** defines how an application should be built from source code, while **Builds** are the execution of these configurations.

### Source-to-Image (S2I)
**S2I** is an OpenShift feature that allows developers to build images directly from source code without needing Dockerfiles.

### Resource Quota
A **ResourceQuota** limits resource consumption at the project level to ensure fair usage.

### Template and Catalog
**Templates** provide reusable configurations for applications and infrastructure. The **Catalog** allows easy deployment of predefined services.

### Security Context Constraints (SCC)
**SCCs** control user permissions and security contexts within OpenShift clusters, restricting container capabilities for security.

## OpenShift Commands Cheat Sheet

| Command | Description |
|---------|-------------|
| `oc login` | Authenticate to OpenShift cluster |
| `oc new-project <name>` | Create a new project |
| `oc get pods` | List all running pods |
| `oc get nodes` | Display node information |
| `oc apply -f <file>.yaml` | Apply configuration from a YAML file |
| `oc expose svc <service-name>` | Expose a service as a route |
| `oc scale deployment <name> --replicas=3` | Scale a deployment |
| `oc delete pod <pod-name>` | Delete a specific pod |
| `oc create user <username>` | Create a new user |

## Conclusion
OpenShift simplifies Kubernetes deployment while adding enterprise features like security, automation, and monitoring. It is a strong choice for enterprises looking for a fully managed Kubernetes solution.
