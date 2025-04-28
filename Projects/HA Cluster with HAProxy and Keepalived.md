# Kubernetes HA Cluster with HAProxy and Keepalived (Full Setup)

This guide explains how to set up a highly available Kubernetes control plane using two HAProxy servers and a Virtual IP (VIP) managed by Keepalived.

---

## Architecture Overview

- **3 Kubernetes Master nodes**
- **2 Kubernetes Worker nodes**
- **2 HAProxy servers for Load Balancing traffic to kube-apiserver**
- **Keepalived** to manage a Virtual IP (VIP) for HAProxy servers
- **Cloudflare DNS** (or any public DNS) will point to the VIP

---

## 1. Environment Setup

- HAProxy1 IP: `192.168.1.10`
- HAProxy2 IP: `192.168.1.11`
- VIP (Virtual IP): `192.168.1.100`
- Network Interface: `eth0`

> Make sure to adjust IP addresses and interface names according to your actual setup.

---

## 2. Install Keepalived

Install `keepalived` on both HAProxy servers:

### Ubuntu/Debian:
```bash
sudo apt update
sudo apt install keepalived -y
```

### CentOS/RHEL:
```bash
sudo yum install keepalived -y
```

---

## 3. Configure Keepalived

### On HAProxy1 (`192.168.1.10`): `/etc/keepalived/keepalived.conf`

```bash
vrrp_instance VI_1 {
    state MASTER
    interface eth0
    virtual_router_id 51
    priority 150
    advert_int 1
    authentication {
        auth_type PASS
        auth_pass StrongPasswordHere
    }
    virtual_ipaddress {
        192.168.1.100
    }
}
```

### On HAProxy2 (`192.168.1.11`): `/etc/keepalived/keepalived.conf`

```bash
vrrp_instance VI_1 {
    state BACKUP
    interface eth0
    virtual_router_id 51
    priority 100
    advert_int 1
    authentication {
        auth_type PASS
        auth_pass StrongPasswordHere
    }
    virtual_ipaddress {
        192.168.1.100
    }
}
```

> Notes:
> - The `priority` value on HAProxy1 should be higher than HAProxy2.
> - `virtual_router_id` must be the same on both.
> - Choose a strong password for `auth_pass`.

---

## 4. Start and Enable Keepalived

```bash
sudo systemctl enable keepalived
sudo systemctl restart keepalived
```

Run this on both HAProxy servers.

### Test VIP:
- Run `ip a` on HAProxy1 to check if VIP is assigned.
- Stop keepalived on HAProxy1 and check if VIP moves to HAProxy2.

---

## 5. Install and Configure HAProxy

Install HAProxy:

```bash
sudo apt install haproxy -y
# or
sudo yum install haproxy -y
```

### Example HAProxy configuration `/etc/haproxy/haproxy.cfg`

```bash
global
    log /dev/log    local0
    log /dev/log    local1 notice
    chroot /var/lib/haproxy
    stats timeout 30s
    user haproxy
    group haproxy
    daemon

defaults
    log     global
    option  httplog
    option  dontlognull
    timeout connect 5s
    timeout client  50s
    timeout server  50s

frontend kubernetes_frontend
    bind *:6443
    default_backend kubernetes_backend

backend kubernetes_backend
    balance roundrobin
    option tcp-check
    server master1 192.168.1.21:6443 check fall 3 rise 2
    server master2 192.168.1.22:6443 check fall 3 rise 2
    server master3 192.168.1.23:6443 check fall 3 rise 2
```

> Adjust `192.168.1.21/22/23` to your Kubernetes master node IPs.

Reload HAProxy:

```bash
sudo systemctl enable haproxy
sudo systemctl restart haproxy
```

---

## 6. Cloudflare DNS Setup

- In Cloudflare (or your DNS provider), create an A record:
  - **Name**: `@` (for root domain) or `api` (for subdomain like `api.saeed.com`)
  - **IPv4 address**: `192.168.1.100` (your VIP)
  - **Proxy Status**: Set to **DNS only** (gray cloud)

---

## Summary

| Component | Purpose |
|:---|:---|
| Kubernetes Masters | Run the control plane |
| HAProxy Servers | Load balancing traffic to kube-apiserver |
| Keepalived | Provide VIP high availability |
| Cloudflare DNS | Public DNS pointing to VIP |


✅ With this setup, you achieve full high availability for your Kubernetes control plane access.

---

## Next Steps
- Secure HAProxy with SSL/TLS termination if needed.
- Fine-tune HAProxy health checks.
- Monitor Keepalived state for better observability.


---

# Good Luck with your Production Grade Kubernetes Cluster! 🚀
