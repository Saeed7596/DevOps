# [OpenShift Virtualization](https://docs.redhat.com/en/documentation/openshift_container_platform/4.18/html/virtualization/index)

# Creating Virtual Machines with OpenShift Virtualization
### Technical Guide — OCP 4.18 | Bare Metal | Air-Gapped | Rook-Ceph Storage

---

> **Environment**
>
> | Item | Value |
> |---|---|
> | OpenShift Version | 4.18.23 |
> | OCP-Virt Version | 4.18.23 |
> | Storage | Rook-Ceph (rook-ceph-block) |
> | Network | OVN-Kubernetes |
> | Infrastructure | Bare Metal, Air-Gapped |
> | Cluster Domain | ocp-bm.mellat-vc.bm |

---

## Table of Contents

1. [Architecture Overview](#1-architecture-overview)
2. [VM Object Model](#2-vm-object-model)
3. [Prerequisites](#3-prerequisites)
4. [Method 1 — Web Console Wizard](#4-method-1--web-console-wizard)
5. [Method 2 — CLI with YAML Manifest](#5-method-2--cli-with-yaml-manifest)
6. [Upload ISO for Windows VMs](#6-upload-iso-for-windows-vms)
7. [Windows 10 VM — Full Walkthrough](#7-windows-10-vm--full-walkthrough)
8. [Linux VM — Full Walkthrough](#8-linux-vm--full-walkthrough)
9. [Post-Installation — VirtIO Drivers & Guest Agent](#9-post-installation--virtio-drivers--guest-agent)
10. [VM Operations](#10-vm-operations)
11. [Network Connectivity](#11-network-connectivity)
12. [Storage Configuration](#12-storage-configuration)
13. [Live Migration](#13-live-migration)
14. [Troubleshooting](#14-troubleshooting)

---

## 1. Architecture Overview

### How a VM Runs in OpenShift

```
OpenShift Cluster (OVN-Kubernetes CNI)
│
└── Namespace: default (or your namespace)
      │
      ├── VirtualMachine (VM)              ← desired state, persists when stopped
      │     └── VirtualMachineInstance (VMI) ← live running instance
      │           └── virt-launcher Pod    ← actual Kubernetes Pod
      │                 └── QEMU-KVM       ← hypervisor process
      │                       └── 🖥️ Your VM (Windows/Linux)
      │
      ├── PersistentVolumeClaim            ← VM disk (Rook-Ceph RBD)
      └── Service                         ← stable network endpoint
```

### Key Concept

```
VMs and Pods are equals in OpenShift:
  ✅ Same scheduler     (kube-scheduler)
  ✅ Same network       (OVN-Kubernetes)
  ✅ Same storage       (CSI / Rook-Ceph)
  ✅ Same RBAC          (oc policies)
  ✅ Same monitoring    (Prometheus)
  ✅ Same DNS           (cluster.local)

A VM is just a Pod running a QEMU-KVM process.
```

---

## 2. VM Object Model

### Three Kubernetes Objects Per VM

| Object | API | Purpose | Lifecycle |
|---|---|---|---|
| `VirtualMachine` | `kubevirt.io/v1` | Desired state, configuration | Permanent |
| `VirtualMachineInstance` | `kubevirt.io/v1` | Live running instance | Exists only when running |
| `virt-launcher Pod` | `v1` | Actual workload Pod | Exists only when running |

### Check All Three

```bash
# See all layers at once
oc get vm,vmi,pod -n <namespace>

# Detailed VM spec
oc get vm <vm-name> -n <namespace> -o yaml

# Live instance details (IP, node, phase)
oc get vmi <vm-name> -n <namespace> -o yaml

# Underlying Pod
oc get pod -n <namespace> | grep virt-launcher
```

---

## 3. Prerequisites

### Verify OCP-Virt is Ready

```bash
# Check HyperConverged operator status
oc get hyperconverged kubevirt-hyperconverged \
  -n openshift-cnv -o wide

# Check all OCP-Virt pods are Running
oc get pods -n openshift-cnv | grep -v Completed

# Verify CSV is Succeeded
oc get csv -n openshift-cnv

# Check virtctl is installed
virtctl version
```

### Verify Storage is Ready

```bash
# StorageClass must exist and be default
oc get sc

# StorageProfile must have RWX+Block for live migration
oc get storageprofile rook-ceph-block \
  -o jsonpath='{.status.claimPropertySets}' | jq .

# Expected:
# [
#   {"accessModes":["ReadWriteMany"],"volumeMode":"Block"},
#   {"accessModes":["ReadWriteOnce"],"volumeMode":"Block"}
# ]
```

### Verify CPU Virtualization

```bash
# Check on each worker node
oc debug node/<node-name> -- \
  chroot /host grep -c vmx /proc/cpuinfo
# Result > 0 means virtualization is supported
```

### Install virtctl CLI

```bash
# Download from cluster (air-gap safe)
PROXY_URL=$(oc get route cdi-uploadproxy \
  -n openshift-cnv \
  -o jsonpath='{.spec.host}')

# Or get download link from console
oc get ConsoleCLIDownload virtctl-clidownloads-kubevirt-hyperconverged \
  -o jsonpath='{.spec.links[*].href}'

chmod +x virtctl
mv virtctl /usr/local/bin/
virtctl version
```

---

## 4. Method 1 — Web Console Wizard

### Navigate to VM Creation

```
OpenShift Web Console
  → Left sidebar: Virtualization
    → VirtualMachines
      → Top right: Create VirtualMachine
        → From template   ← recommended for Windows/RHEL
        → From YAML       ← for advanced/custom VMs
```

### Template Selection

OCP-Virt provides pre-configured templates for common OS types:

| Template | OS | Notes |
|---|---|---|
| Microsoft Windows 10 | Windows 10 | Includes VirtIO config |
| Microsoft Windows Server 2019 | WS 2019 | Includes VirtIO config |
| Red Hat Enterprise Linux 9 | RHEL 9 | Optimized defaults |
| Fedora | Fedora Latest | Community template |
| CentOS Stream 9 | CentOS 9 | Community template |

### Wizard Fields Reference

| Field | Recommended Value | Notes |
|---|---|---|
| Name | `<os>-vm-<number>` | e.g. `win10-vm-01` |
| Namespace | Your project namespace | e.g. `default` |
| CPU Cores | 2–8 | Depends on workload |
| Memory | 4Gi–16Gi | Windows needs min 4Gi |
| Boot disk size | 60–120Gi | Windows needs min 60Gi |
| Storage class | `rook-ceph-block` | Default StorageClass |
| Access mode | `ReadWriteMany` | Required for live migration |
| Volume mode | `Block` | Better performance |

---

## 5. Method 2 — CLI with YAML Manifest

### Minimal VM Manifest Structure

```yaml
apiVersion: kubevirt.io/v1
kind: VirtualMachine
metadata:
  name: <vm-name>
  namespace: <namespace>
  labels:
    app: <vm-name>
    vm.kubevirt.io/name: <vm-name>
spec:
  running: true                          # start immediately
  template:
    metadata:
      labels:
        vm.kubevirt.io/name: <vm-name>   # used by Service selector
    spec:
      domain:
        cpu:
          cores: <count>
        memory:
          guest: <size>
        devices:
          disks: []                      # defined below
          interfaces: []                 # defined below
      networks: []                       # defined below
      volumes: []                        # defined below
```

### Apply and Manage

```bash
# Create VM
oc apply -f vm.yaml

# Start / Stop / Restart
virtctl start <vm-name> -n <namespace>
virtctl stop <vm-name> -n <namespace>
virtctl restart <vm-name> -n <namespace>

# Connect to console
virtctl console <vm-name> -n <namespace>    # serial console
virtctl vnc <vm-name> -n <namespace>        # VNC (graphical)
```

---

## 6. Upload ISO for Windows VMs

> Windows requires an ISO for installation since no cloud image is available.

### Step 1 — Expose CDI Upload Proxy

```bash
# Check if route already exists
oc get route cdi-uploadproxy -n openshift-cnv

# If not, create it
oc create route passthrough cdi-uploadproxy \
  --service=cdi-uploadproxy \
  --namespace=openshift-cnv

# Get route URL
UPLOAD_PROXY=$(oc get route cdi-uploadproxy \
  -n openshift-cnv \
  -o jsonpath='{.spec.host}')
echo "Upload proxy: https://${UPLOAD_PROXY}"
```

### Step 2 — Create ISO PVC

```yaml
# win10-iso-pvc.yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: win10-iso
  namespace: default
spec:
  accessModes:
    - ReadWriteOnce
  volumeMode: Filesystem          # ← must be Filesystem for ISO
  storageClassName: rook-ceph-block
  resources:
    requests:
      storage: 10Gi
```

```bash
oc apply -f win10-iso-pvc.yaml

# Wait for Bound status
watch oc get pvc win10-iso -n default
```

> **Important:** ISO upload requires `volumeMode: Filesystem`.
> `Block` mode is for raw VM disk images only.
> Do NOT add a `selector` block — Ceph RBD does not support PVC selectors.

### Step 3 — Upload ISO

```bash
virtctl image-upload pvc win10-iso \
  --namespace=default \
  --image-path=/path/to/Win10.iso \
  --storage-class=rook-ceph-block \
  --access-mode=ReadWriteOnce \
  --volume-mode=Filesystem \
  --size=10Gi \
  --uploadproxy-url=https://${UPLOAD_PROXY} \
  --insecure

# Expected output:
# Uploading data to https://cdi-uploadproxy-...
#  5.80 GiB / 5.80 GiB [====================] 100.00%
# Uploading data completed successfully
# Uploading Win10.iso completed successfully
```

### Step 4 — Mirror VirtIO Drivers Image

```bash
# On internet-connected machine
podman pull quay.io/containerdisks/virtio-win:latest

podman tag quay.io/containerdisks/virtio-win:latest \
  your-mirror-registry:5000/containerdisks/virtio-win:latest

podman push your-mirror-registry:5000/containerdisks/virtio-win:latest
```

---

## 7. Windows 10 VM — Full Walkthrough

### Complete VM Manifest

```yaml
# win10-vm.yaml
apiVersion: kubevirt.io/v1
kind: VirtualMachine
metadata:
  name: win10-vm-01
  namespace: default
  labels:
    app: win10-vm-01
    vm.kubevirt.io/name: win10-vm-01
    os: windows10
spec:
  running: true
  template:
    metadata:
      labels:
        vm.kubevirt.io/name: win10-vm-01
    spec:
      domain:
        cpu:
          cores: 4
          sockets: 1
          threads: 1
        memory:
          guest: 8Gi
        clock:
          utc: {}
          timer:
            hpet:
              present: false
            pit:
              tickPolicy: delay
            rtc:
              tickPolicy: catchup
            hyperv: {}
        features:
          acpi: {}
          apic: {}
          hyperv:
            relaxed: {}
            vapic: {}
            spinlocks:
              enabled: true
              spinlocks: 8191
            vpindex: {}
            runtime: {}
            synic: {}
            reset: {}
            frequencies: {}
        devices:
          disks:
            # ── Boot disk (VirtIO SCSI for best performance) ──
            - name: rootdisk
              bootOrder: 2
              disk:
                bus: virtio
            # ── Windows 10 ISO (SATA CD-ROM) ──
            - name: win10-iso
              bootOrder: 1
              cdrom:
                bus: sata
            # ── VirtIO drivers ISO ──
            - name: virtio-drivers
              cdrom:
                bus: sata
          interfaces:
            - name: default
              model: virtio
              masquerade: {}
          tpm: {}
        resources:
          requests:
            memory: 8Gi
      networks:
        - name: default
          pod: {}
      volumes:
        # ── Root disk: 80Gi RBD block volume ──
        - name: rootdisk
          persistentVolumeClaim:
            claimName: win10-vm-01-rootdisk
        # ── Windows 10 ISO ──
        - name: win10-iso
          persistentVolumeClaim:
            claimName: win10-iso
        # ── VirtIO drivers from mirror registry ──
        - name: virtio-drivers
          containerDisk:
            image: your-mirror-registry:5000/containerdisks/virtio-win:latest
```

### Create Root Disk PVC

```yaml
# win10-rootdisk-pvc.yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: win10-vm-01-rootdisk
  namespace: default
spec:
  accessModes:
    - ReadWriteMany                 # required for live migration
  volumeMode: Block                 # best performance for VM disk
  storageClassName: rook-ceph-block
  resources:
    requests:
      storage: 80Gi
```

```bash
# Apply both PVC and VM
oc apply -f win10-rootdisk-pvc.yaml
oc apply -f win10-vm.yaml

# Monitor VM startup
oc get vm,vmi -n default
oc get pod -n default | grep virt-launcher
```

### Windows Installation Steps

```bash
# Connect via VNC console
virtctl vnc win10-vm-01 -n default

# Or via Web Console:
# Virtualization → VirtualMachines → win10-vm-01 → Console tab
```

Inside the VNC console:

```
1. Windows Setup loads from ISO
2. Select language, time, keyboard → Next
3. Install Now
4. At "Where to install Windows":
   → Disk not detected  ← expected, VirtIO disk needs driver
   → Click "Load driver"
   → Browse to VirtIO CD-ROM (D: or E:)
   → Navigate to: viostor\w10\amd64
   → Select VirtIO SCSI driver → Next
5. Disk now appears → Select it → Next
6. Windows installation proceeds normally
7. Complete Windows setup (username, password, etc.)
```

### Post-Install: Update Boot Order

After Windows is installed, remove ISO and set disk as primary boot:

```bash
virtctl stop win10-vm-01 -n default

# Edit VM to remove ISO and update boot order
oc edit vm win10-vm-01 -n default
```

Change in the spec:
```yaml
# Remove or comment out the ISO cdrom disk
# Change rootdisk bootOrder to 1
devices:
  disks:
    - name: rootdisk
      bootOrder: 1          # ← was 2, now 1
      disk:
        bus: virtio
    # ── Remove win10-iso cdrom entry ──
    - name: virtio-drivers
      cdrom:
        bus: sata

volumes:
  - name: rootdisk
    persistentVolumeClaim:
      claimName: win10-vm-01-rootdisk
  # ── Remove win10-iso volume entry ──
  - name: virtio-drivers
    containerDisk:
      image: your-mirror-registry:5000/containerdisks/virtio-win:latest
```

```bash
virtctl start win10-vm-01 -n default
```

---

## 8. Linux VM — Full Walkthrough

Linux VMs are simpler — use cloud images directly (no ISO needed).

### Mirror Linux Container Disk

```bash
# On internet-connected machine
podman pull quay.io/containerdisks/centos-stream:9
podman tag quay.io/containerdisks/centos-stream:9 \
  your-mirror-registry:5000/containerdisks/centos-stream:9
podman push your-mirror-registry:5000/containerdisks/centos-stream:9
```

### Linux VM Manifest

```yaml
# centos9-vm.yaml
apiVersion: kubevirt.io/v1
kind: VirtualMachine
metadata:
  name: centos9-vm-01
  namespace: default
  labels:
    app: centos9-vm-01
    vm.kubevirt.io/name: centos9-vm-01
    os: centos-stream9
spec:
  running: true
  template:
    metadata:
      labels:
        vm.kubevirt.io/name: centos9-vm-01
    spec:
      domain:
        cpu:
          cores: 2
        memory:
          guest: 4Gi
        devices:
          disks:
            - name: rootdisk
              disk:
                bus: virtio
            - name: cloudinitdisk
              disk:
                bus: virtio
          interfaces:
            - name: default
              model: virtio
              masquerade: {}
      networks:
        - name: default
          pod: {}
      volumes:
        - name: rootdisk
          containerDisk:
            image: your-mirror-registry:5000/containerdisks/centos-stream:9
        # ── Cloud-init for initial config ──
        - name: cloudinitdisk
          cloudInitNoCloud:
            userData: |
              #cloud-config
              user: centos
              password: yourpassword
              chpasswd:
                expire: false
              ssh_authorized_keys:
                - ssh-rsa AAAA...your-public-key
              packages:
                - qemu-guest-agent
              runcmd:
                - systemctl enable --now qemu-guest-agent
```

```bash
oc apply -f centos9-vm.yaml

# SSH into Linux VM (after getting IP)
VM_IP=$(oc get vmi centos9-vm-01 -n default \
  -o jsonpath='{.status.interfaces[0].ipAddress}')
ssh centos@${VM_IP}
```

---

## 9. Post-Installation — VirtIO Drivers & Guest Agent

> Applies to **Windows VMs only**. Linux VMs use `qemu-guest-agent` package.

### What Each Driver Provides

| Driver | Component | Benefit |
|---|---|---|
| `vioscsi` / `viostor` | VirtIO SCSI/Block | High performance disk I/O |
| `NetKVM` | VirtIO Network | High performance networking |
| `balloon` | VirtIO Balloon | Dynamic memory management |
| `vioserial` | VirtIO Serial | Console communication |
| `viorng` | VirtIO RNG | Entropy source |
| `vioinput` | VirtIO Input | Keyboard/mouse optimization |
| `qemu-ga` | QEMU Guest Agent | IP reporting, snapshots, shutdown |

### Install All Drivers at Once

Inside the Windows VM:

```
1. Open File Explorer
2. Navigate to VirtIO CD-ROM drive (D: or E:)
3. Run: virtio-win-guest-tools.exe
4. Follow the installer — installs ALL drivers + QEMU Guest Agent
5. Reboot when prompted
```

### Verify Guest Agent from OCP Side

```bash
# Guest OS info (populated by QEMU Guest Agent)
oc get vmi win10-vm-01 -n default \
  -o jsonpath='{.status.guestOSInfo}' | jq .

# Expected:
# {
#   "hostname": "WIN10-VM-01",
#   "os": "Microsoft Windows 10",
#   "version": "10.0"
# }

# VM IP address (populated by Guest Agent)
oc get vmi win10-vm-01 -n default \
  -o jsonpath='{.status.interfaces}' | jq .
```

In the Web Console after Guest Agent installation:

```
Virtualization → VirtualMachines → win10-vm-01 → Overview
  ✅ IP Address: 10.x.x.x
  ✅ Hostname:   WIN10-VM-01
  ✅ Guest OS:   Microsoft Windows 10 Enterprise
  ✅ CPU usage graphs
  ✅ Memory usage graphs
```

---

## 10. VM Operations

### Start / Stop / Restart

```bash
# Start
virtctl start <vm-name> -n <namespace>

# Stop (graceful via Guest Agent)
virtctl stop <vm-name> -n <namespace>

# Force stop (immediate, like pulling power)
virtctl stop <vm-name> -n <namespace> --force --grace-period=0

# Restart
virtctl restart <vm-name> -n <namespace>

# Pause / Unpause
virtctl pause vm <vm-name> -n <namespace>
virtctl unpause vm <vm-name> -n <namespace>
```

### Console Access

```bash
# Serial console (text only, always available)
virtctl console <vm-name> -n <namespace>
# Exit: Ctrl+]

# VNC graphical console (requires virtctl on workstation)
virtctl vnc <vm-name> -n <namespace>

# Web Console VNC: Virtualization → VMs → <name> → Console tab
```

### Get VM Status

```bash
# Summary
oc get vm,vmi -n <namespace>

# Detailed status
oc describe vmi <vm-name> -n <namespace>

# Which node is VM running on
oc get vmi <vm-name> -n <namespace> \
  -o jsonpath='{.status.nodeName}'

# VM IP address
oc get vmi <vm-name> -n <namespace> \
  -o jsonpath='{.status.interfaces[0].ipAddress}'
```

### Snapshot a VM

```bash
# Create snapshot (VM can be running)
cat <<EOF | oc apply -f -
apiVersion: snapshot.kubevirt.io/v1alpha1
kind: VirtualMachineSnapshot
metadata:
  name: win10-snap-$(date +%Y%m%d)
  namespace: default
spec:
  source:
    apiGroup: kubevirt.io
    kind: VirtualMachine
    name: win10-vm-01
EOF

# Check snapshot status
oc get vmsnapshot -n default
```

### Resize VM (Hot-plug CPU/Memory)

```bash
# Edit VM spec (requires restart for most changes)
oc edit vm win10-vm-01 -n default

# Hot-plug a disk (no restart needed)
virtctl addvolume win10-vm-01 \
  --volume-name=extra-disk \
  --persist \
  -n default
```

---

## 11. Network Connectivity

### Default Pod Network

Every VM gets a Pod IP automatically:

```bash
# Get VM IP
oc get vmi <vm-name> -n <namespace> \
  -o jsonpath='{.status.interfaces[0].ipAddress}'
```

### Create a Service for Stable DNS

```yaml
# vm-service.yaml
apiVersion: v1
kind: Service
metadata:
  name: win10-vm-01-svc
  namespace: default
spec:
  selector:
    vm.kubevirt.io/name: win10-vm-01     # matches VM label
  ports:
    - name: rdp
      port: 3389
      targetPort: 3389
    - name: winrm
      port: 5985
      targetPort: 5985
```

```bash
oc apply -f vm-service.yaml

# DNS name (accessible from any Pod or VM in cluster):
# win10-vm-01-svc.default.svc.cluster.local:3389
```

### Expose RDP Externally via Route

```bash
# NodePort for RDP (TCP, not HTTP — can't use Route for RDP)
oc patch svc win10-vm-01-svc -n default \
  --type=merge \
  -p '{"spec":{"type":"NodePort"}}'

# Get assigned NodePort
oc get svc win10-vm-01-svc -n default \
  -o jsonpath='{.spec.ports[?(@.name=="rdp")].nodePort}'

# Connect via RDP client:
# <any-node-ip>:<nodeport>
```

### VM to Pod Communication (same namespace)

```
From Windows VM: ping splunk-forwarder.default.svc.cluster.local
From Pod:        curl http://win10-vm-01-svc.default.svc.cluster.local:8080

No extra configuration needed — OVN-Kubernetes handles it.
```

---

## 12. Storage Configuration

### StorageClass Reference

| StorageClass | Mode | Access | Use Case |
|---|---|---|---|
| `rook-ceph-block` | Block | RWO / RWX | VM disks (recommended) |
| `rook-cephfs` | Filesystem | RWX | Shared data volumes |

### VM Disk PVC Best Practices

```yaml
# Optimal PVC for VM boot disk
spec:
  accessModes:
    - ReadWriteMany     # RWX enables live migration
  volumeMode: Block     # Block = best performance, no filesystem overhead
  storageClassName: rook-ceph-block
  resources:
    requests:
      storage: 80Gi
```

### Add Extra Data Disk to VM

```yaml
# extra-disk-pvc.yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: win10-data-disk
  namespace: default
spec:
  accessModes:
    - ReadWriteMany
  volumeMode: Block
  storageClassName: rook-ceph-block
  resources:
    requests:
      storage: 200Gi
```

Add to VM spec:

```yaml
spec:
  template:
    spec:
      domain:
        devices:
          disks:
            - name: datadisk
              disk:
                bus: virtio
      volumes:
        - name: datadisk
          persistentVolumeClaim:
            claimName: win10-data-disk
```

---

## 13. Live Migration

### Requirements

```
✅ PVC accessMode: ReadWriteMany (RWX)
✅ PVC volumeMode: Block
✅ StorageProfile patched with RWX+Block
✅ QEMU Guest Agent installed (Windows)
✅ At least 2 worker nodes
```

### Trigger Live Migration

```bash
# Migrate VM to another node
virtctl migrate win10-vm-01 -n default

# Watch migration progress
oc get vmim -n default -w

# Expected:
# NAME                    PHASE       VMI
# kubevirt-migrate-xxxx   Running     win10-vm-01
# kubevirt-migrate-xxxx   Succeeded   win10-vm-01  ✅

# Verify VM moved to different node
oc get vmi win10-vm-01 -n default \
  -o jsonpath='{.status.nodeName}'
```

### Verify StorageProfile Supports Migration

```bash
oc patch storageprofile rook-ceph-block \
  --type=merge \
  -p '{
    "spec": {
      "claimPropertySets": [
        {"accessModes": ["ReadWriteMany"], "volumeMode": "Block"},
        {"accessModes": ["ReadWriteOnce"], "volumeMode": "Block"}
      ]
    }
  }'
```

---

## 14. Troubleshooting

### VM Won't Start

```bash
# Check VM events
oc describe vm <vm-name> -n <namespace> | tail -30

# Check VMI events
oc describe vmi <vm-name> -n <namespace> | tail -30

# Check virt-launcher Pod logs
POD=$(oc get pod -n <namespace> -l kubevirt.io=virt-launcher \
  --field-selector=status.phase=Running -o name | head -1)
oc logs $POD -n <namespace> -c compute
```

### PVC Stuck in Pending

```bash
# Check PVC events
oc describe pvc <pvc-name> -n <namespace> | tail -20
```

| Error Message | Cause | Fix |
|---|---|---|
| `claim Selector is not supported` | PVC has a `selector` block | Remove selector from PVC spec |
| `waiting for first consumer` | VolumeBindingMode issue | Set `volumeBindingMode: Immediate` in StorageClass |
| `no persistent volumes available` | Ceph CSI issue | Check `oc get pods -n rook-ceph \| grep csi` |
| `driver not found` | CSI driver not running | Restart Rook operator pod |

### ISO Upload Fails

```bash
# Check CDI upload proxy is exposed
oc get route cdi-uploadproxy -n openshift-cnv

# Check CDI pods
oc get pods -n openshift-cnv | grep cdi

# Verify PVC is Bound before upload
oc get pvc win10-iso -n default
```

| Error | Cause | Fix |
|---|---|---|
| `PVC not available for upload` | PVC not Bound or wrong volumeMode | Use `volumeMode: Filesystem` for ISO PVC |
| `connection refused` | uploadproxy route missing | Create route for `cdi-uploadproxy` service |
| `TLS error` | Self-signed cert | Add `--insecure` flag |

### Live Migration Fails

```bash
# Check migration object
oc get vmim -n <namespace> -o yaml | grep -A10 status

# Check virt-handler logs on both nodes
oc logs -n openshift-cnv \
  $(oc get pod -n openshift-cnv -l kubevirt.io=virt-handler \
  -o name | head -1) --tail=50
```

| Error | Cause | Fix |
|---|---|---|
| `PVC is not RWX` | Access mode is RWO only | Recreate PVC with `ReadWriteMany` |
| `migration timeout` | Network too slow | Check node-to-node bandwidth |
| `guest agent not responding` | QEMU Guest Agent not installed | Install `virtio-win-guest-tools.exe` |

### Common Diagnostic Commands

```bash
# Full VM status
oc get vm,vmi,pod,pvc -n <namespace>

# OCP-Virt operator logs
oc logs -n openshift-cnv \
  deploy/virt-operator --tail=50

# virt-controller logs
oc logs -n openshift-cnv \
  deploy/virt-controller --tail=50

# CDI logs
oc logs -n openshift-cnv \
  deploy/cdi-deployment --tail=50

# All events in namespace sorted by time
oc get events -n <namespace> \
  --sort-by='.lastTimestamp' | tail -30
```

---

## Quick Reference Card

```bash
# ── Create ──────────────────────────────────────────────
oc apply -f vm.yaml                          # create VM from manifest
virtctl start <vm> -n <ns>                   # start VM

# ── Connect ─────────────────────────────────────────────
virtctl console <vm> -n <ns>                 # serial console
virtctl vnc <vm> -n <ns>                     # VNC graphical

# ── Status ──────────────────────────────────────────────
oc get vm,vmi -n <ns>                        # VM status
oc get vmi <vm> -n <ns> -o jsonpath='{.status.nodeName}'    # which node
oc get vmi <vm> -n <ns> -o jsonpath='{.status.interfaces}'  # IP address

# ── Lifecycle ───────────────────────────────────────────
virtctl stop <vm> -n <ns>                    # graceful stop
virtctl restart <vm> -n <ns>                 # restart
virtctl migrate <vm> -n <ns>                 # live migrate

# ── Storage ─────────────────────────────────────────────
virtctl image-upload pvc <pvc> \
  --image-path=<iso> \
  --uploadproxy-url=https://<proxy> \
  --insecure                                 # upload ISO

# ── Snapshot ────────────────────────────────────────────
oc get vmsnapshot -n <ns>                    # list snapshots

# ── Debug ───────────────────────────────────────────────
oc describe vmi <vm> -n <ns>                 # detailed status + events
oc get events -n <ns> --sort-by='.lastTimestamp'  # all events
```

---

*Document generated for OpenShift Virtualization 4.18.23*
*Cluster: ocp-bm.mellat-vc.bm | Rook-Ceph Storage | Air-Gapped | Bare Metal*
