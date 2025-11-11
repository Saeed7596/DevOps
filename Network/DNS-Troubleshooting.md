# DNS Troubleshooting with dig, nslookup, and dnsmasq

This document provides an overview of **dig**, **nslookup**, and **dnsmasq**, including useful commands, flag explanations, and interpretation of outputs.

---

## 🧩 Common Tools

| Tool | Purpose | Typical Use |
|------|----------|-------------|
| `dig` | Detailed DNS query tool | Troubleshooting DNS records and latency |
| `nslookup` | Simple DNS query tool | Quick resolution lookups |
| `dnsmasq` | Lightweight DNS/DHCP server | Local caching and forwarding of DNS queries |

---

## ⚙️ dig (Domain Information Groper)

### Example Commands

```bash
# Query A record
dig example.com

# Query specific record type
dig example.com MX

# Use a specific DNS server
dig @8.8.8.8 example.com

# Display only answer section
dig +short example.com

# Query all available record types
dig example.com ANY

# Trace DNS delegation path
dig +trace example.com
```

### Useful Flags

| Flag | Description | Example |
|------|--------------|----------|
| `+short` | Shows only brief results | `dig +short example.com` |
| `+trace` | Traces the query path through all DNS servers | `dig +trace example.com` |
| `+noall +answer` | Display only the answer section | `dig +noall +answer example.com` |
| `@dns-server` | Use a custom DNS server | `dig @1.1.1.1 example.com` |
| `-t TYPE` | Specify record type (A, AAAA, MX, TXT, etc.) | `dig -t MX example.com` |

### Common Output Sections

| Section | Meaning |
|----------|----------|
| **HEADER** | Includes status codes like `NOERROR`, `NXDOMAIN`, etc. |
| **QUESTION SECTION** | The query you sent (domain and record type). |
| **ANSWER SECTION** | The resolved IP or record data. |
| **AUTHORITY SECTION** | Lists authoritative DNS servers for the domain. |
| **ADDITIONAL SECTION** | Extra information, e.g., IPs of name servers. |

### Common Status Codes

| Status | Meaning |
|---------|----------|
| `NOERROR` | Query successful. |
| `NXDOMAIN` | Domain does not exist. |
| `SERVFAIL` | DNS server failed to answer. |
| `REFUSED` | Request was refused by the server. |
| `FORMERR` | Format error in the query. |
| `TIMEOUT` | No response received. |

---

## ⚙️ nslookup

### Example Commands

```bash
# Query A record
nslookup example.com

# Query a specific record type
nslookup -query=MX example.com

# Use a specific DNS server
nslookup example.com 1.1.1.1

# Interactive mode
nslookup
> set type=TXT
> example.com
```

### Common Output Fields

| Field | Meaning |
|--------|----------|
| **Server:** | The DNS server used to perform the lookup. |
| **Address:** | IP of the DNS server queried. |
| **Non-authoritative answer:** | Response is from cache, not the authoritative source. |
| **Name:** | The queried domain name. |
| **Address:** | IP address returned. |
| **Aliases:** | CNAME records associated with the domain. |

### Useful Flags

| Flag | Description | Example |
|------|--------------|----------|
| `-query=<type>` | Specify record type | `nslookup -query=AAAA example.com` |
| `-debug` | Print detailed debugging information | `nslookup -debug example.com` |
| `-timeout=<sec>` | Set query timeout | `nslookup -timeout=5 example.com` |

---

## ⚙️ dnsmasq

`dnsmasq` acts as a lightweight DNS forwarder and cache.

### Common Commands

```bash
# Check dnsmasq version
dnsmasq -v

# Start dnsmasq service
sudo systemctl start dnsmasq

# Enable dnsmasq at boot
sudo systemctl enable dnsmasq

# Check logs
journalctl -u dnsmasq

# Test a query (if dnsmasq is listening on 127.0.0.1)
dig @127.0.0.1 example.com
```

### Log Output Meaning

| Example Log | Meaning |
|--------------|----------|
| `dnsmasq: query[A] example.com from 127.0.0.1` | Received an A record query. |
| `dnsmasq: forwarded example.com to 8.8.8.8` | Query forwarded to upstream DNS. |
| `dnsmasq: reply example.com is 93.184.216.34` | Received a valid reply. |
| `dnsmasq: cached example.com is 93.184.216.34` | Response served from local cache. |

---

## ✅ Summary Table

| Action | dig | nslookup | dnsmasq |
|---------|-----|-----------|----------|
| Query a domain | `dig example.com` | `nslookup example.com` | `dig @127.0.0.1 example.com` |
| Specify DNS server | `dig @8.8.8.8` | `nslookup example.com 8.8.8.8` | `server=<IP>` in config |
| Trace DNS resolution | `dig +trace example.com` | — | — |
| Check cached records | — | — | Logs show cached replies |
| View only answer | `dig +short` | — | — |

---

## 🧠 Pro Tips

- Always check `/etc/resolv.conf` to confirm which DNS servers your system is using.  
- Combine `dig` with `+trace` to debug domain delegation problems.  
- Use `dnsmasq` when you need a small, efficient caching DNS service for labs or edge devices.

