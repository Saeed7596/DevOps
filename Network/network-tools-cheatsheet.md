# Network Troubleshooting Command Cheatsheet

A quick reference for commonly used network diagnostic tools: `ip`, `route`, `ping`, `traceroute`, `nslookup`, `dig`, and `tcpdump`.

---

## 🧭 IP Command

| Purpose | Command | Description |
|----------|----------|-------------|
| Show all interfaces and IPs | `ip addr show` | Lists IPs assigned to interfaces |
| Show interface link status | `ip link show` | Displays interface state (UP/DOWN) |
| Bring interface up/down | `ip link set eth0 up` / `ip link set eth0 down` | Enables or disables an interface |
| Show routing table | `ip route show` | Lists current routes |
| Add default route | `sudo ip route add default via <gateway-ip> dev eth0` | Adds default gateway |
| Delete default route | `sudo ip route del default` | Removes default gateway |
| Add route to specific network | `sudo ip route add 10.10.10.0/24 dev eth0` | Adds route for subnet |
| Add host route | `sudo ip route add <ip>/32 via <gateway>` | Route to a single host |

---

## 🗺️ Route Command (legacy alternative)

| Purpose | Command | Description |
|----------|----------|-------------|
| Show routing table | `route -n` | Legacy equivalent of `ip route show` |
| Add route | `sudo route add -net 10.10.10.0 netmask 255.255.255.0 gw 192.168.1.1` | Adds a network route |
| Delete route | `sudo route del -net 10.10.10.0/24 gw 192.168.1.1` | Removes a network route |

---

## 🛰️ Ping

| Purpose | Command | Description |
|----------|----------|-------------|
| Ping host | `ping <host>` | Tests reachability |
| Ping specific IP | `ping 8.8.8.8` | Tests connectivity to Google DNS |
| Limit number of packets | `ping -c 4 <host>` | Sends 4 ICMP packets |
| Use specific interface | `ping -I eth0 8.8.8.8` | Sends via specified interface |
| Flood ping (stress test) | `sudo ping -f <host>` | Sends packets rapidly (use with care) |

---

## 🧭 Traceroute

| Purpose | Command | Description |
|----------|----------|-------------|
| Basic route trace | `traceroute <host>` | Shows hops to destination |
| Numeric only | `traceroute -n <host>` | Disables DNS lookup for faster output |
| ICMP-based | `traceroute -I <host>` | Uses ICMP echo instead of UDP |
| TCP-based (common for firewalls) | `traceroute -T -p 80 <host>` | Uses TCP packets on port 80 |
| Continuous tracing | `mtr <host>` | Interactive traceroute with live stats |

---

## 🌐 nslookup

| Purpose | Command | Description |
|----------|----------|-------------|
| Basic lookup | `nslookup example.com` | Resolves domain to IP |
| Reverse lookup | `nslookup 8.8.8.8` | Resolves IP to domain |
| Query specific DNS server | `nslookup example.com 1.1.1.1` | Uses Cloudflare DNS |
| Interactive mode | `nslookup` → then type `set type=MX`, `example.com` | Used for deeper DNS testing |

---

## 🔎 dig

| Purpose | Command | Description |
|----------|----------|-------------|
| Basic lookup | `dig example.com` | Resolves domain name |
| Short answer | `dig +short example.com` | Displays only IP |
| Query specific DNS server | `dig @1.1.1.1 example.com` | Queries Cloudflare DNS directly |
| MX records | `dig example.com MX` | Retrieves mail server records |
| NS records | `dig example.com NS` | Lists name servers |
| Reverse lookup | `dig -x 8.8.8.8` | IP to domain lookup |
| Trace DNS resolution | `dig +trace example.com` | Shows entire DNS resolution path |

---

## 🧰 tcpdump

| Purpose | Command | Description |
|----------|----------|-------------|
| Capture all traffic | `sudo tcpdump -i eth0 -n` | Shows all packets on interface |
| Capture and save to file | `sudo tcpdump -i eth0 -n -w capture.pcap` | Writes packets to a file |
| Filter by host | `sudo tcpdump -i eth0 host 8.8.8.8` | Traffic to/from specific IP |
| Filter by source/destination | `sudo tcpdump -i eth0 src 10.0.0.1` / `dst 8.8.8.8` | Source or destination filters |
| Filter by protocol | `sudo tcpdump -i eth0 icmp` | Only ICMP packets (e.g., ping) |
| Filter by port | `sudo tcpdump -i eth0 port 80` | HTTP traffic |
| TCP on custom port | `sudo tcpdump -i eth0 'tcp port 2222' -nn -vv -s 0` | Detailed view of TCP port 2222 |
| Capture DNS | `sudo tcpdump -i eth0 port 53` | Shows DNS requests/responses |
| Capture ARP | `sudo tcpdump -i eth0 arp` | Monitors ARP requests |
| Capture HTTP | `sudo tcpdump -i eth0 'tcp port 80 or port 443'` | Captures HTTP/HTTPS |
| Display live traffic but not resolve | `sudo tcpdump -n -i eth0` | Faster output without DNS lookup |
| Read from saved file | `sudo tcpdump -r capture.pcap` | Reads stored capture |

---

## ⚙️ Quick Tips

- Use `-n` to disable DNS lookups (faster output).  
- Use `-vv` or `-vvv` for more detailed protocol headers.  
- Use `-s 0` to capture full packets (not truncated).  
- Combine filters: `tcpdump -i eth0 'src 10.0.0.1 and port 22'`.  
- Stop capturing with `Ctrl + C`.

---

## 🧩 Useful Combos

| Use Case | Example Command |
|-----------|----------------|
| Debug DNS | `dig +trace example.com` |
| Capture ICMP and save | `sudo tcpdump -i eth0 icmp -w icmp.pcap` |
| Check default route | `ip route show | grep default` |
| Test connectivity | `ping -c 4 8.8.8.8` |
| Visual route test | `mtr 8.8.8.8` |

---

### 🧠 Pro Tip
Combine these tools logically:
1. `ip addr` → Check if you have an IP.  
2. `ip route` → Verify default route.  
3. `ping <gateway>` → Test local reachability.  
4. `ping 8.8.8.8` → Test internet access.  
5. `nslookup google.com` → Verify DNS.  
6. `tcpdump icmp` → Watch actual ping traffic.

---
