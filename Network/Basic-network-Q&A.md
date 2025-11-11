# Networking Questions and Answers

## OSI Model

### **What are the OSI layers?**

The OSI (Open Systems Interconnection) model describes seven layers for standardizing communication between networked devices:

1. **Physical Layer:** Responsible for transmitting raw data bits over a physical medium.
2. **Data Link Layer:** Handles error detection, correction, and framing (e.g., Ethernet).
3. **Network Layer:** Manages routing and addressing (e.g., IP).
4. **Transport Layer:** Ensures reliable data transfer through protocols like TCP or UDP.
5. **Session Layer:** Manages sessions and dialogs between applications.
6. **Presentation Layer:** Formats and encrypts data for the application layer.
7. **Application Layer:** Provides network services to end-users (e.g., HTTP, FTP).

---


# The 7 Layers of the OSI Model

The **OSI Model (Open Systems Interconnection)** is a conceptual framework used to understand and standardize how different networking systems communicate. It divides the communication process into **seven distinct layers**, each with specific functions and responsibilities.

---

## 1. Physical Layer (Layer 1)
**Purpose:** Transmits raw bit streams over a physical medium.

**Key Functions:**
- Defines hardware elements (cables, switches, network cards).
- Deals with voltage levels, data rates, and physical connections.
- Converts binary data into signals (electrical, optical, or radio).

**Examples:** Ethernet cables, fiber optics, hubs, repeaters.

---

## 2. Data Link Layer (Layer 2)
**Purpose:** Provides node-to-node data transfer and error detection.

**Key Functions:**
- Frames data for transmission.
- Detects and may correct errors that occur in the physical layer.
- Uses MAC (Media Access Control) addresses.

**Examples:** Switches, bridges, Ethernet (IEEE 802.3), PPP.

---

## 3. Network Layer (Layer 3)
**Purpose:** Handles routing and forwarding of data packets between devices.

**Key Functions:**
- Logical addressing using IP addresses.
- Determines the best path for data delivery.
- Manages packet fragmentation and reassembly.

**Examples:** Routers, IP (IPv4/IPv6), ICMP.

---

## 4. Transport Layer (Layer 4)
**Purpose:** Ensures reliable data transfer between systems.

**Key Functions:**
- Segments data and ensures complete delivery.
- Provides error recovery and flow control.
- Supports both connection-oriented (TCP) and connectionless (UDP) protocols.

**Examples:** TCP, UDP, SSL/TLS.

---

## 5. Session Layer (Layer 5)
**Purpose:** Manages and controls the connections (sessions) between applications.

**Key Functions:**
- Establishes, maintains, and terminates sessions.
- Synchronizes dialogue between systems.

**Examples:** NetBIOS, PPTP, RPC.

---

## 6. Presentation Layer (Layer 6)
**Purpose:** Translates data between the application and the network.

**Key Functions:**
- Converts data formats (encryption, compression, encoding).
- Ensures that data from the application layer of one system can be read by the application layer of another.

**Examples:** SSL, JPEG, MPEG, GIF.

---

## 7. Application Layer (Layer 7)
**Purpose:** Provides network services directly to end users and applications.

**Key Functions:**
- Interfaces with software applications.
- Handles protocols like HTTP, SMTP, FTP, DNS, and POP3.

**Examples:** Web browsers, email clients, file transfer programs.

---

## Summary Table

| Layer | Name         | Function  | Example Protocols / Devices   |
|-------|--------------|-----------|------------------------------|
| 7     | Application  | User interface and services - End User Layer | HTTP, FTP, IRC, SMTP, SSH, DNS |
| 6     | Presentation | Data translation, encryption - Syntax Layer | SSL, SSH, IMAP, FTP, JPEG, MPEG |
| 5     | Session      | Connection management - Synch & Send to Port | API's, Socket, WinSock, RPC, NetBIOS |
| 4     | Transport    | Reliable data transfer - End-to-end Connections | TCP, UDP |
| 3     | Network      | Routing and addressing - Packets | IP, ICMP, IPSec, IGMP, Routers |
| 2     | Data Link    | Node-to-node delivery - Frames | Ethernet, Switch, Bridge, PPP |
| 1     | Physical     | Transmission of bits - Physical Structure | Cables (Coax, Fiber), Wireless, Hubs, Repeaters |

---

## TCP vs UDP

### **Differences between TCP and UDP**

| **Feature**     | **TCP**                              | **UDP**                                   |
| --------------- | ------------------------------------ | ----------------------------------------- |
| Connection Type | Connection-oriented                  | Connectionless                            |
| Reliability     | Ensures delivery via acknowledgments | No guarantees for delivery                |
| Speed           | Slower due to reliability features   | Faster as there are no reliability checks |
| Use Cases       | Web browsing, email, file transfer   | Video streaming, gaming, VoIP             |

---

## Common Networking Protocols

