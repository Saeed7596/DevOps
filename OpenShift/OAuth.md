# OAuth
## Check Access to Active Directory LDAP:
```bash
nc -vz <ip-ldap> 389
```
## With CLI:
```bash
oc edit oauth cluster
```
## With Console:
**Administrator -> CustomResourceDefinitions -> OAuth ->  Identity Providers -> LDAP**
or
**User Managenment -> Users -> Add IDP -> LDAP**
### Set the attributes.

### Check it:
**Administrator -> CustomResourceDefinitions -> OAuth ->  Instances -> YAML**

```yaml
apiVersion: config.openshift.io/v1
kind: OAuth
metadata:
  name: cluster
spec:
  identityProviders:
    - ldap:
        attributes:
          email: []
          id:
            - dn
          name:
            - cn
          preferredUsername:
            - sAMAccountName
        bindDN: 'CN=openshift,OU=Users,DC=example,DC=com'
        bindPassword:
          name: ldap-bind-secret
        insecure: true
        url: 'ldaps://example.com:389/DC=example,DC=com?sAMAccountName'
      mappingMethod: claim
      name: my-ldap
      type: LDAP
  tokenConfig:
    accessTokenInactivityTimeout: 15m
```

**You can check `logs` in the `openshift-authentication` pods.**

---

# OpenShift RBAC Roles Reference

## ✅ Level 1 — General Access (Namespace-level Roles)
**These Roles only apply within a `Project/Namespace`:**

| Role    | Description                                              |
| ------- | -------------------------------------------------------- |
| `view`  | Read-only access to view resources, no modifications     |
| `edit`  | View + create/delete/modify all resources except Roles and Policies |
| `admin` | Full management of Namespace (including RoleBinding), but no Cluster-level access |

```bash
oc adm policy add-role-to-user admin ali -n test
```

---

## ✅ Level 2 — Cluster-level Access (Common ClusterRoles)
**These Roles apply at the entire Cluster level:**

| ClusterRole	           | Description                                       |
| ---------------------- | ------------------------------------------------- |
| `cluster-admin`	       | Full super-user access across entire cluster      |
| `cluster-reader`	     | Read-only access to view entire cluster           |
| `self-provisioner`     |	User can create new Projects                     |
| `basic-user`           |	Basic access for login and viewing basic info    |
| `sudoer`               |	Extended admin-like privileges for management    |
| `system:image-puller`  |	Permission to Pull Images from internal registry |
| `system:image-builder` |	Permission to Build Images                       |
| `system:deployer`      |	Permission for Deployment operations             |
| `system:node-reader`   |	Permission to view Nodes                         |


```bash
oc adm policy add-cluster-role-to-user cluster-reader reza
```

---

## ✅ Level 3 — Specialized & System Roles (Created by OpenShift/Operators)
**These are typically for services and Operators but can be assigned to users:**

| Category         | Examples                                                              |
| ---------------- | --------------------------------------------------------------------- |
| Storage roles    | `system:storage-admin`, `system:storage-node`                         |
| Monitoring roles | `monitoring-edit`, `monitoring-view`, `alert-routing-edit`            |
| Security         | `security-admin`, `system:auth-delegator`, `system:openauth-reviewer` |
| Networking       | `system:network-admin`, `system:multus`                               |
| Registry         | `registry-admin`, `registry-viewer`, `registry-editor`                |
| Node access      | `system:node`, `system:node-admin`, `system:node-reader`              |
| Operators        | `hpa-controller`, `ingress-to-route-controller`                       |
 
---

## ✅ Role Assignment Decision Guide

| User Requirement                   |	Recommended Role            |
| ---------------------------------- | ---------------------------- |
| Read-only access to a project      |	`view`                      |
| Developer working on a project     |	`edit`                      |
| Owner of a project                 |	`admin` (namespace level)   |
| Read-only access to entire cluster |	`cluster-reader`            |
| Infrastructure operator            |	`cluster-admin`             |
| DevOps for CI/CD and Registry      |	`registry-editor` + `edit`  |


---

## ✅ Summary

| Layer                   |	Access Category                                         | 
| ----------------------- | ------------------------------------------------------- |
| Namespace Roles	        | view / edit / admin                                     | 
| Cluster Roles	          | cluster-reader / cluster-admin / self-provisioner / ... | 
| System & Operator Roles |	For specific advanced needs only                        | 

---

## Edit self-provisioners
User Management -> RoleBinding 

---

## Delete User
After delete user in console
```bash
oc get identities
```
```bash
oc delete identity 'ldap_provider:...'
```
