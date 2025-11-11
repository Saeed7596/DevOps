
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
sudo iptables -L -n -v
sudo nft list ruleset
sudo ufw status verbose
```

**Interpretation:**
- DROP/REJECT rules may block outgoing/incoming packets.

---

## Step 9 — Packet Capture
**Purpose:** Verify packet flow and response.

```bash
sudo tcpdump -n -i eth0 host 8.8.8.8 -w /tmp/cap.pcap
sudo tcpdump -n -i eth0 icmp
```

**Interpretation:**
- Requests sent but no reply → remote issue.
- No packets sent → local routing/firewall problem.

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