1. **HTTP/HTTPS:** For web communication.
2. **FTP:** File transfer between systems.
3. **SMTP:** Sending emails.
4. **DNS:** Resolves domain names to IP addresses.
5. **DHCP:** Dynamically assigns IP addresses to devices.
6. **SSH:** Secure remote login.

---

## DNS (Domain Name System)

**What is DNS?**
DNS translates human-readable domain names (e.g., `example.com`) into IP addresses (e.g., `192.168.1.1`) so computers can communicate.

**Key Components of DNS:**

- **Resolver:** Client-side that sends requests.
- **Root Servers:** Directs requests to Top-Level Domains (TLDs).
- **TLD Servers:** Directs to authoritative servers for specific domains.
- **Authoritative Server:** Provides the final IP address.

---

## DHCP (Dynamic Host Configuration Protocol)

**What is DHCP?**
DHCP automatically assigns IP addresses and other network configurations (subnet mask, gateway, DNS) to devices in a network. It simplifies network management by eliminating manual IP configuration.

---

## `UDP` vs `TCP` and Addressing Types

### UDP (User Datagram Protocol) is like shouting in a hall:

* “Saeed, come have some ice cream!”
* Maybe Saeed hears it, maybe he doesn’t — but you still sent the message.
* UDP sends data without establishing a connection (`Connectionless`) and does not guarantee delivery, order, or reliability.

### TCP (Transmission Control Protocol) is like having a proper conversation:

* “Saeed, come have some ice cream.”
* “Saeed, did you hear me?”
* “Yes, I heard you.”
* TCP ensures that data is delivered reliably, in the correct order, and that both sides confirm successful communication.(`Connection-oriented`)

### There are also two common communication types:

* `Unicast`: Sending data to a single, specific destination (e.g., just to Saeed).

* `Broadcast`: Sending data to all devices on the local network simultaneously.

---

## IP Addressing

### **What is an IP address?**

An IP (Internet Protocol) address is a unique identifier assigned to devices on a network to facilitate communication.

### **Types of IP Addresses**

1. **IPv4:**

   - 32-bit address (e.g., `192.168.1.1`).
   - Divided into classes (A, B, C, D, E).

2. **IPv6:**

   - 128-bit address (e.g., `2001:0db8::7334`).
   - Designed to overcome IPv4 limitations.

### **IPv4 Classes Overview**

| **Class** | **Range**                   | **Network Bits** | **Host Bits** |
| --------- | --------------------------- | ---------------- | ------------- |
| A         | 0.0.0.0 - 127.255.255.255   | 8                | 24            |
| B         | 128.0.0.0 - 191.255.255.255 | 16               | 16            |
| C         | 192.0.0.0 - 223.255.255.255 | 24               | 8             |

---

| **Class**  | **First Octet** | **Number of Subnets**    | **Number of Hosts**         | **Description**                         |
|------------|-----------------|--------------------------|-----------------------------|-----------------------------------------|
| Class A    | 1 to 126        | 126                      | Approximately 16.7 million  | Many hosts per network.                |
| Class B    | 128 to 191      | 16,384                   | 65,536                      | Many hosts per network.                |
| Class C    | 192 to 223      | Approximately 2.1 million| 254                         | Many networks with fewer hosts per network. |
| Class D    | 224 to 239      | n/a                      | n/a                         | Multicasting.                          |
| Class E    | 240 to 254      | n/a                      | n/a                         | Experimental.                          |

---

### **Special IP Address Ranges**

1. **Private IPs:**

   - Not routable on the **`internet`**.
   - Examples:
     - `10.0.0.0/8`
     - `172.16.0.0/12`
     - `192.168.0.0/16`

| **Name**     | **CIDR block**  | **Address range**             | **Number of addresses** | *Classful description***               |
| ------------ | --------------- | ----------------------------- | ----------------------- | -------------------------------------- |
| 24-bit block	| 10.0.0.0/8      | 10.0.0.0 – 10.255.255.255     | 16777216                | Single Class A                         |
| 20-bit block | 172.16.0.0/12   | 172.16.0.0 – 172.31.255.255   | 1048576                 | Contiguous range of 16 Class B blocks  |
| 16-bit block | 192.168.0.0/16  | 192.168.0.0 – 192.168.255.255 | 65536                   | Contiguous range of 256 Class C blocks |

2. **Loopback:** `127.0.0.1` for local testing.

3. **APIPA:** `169.254.0.0/16` for auto-configuration when DHCP fails.

---

## Additional Networking Topics

### **What is the difference between static and dynamic IPs?**

- **Static IP:** Manually assigned, fixed address. Often used for servers.
- **Dynamic IP:** Assigned by DHCP. Changes periodically.

---

### **What is a subnet?**

A subnet divides a large network into smaller, manageable sections. Each subnet has its own unique IP range, defined by a subnet mask (e.g., `255.255.255.0`).

---

### Structure of an IP Address

#### Every IP address is divided into two parts:
* `Network` part: Identifies the network segment and is the same for all devices within that network.
* `Host` part: Identifies a specific device within the network and is unique to each one.

