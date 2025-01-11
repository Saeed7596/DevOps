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

