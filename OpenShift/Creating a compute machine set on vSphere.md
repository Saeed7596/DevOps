# [Creating a compute machine set on vSphere ](https://docs.redhat.com/en/documentation/openshift_container_platform/4.20/html/machine_management/managing-compute-machines-with-the-machine-api#creating-machineset-vsphere)

## 1. Create new MachineSet
```yaml
apiVersion: machine.openshift.io/v1beta1
kind: MachineSet
metadata:
 annotations:
   machine.openshift.io/memoryMb: '16384'
   machine.openshift.io/vCPU: '4'
 name: openshift-74r6t-worker-0
 namespace: openshift-machine-api
 labels:
   machine.openshift.io/cluster-api-cluster: openshift-74r6t
spec:
 replicas: 0
 selector:
   matchLabels:
     machine.openshift.io/cluster-api-cluster: openshift-74r6t
     machine.openshift.io/cluster-api-machineset: openshift-74r6t-worker-0
 template:
   metadata:
     labels:
       machine.openshift.io/cluster-api-cluster: openshift-74r6t
       machine.openshift.io/cluster-api-machine-role: worker
       machine.openshift.io/cluster-api-machine-type: worker
       machine.openshift.io/cluster-api-machineset: openshift-74r6t-worker-0
   spec:
     lifecycleHooks: {}
     metadata: {}
     providerSpec:
       value:
         numCoresPerSocket: 4
         diskGiB: 120
         snapshot: ''
         userDataSecret:
           name: worker-user-data
         memoryMiB: 16384
         credentialsSecret:
           name: vsphere-cloud-credentials
         network:
           devices:
             - addressesFromPools:
                 - group: installer.openshift.io
                   name: default-0
                   resource: IPPool
               nameservers:
                 - 192.168.254.214
               networkName: VM Network
         metadata:
           creationTimestamp: null
         numCPUs: 4
         kind: VSphereMachineProviderSpec
         workspace:
           datacenter: OCP-DC
           datastore: /OCP-DC/datastore/datastore1
           folder: /OCP-DC/vm/openshift-74r6t
           resourcePool: /OCP-DC/host/OCP-Cluster/Resources
           server: 192.168.254.217
         template: openshift-74r6t-rhcos-OCP-DC-OCP-Cluster # You must see the template in vSphere!
         apiVersion: machine.openshift.io/v1beta1
```

---

## 2. Scale the compute machine set by running one of the following commands:
```bash
oc scale --replicas=2 machinesets.machine.openshift.io <machineset> -n openshift-machine-api
```
or
```bash
oc edit machinesets.machine.openshift.io <machineset> -n openshift-machine-api
```
or Scale up in Web Console.

---

## 3. Already new `IPAddressClaim` must be created.
### Administrator -> CustomResourceDefinition -> Search `ipam` -> IPAddressClaim -> Copy the Name of new One!

---

## 4. Create IPAdress
### Administrator -> CustomResourceDefinition -> Search `ipam` -> IPAddress -> Create
    * With same name of <ip-address-calim-name>
    * Set IP Static

---

## 5. Update `IPAddressClaim` status with `CLI`
```bash
oc --type=merge patch IPAddressClaim -n openshift-machine-api <ip-address-calim-name> -p='{"status":{"addressRef": {"name": "<ip-address-calim-name>"}}}' --subresource=status
```
After patched check the `IPAddressClaim`
```yaml
status:
 addressRef:
   name: <ip-address-calim-name>
```

---

# Update Note❗
1. 1. Lock the machine status.
```bash
oc -n openshift-machine-api annotate mhc <mhc-name> cluster.x-k8s.io/paused=""
```
2. Backup list (required)
```bash
oc get machine -n openshift-machine-api -o wide > machines.before
oc get ipaddressclaim -n openshift-machine-api -o yaml > ipclaims.before.yaml
oc get ipaddress -n openshift-machine-api -o yaml > ipaddresses.before.yaml
```
3. Verify that no Machine is being replaced.
```bash
oc get machine -n openshift-machine-api
oc get events -n openshift-machine-api | grep -i delete
```
4. What to check after upgrading?
```bash
oc get nodes
oc get machine -n openshift-machine-api
oc get ipaddressclaim -n openshift-machine-api
```