Since IP addresses are stored in binary form, they are represented in a `decimal` (base-10) format for readability — for example, 192.168.1.101.

##### When we write an IP address as 1`92.168.1.101/24`, the `“/24”` indicates the `subnet mask`.
##### A `/24` means the subnet mask is `255.255.255.0`, which corresponds to `24 ones` in binary form:
```bash
11111111.11111111.11111111.00000000
```

This means the `first 24 bits` represent the `network` portion, and the remaining `8 bits` represent the `host` portion.

---
## Questions
### Which of the following is a valid IP address for a network interface?
- A) 192.168.10.0/24

- B) 10.10.10.255/24

- C) 256.10.10.10/24

- D) 56.41.26.8/15

| **Option**        | **Analysis** | **Valid?** |
| ----------------- | -------------------------------------------------------------------------------------------------------------- | -- | 
| `192.168.10.0/24` | **The `last octet` is `0`**, which represents the network address. It cannot be assigned to a `host`.          | ❌ |
| `10.10.10.255/24` | **The `last octet` is `255`, which is the `broadcast address` for this subnet. It cannot be used by a host.    | ❌ |
| `256.10.10.10/24` | Invalid, because `256` is not a valid octet value in IPv4 (the range is `0–255`).                              | ❌ |
| `56.41.26.8/15`   | All octets are within valid range, and this address is not the network or broadcast address in the /15 subnet. | ✅ |

##### ✅ Correct Answer: `56.41.26.8/15` is a valid IP address for a network interface.

---

## Understanding `Routing` and IP Communication
**When all devices share IP addresses `within the same range`, they can communicate directly and ping each other without needing a router.**
**However, if a device is located `outside` the local network, `routing is required` to reach it.**

In Linux, you can view or manage routing tables using the ip route command.

Example:
```nginx
Device A = 10.10.10.5/24
Device B = 10.10.10.10/24
Device C = 5.5.5.1/24
```

**Devices A and B are in the same subnet, so they can communicate directly.**
**But A cannot reach C because they belong to different networks.**

##### To add a route from A to C, we use:
```bash
ip route add 5.5.5.0/24 dev eth0
```

**This allows A to send packets toward the 5.5.5.0/24 network.**
**However, since C has no return route, it can receive the packets but `cannot reply`.**

**So, we must also add a route on C:**
```bash
ip route add 10.10.10.0/24 dev eth0
```
Or (It's work also too)
```bash
ip route add 10.10.0.0/16 dev eth0
```

**Now both directions are defined, and communication can occur successfully.**

---

## Default Route

**When a device is connected to a router, default routes are usually added automatically.**
**To manually define a default route in Linux, use:**
```bash
ip route add default dev eth0
```
# 🔹 This is the common and correct way to define a Default Route.
```bash
sudo ip route add default via <gateway-ip> dev eth0
```

**The default route acts as a fallback path:**
**If the destination IP address does not match any specific route in the routing table, the packet is sent through this default route.**

##### Purpose:
This command adds a `specific route` for a single host (identified by its exact IP address) and tells the system to send packets to that host via a particular gateway using the specified `network interface`.
```bash
ip route add <source-ip/32> via <default-gateway> dev eth0
```
* Breakdown:
   * `<source-ip/32>` → The destination IP address with a `/32` subnet mask, meaning **`only that exact IP`** (a single host route).
   * `via <default-gateway>` → Specifies the **`next hop (gateway)`** that should be used to reach the destination.
   * `dev eth0` → Defines the `network interface` (e.g., eth0) through which the traffic should be sent.

Example:
```bash
ip route add 10.10.20.5/32 via 192.168.1.1 dev eth0
```
* Means: To reach the host `10.10.20.5`, send packets through the gateway `192.168.1.1` using the `eth0` interface.

### Add Permanent
```bash
sudo nmtui
```
### Edit eth0 -> Route -> 
* Destination/Perfix = <source-ip/32>
* Next Hop = default-gateway
* Metric -> Empty

### Verify
```bash
ip route
sudo nft list ruleset 
```

---

## Summary of Key Concepts

* `IP Address`: A `unique` identifier assigned to a device on a network. It consists of a `network part` and a `host part`.

* `Subnet Mask`: Defines which portion of the IP address represents the network and which part represents the host.
   * Example: `/24 → 255.255.255.0` means the first 24 bits are for the `network`.

* `Default Gateway`: The device (usually a router) that forwards packets from the local network to external networks or the internet.
   * If a packet’s destination is outside the local subnet, it is sent to the default gateway.

---

### **What is NAT (Network Address Translation)?**

NAT is a technique used to modify network address information in IP headers. It enables:

- Sharing a single public IP among multiple devices.
- Improved security by hiding internal IPs.

---

### **What are VLANs (Virtual LANs)?**

VLANs logically segment networks into isolated sections, enhancing security and reducing broadcast traffic.

---

### **What is a firewall?**

A firewall is a security system that monitors and controls incoming and outgoing network traffic. It operates using predefined security rules to protect the network.

---

