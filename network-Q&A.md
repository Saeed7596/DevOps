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

| **Class** | **Range**                 | **Network Bits** | **Host Bits** |
| --------- | ------------------------- | ---------------- | ------------- |
| A         | 1.0.0.0 - 126.0.0.0       | 8                | 24            |
| B         | 128.0.0.0 - 191.255.0.0   | 16               | 16            |
| C         | 192.0.0.0 - 223.255.255.0 | 24               | 8             |

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

   - Not routable on the internet.
   - Examples:
     - `10.0.0.0/8`
     - `172.16.0.0/12`
     - `192.168.0.0/16`

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

