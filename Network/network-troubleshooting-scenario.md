
# Network Troubleshooting Scenario (Step-by-Step Guide)

## Scenario: “The computer is not connected to the Internet / websites do not load.”
**Goal:** Identify and fix network issues from the physical layer up to the application layer.

---

## Step 0 — Preparation
- Access the affected computer (locally or remotely).
- Have another working device on the same network for comparison.

---

## Step 1 — Check Physical Connection and Link
**Purpose:** Ensure that the cable/Wi-Fi and interface are active.

### Linux
```bash
ip addr show
ethtool eth0
```
Check physical cable or port LEDs.

### Windows
```powershell
ipconfig /all
Get-NetAdapter
```

**Interpretation:**
- Interface should be `UP` and `RUNNING`.
- If Wi-Fi, ensure it’s associated with an SSID.
- If `ethtool` shows no link or 0 Mbps, there’s a cable/port issue.

---

## Step 2 — IP Addressing and DHCP
**Purpose:** Verify that IP and gateway are assigned correctly.

### Linux
```bash
ip addr show eth0
ip route show
cat /etc/resolv.conf
```

### Windows
```powershell
ipconfig
route print
```

**Interpretation:**
- If IP is `169.254.x.x`, DHCP failed.
- Check for `default via` route in `ip route` output.
- Missing DNS in `resolv.conf` causes name resolution failure.

---

## Step 3 — Test Local Connectivity (Ping and ARP)
**Purpose:** Ensure communication with the local gateway.

### Linux
```bash
ping -c 4 <default-gateway>
ip neigh show
```

### Windows
```powershell
ping -n 4 <default-gateway>
arp -a
```

**Interpretation:**
- No ping reply → local link issue or gateway offline.
- Missing ARP entry → Layer 2/VLAN problem.

---

## Step 4 — Trace Route to the Internet
**Purpose:** See how far packets travel.

### Linux
```bash
traceroute 8.8.8.8
mtr --report 8.8.8.8
```

### Windows
```powershell
tracert 8.8.8.8
```

**Interpretation:**
- Failure at first hop → gateway issue.
- Stops at ISP → external routing problem.

---

## Step 5 — DNS Test
**Purpose:** Check if name resolution works.

### Linux
```bash
nslookup google.com
dig +short google.com
```

### Windows
```powershell
nslookup google.com
```

**Interpretation:**
- If ping to IP works but DNS fails → DNS misconfiguration.

---

## Step 6 — Test IP Connectivity
**Purpose:** Confirm internet access without DNS.

```bash
ping -c 4 8.8.8.8
curl -I http://example.com
curl -I http://93.184.216.34
```

**Interpretation:**
- Ping to IP OK but domain fails → DNS issue.
- IP unreachable → routing/NAT/ISP issue.

---

## Step 7 — Routing and Default Route
**Purpose:** Ensure correct routes exist.

```bash
ip route show
sudo ip route add default via <gateway-ip> dev eth0
```

**Interpretation:**
- Missing default route → no traffic outside subnet.
- Route exists but still no connectivity → router/NAT/firewall issue.

---

## Step 8 — Firewall Check
**Purpose:** Detect any blocked traffic.

```bash
# iptables - View traditional firewall rules
sudo iptables -L -n -v

# nftables - Show the entire structure of the new firewall
sudo nft list ruleset

# Readable firewall status (on Ubuntu and Debian)
sudo ufw status verbose

# Readable firewall status (on RedHat)
sudo firewall-cmd --state
sudo firewall-cmd --list-all
sudo firewall-cmd --list-all-zones
```

**Interpretation:**
- DROP/REJECT rules may block outgoing/incoming packets.

### Enable or disable the firewall
```bash
# Ubuntu
sudo ufw enable/disable
# RedHat
sudo systemctl enable/disable firewalld
```
### Open SSH Port
```bash
# Ubuntu
udo ufw allow 22/tcp
# RedHat
sudo firewall-cmd --permanent --add-service=ssh && sudo firewall-cmd --reload
```

---

## Step 9 — Packet Capture
**Purpose:** Verify packet flow and response.

```bash
sudo tcpdump -n -i eth0 host 8.8.8.8 -w /tmp/cap.pcap
```
**Note**: No packets are printed to the terminal — they are just saved to a file. You'll need to open it later with Wireshark or `tcpdump -r /tmp/cap.pcap`.
```bash
sudo tcpdump -n -i eth0 icmp
```
**Note**: Live display of all ICMP packets (like ping) on ​​eth0 in the terminal.

