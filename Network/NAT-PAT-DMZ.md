# 🔐 NAT, PAT, and DMZ Explained

## 1. What is NAT (Network Address Translation)?

**NAT** is a method that allows multiple devices on a private network to access external networks (like the Internet) using one or a few public IP addresses.

### **Why NAT Exists**
- IPv4 address shortage — not enough public IPs for every device.
- Security — hides internal network structure from the outside world.
- Routing simplicity — reduces the global routing table size. 
  - If every device in the world had a direct public IP, routing tables would become very large and unmanageable.

### **Types of NAT**
| Type | Description | Example |
|------|--------------|----------|
| **Static NAT** | One-to-one mapping between a private IP and a public IP. | `192.168.1.10 ↔ 203.0.113.10` |
| **Dynamic NAT** | Maps private IPs to a pool of public IPs dynamically. | Uses available public IPs from a defined pool. |
| **PAT (Port Address Translation)** | Also known as *NAT Overload*. Many private IPs share one public IP, distinguished by **port numbers**. | `192.168.1.5:1025 → 203.0.113.5:2001` |

---

## 2. PAT (Port Address Translation)

**PAT** enables multiple internal hosts to access external networks using **a single public IP** by mapping each connection to a **unique port number**.

### **How It Works**
1. A device in the LAN sends a packet to the Internet.
2. The router replaces:
   - **Source IP:** from private to public IP
   - **Source Port:** with a unique random port number
3. The router maintains a **translation table** to map connections back when replies arrive.

| Internal Address | Port | Translated Public Port |
|------------------|------|------------------------|
| 192.168.1.2 | 1025 | 30001 |
| 192.168.1.3 | 1026 | 30002 |
| 192.168.1.4 | 1027 | 30003 |

---

## 3. Example Scenario

Imagine a home network:
```nginx
PC1: 192.168.1.10
PC2: 192.168.1.11
Router (WAN): 45.12.5.10
```

When both PCs access the Internet:
- NAT translates `192.168.1.x` to `45.12.5.10`
- PAT assigns different source ports so traffic can be distinguished.

| Device | Source IP (Private) | Translated IP (Public) | Source Port |
|--------|--------------------|------------------------|--------------|
| PC1 | 192.168.1.10 | 45.12.5.10 | 30211 |
| PC2 | 192.168.1.11 | 45.12.5.10 | 30212 |

This allows **many internal devices** to share **one public IP**.

---

## 4. DMZ (Demilitarized Zone)

A **DMZ** is a small, isolated network between the **internal LAN** and the **Internet**, used to host **public-facing services** (e.g., web servers, mail servers, DNS).

### **Why Use a DMZ**
- Protects the internal LAN if a public server is compromised.
- Separates **public traffic** from **private internal traffic**.
- Allows controlled access through **firewall rules**.

### **Typical DMZ Setup**
```nginx
|
[Public IP]
|
[Firewall / Router]
├── [DMZ Network: 192.168.50.0/24]
│ ├── Web Server: 192.168.50.10
│ └── Mail Server: 192.168.50.20
└── [Internal LAN: 192.168.1.0/24]
└── Employees, PCs, etc.
```


### **Routing and NAT in a DMZ Scenario**

- External users access the web server via **Static NAT**:  
  `Public IP 203.0.113.10 → 192.168.50.10`
- Internal users in the LAN can reach the server directly without NAT.
- The firewall allows:
  - HTTP/HTTPS from Internet → DMZ
  - Management traffic (SSH, RDP) from LAN → DMZ
  - No direct traffic from Internet → LAN

---

## 5. Example Configuration Commands (Linux)

```bash
# View current routing table
ip route show

# Add a default route
sudo ip route add default via 192.168.1.1 dev eth0

# Enable IP forwarding (for NAT)
sudo sysctl -w net.ipv4.ip_forward=1

# Configure NAT using iptables
sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
```

---

## 6. Summary
| Concept |	Description |
| ------- | ----------- |
| NAT |	Translates private ↔ public IPs |
| PAT |	Many-to-one translation using ports |
| DMZ |	Isolated zone for public servers |
| Static NAT |	Fixed mapping between internal and external IPs |
| Dynamic NAT |	Uses a pool of public IPs dynamically |
