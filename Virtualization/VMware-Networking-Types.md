
# VMware Networking Types

This document explains the different network types available in VMware Workstation/Player and ESXi/vSphere, along with their purposes and use cases.

In **VMware Workstation**
```
Edit -> Virual Network Editor
```

---

## VMware Workstation / Player Network Types

### 1. **Bridged Network**
Connects the virtual machine directly to the physical network.

**Characteristics:**
- VM receives an IP address from the physical LAN.
- Acts as if it is another physical device on the network.

**Use Cases:**
- Realistic enterprise simulations.
- When VM must be reachable from the LAN.
- Hosting services tested directly in a local network.

---

### 2. **NAT (Network Address Translation)**
VM receives a private IP and uses the host as a gateway to access external networks.

**Characteristics:**
- VM is hidden behind the host.
- IP assigned from a private network (e.g., 192.168.x.x).
- Outbound connections work; inbound does not unless port forwarding is set.

**Use Cases:**
- When VM needs internet but must stay invisible to the LAN.
- Restricted environments where bridged mode is not allowed.

---

### 3. **Host-Only Network**
A fully isolated network between the host and virtual machines.

**Characteristics:**
- No internet access.
- No connection to the physical LAN.
- Only VM ↔ Host and VM ↔ VM communication.

**Use Cases:**
- Malware analysis.
- Isolated lab environments.
- Secure testing without risk to the physical LAN.

---

### 4. **LAN Segments / Custom Networks**
Allows creation of isolated virtual networks between selected VMs.

**Characteristics:**
- No connectivity with the host or the external network.
- Useful for building custom topologies.

**Use Cases:**
- Advanced network labs.
- Multi-tier architectures.
- Firewall, router, VLAN simulations.

---

## VMware ESXi / vSphere Network Types

### 1. **vSwitch (Virtual Switch)**
Virtual switch that connects VMs to each other and physical NICs.

---

### 2. **Port Groups**
Logical configurations on vSwitches.

**Types include:**
- VM Network (VM traffic)
- Management Network
- vMotion Network
- Storage Network (iSCSI/NFS)

---

### 3. **VLAN Tagging**
Segregates traffic using VLAN IDs on port groups.

**Use Cases:**
- Data centers
- Multi-tenant networks
- Security segmentation

---

### 4. **Distributed vSwitch (vDS)**
Centralized virtual switch for managing networking across multiple ESXi hosts.

**Benefits:**
- Centralized configuration
- Advanced load balancing
- Enterprise-level performance and security

---

## Summary Table

| Network Type | Description | Use Case |
|--------------|-------------|----------|
| **Bridged** | VM is part of physical LAN | Realistic networking |
| **NAT** | VM has private IP and uses host for external access | Internet without LAN exposure |
| **Host-Only** | Isolated network between VMs and host | Labs, secure testing |
| **LAN Segment** | Isolated VM-only networks | Advanced simulations |
| **vSwitch / Port Group** | ESXi network building blocks | Data center networking |