**Interpretation:**
- Requests sent but no reply → remote issue.
- No packets sent → local routing/firewall problem.

### Troubleshooting specific service connectivity (e.g. SSH on port 2222).
```bash
sudo tcpdump -i eth0 'tcp port 2222' -nn -vv -s 0
```
Accurate and live display of all TCP traffic on port 2222 (for example, if SSH or a custom service is running on that port).

---

## Step 10 — NAT and Public IP Test
**Purpose:** Verify NAT translation and public IP.

```bash
curl -s https://ifconfig.co
```

**Interpretation:**
- Displays public IP assigned by your ISP/router.

---

## Step 11 — Service and Application-Level Tests
**Purpose:** Check specific services (e.g., HTTP).

```bash
nc -vz example.com 80
nc -vz example.com 443
ss -tulnp
```

**Interpretation:**
- Closed ports → service offline or blocked by firewall.

---

## Quick Summary (Cheatsheet)
| Layer | What to Check | Tools/Commands |
|-------|----------------|----------------|
| 1 | Cable, Wi-Fi, link | `ip addr`, `ethtool` |
| 2 | Local network | `ping <gw>`, `ip neigh` |
| 3 | Routes | `ip route`, `traceroute` |
| 4 | IP Connectivity | `ping 8.8.8.8` |
| 5 | DNS | `nslookup`, `dig` |
| 7 | Application | `curl`, `nc`, `ss` |

---

## Common Mistakes
- Assuming modem ping = internet access. (NAT/ISP may still fail)
- Missing default route after static IP setup.
- DNS not assigned via DHCP.
- Firewall silently dropping ICMP or DNS packets.

---

## Summary
This structured process lets you isolate network issues layer by layer, from cable failures to DNS or routing problems. Use packet captures and route inspection only after confirming physical and IP-level basics.

# ============================



## 3. 🔧 Scenario: Testing TCP Connectivity Between Two Hosts

### 🧠 Objective
Verify if two hosts in a LAN can communicate over a specific TCP port (e.g., 8080).

---

### 🖥️ Environment Setup

| Hostname | IP Address | Role |
|-----------|-------------|------|
| `server1` | 192.168.10.10 | Web Server |
| `client1` | 192.168.10.20 | Client |

---

### ⚙️ Step 1: Listen on Server

On **server1**:
```bash
sudo nc -l -p 8080
```
The server now waits for incoming connections on port **8080**.

---

### ⚙️ Step 2: Connect from Client

On **client1**:
```bash
nc 192.168.10.10 8080
```
Type any message:
```
Hello from client
```
You’ll see the same message appear on the server terminal — indicating a successful connection.

---

### ⚙️ Step 3: Add Verbosity for Troubleshooting

```bash
nc -v 192.168.10.10 8080
```

If you see:
```
Connection refused
```
➡️ The service isn’t listening on that port.  
If you see:
```
Timed out
```
➡️ The connection is blocked by a firewall or routing issue.

---

### ⚙️ Step 4: Test Using Telnet

Alternative test:
```bash
telnet 192.168.10.10 8080
```

If successful:
```
Trying 192.168.10.10...
Connected to 192.168.10.10.
```

If not:
```
telnet: Unable to connect to remote host: Connection refused
```

---

### ⚙️ Step 5: Check Firewall Rules

If connection fails:
```bash
sudo iptables -L -n -v
# or
sudo firewall-cmd --list-all
```

---

### ⚙️ Step 6: Test File Transfer with Netcat

On **server1**:
```bash
nc -l 9000 > received.txt
```

On **client1**:
```bash
nc 192.168.10.10 9000 < file.txt
```

✅ The file `file.txt` will be transferred to the server as `received.txt`.

---

## 🧭 Summary

| Tool | Purpose | Notes |
|------|----------|-------|
| `nc` | General-purpose network testing & data transfer | Supports both TCP and UDP |
| `telnet` | Simple TCP connectivity test | For quick service checks |
| `iptables` / `firewall-cmd` | Firewall rule verification | Ensure the port is open |
| `ip route` | Routing path validation | Confirms gateway or subnet reachability |

---

## 🔍 Quick Takeaway

> **Netcat** and **Telnet** are essential diagnostic tools for network engineers.  
> They help verify service availability, connectivity, and firewall configurations — all from the terminal.

