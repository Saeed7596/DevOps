# **Linux Networking Commands and Configuration Files**

| Command/File | Description | Example |
|-------------|------------|---------|
| `ip a` / `ip link` | Displays the status of network interfaces (UP/DOWN, MAC address). | `ip a` - `ip a show eth0` |
| `ip addr` | Shows IP addresses assigned to interfaces. | `ip addr` |
| `ip addr show <interface>` | Shows IP addresses assigned to interfaces. | `ip addr show weave` |
| `ip addr add <IP>/CIDR dev <interface>` | Assigns an IP address to a network interface temporarily. | `ip addr add 192.168.1.10/24 dev eth0` |
| `route` | Displays the system's routing table (deprecated). | `route -n` |
| `ip route` | Shows or manipulates the routing table (replacement for `route`). | `ip route show` |
| `ip route add <network> via <gateway>` | Adds a new route to the routing table. | `ip route add 192.168.1.0/24 via 192.168.2.1` |
| `cat /proc/sys/net/ipv4/ip_forward` | Checks if IP forwarding is enabled (`0` = disabled, `1` = enabled). | `cat /proc/sys/net/ipv4/ip_forward` |
| `echo 1 > /proc/sys/net/ipv4/ip_forward` | Enables IP forwarding temporarily. | `echo 1 > /proc/sys/net/ipv4/ip_forward` |
| `sysctl -w net.ipv4.ip_forward=1` | Enables IP forwarding temporarily using `sysctl`. | `sysctl -w net.ipv4.ip_forward=1` |
| `echo "net.ipv4.ip_forward = 1" >> /etc/sysctl.conf && sysctl -p` | Enables IP forwarding permanently. | `echo "net.ipv4.ip_forward = 1" >> /etc/sysctl.conf && sysctl -p` |
| `/etc/hosts` | Local file for mapping domain names to IP addresses before DNS resolution. | `127.0.0.1 localhost` |
| `/etc/resolv.conf` | Specifies DNS servers for domain name resolution. | `nameserver 8.8.8.8` | 
| `nslookup`         | A tool to query DNS servers to obtain domain name or IP address mapping. | nslookup google.com |
| `dig`              | A DNS lookup tool for querying domain names and their associated IP addresses. | dig google.com |
| `ping`             | Used to test the connectivity between the local machine and remote systems.    | ping 8.8.8.8 |
| `trace`            | A network diagnostic tool used to trace the route packets take to a remote host. | traceroute google.com |
|`ip netns list`     | This lists all network namespaces on the system. |
|`tcpdump -l`        | data-network packet analyzer |
|`netstat -plnt`     | This shows all active listening TCP connections along with the associated processes. | - -p: Show the process using each socket. - -l: Show only listening sockets. - -n: Show numerical addresses (don’t resolve hostnames). - -t: Show TCP connections.|
|`arp`| The arp command is used to display and manipulate the system's ARP (Address Resolution Protocol) cache, which maps IP addresses to MAC (hardware) addresses.| `arp -a` |
---

# **How to Set Permanent Static IP on Linux**

To configure a permanent static IP on Linux systems, you need to modify network configuration files. Below are the methods for different Linux distributions to make the changes persistent across reboots.

---

## **1️⃣ Setting Permanent Static IP on Ubuntu/Debian (with Netplan)**

In Ubuntu 18.04 and later, `netplan` is used for network configuration.

### **Steps to Set Permanent Static IP:**

1. **Edit the Netplan configuration file:**
   Netplan configuration files are located in `/etc/netplan/`. Edit one of the files:
   ```sh
   sudo nano /etc/netplan/50-cloud-init.yaml
   ```

2. **Configure Static IP:**
   Add the following configuration to set a static IP:
   ```yaml
   network:
     version: 2
     renderer: networkd
     ethernets:
       eth0:
         dhcp4: no        # Disable DHCP
         addresses:
           - 192.168.1.10/24  # Set static IP
         gateway4: 192.168.1.1  # Set Gateway
         nameservers:
           addresses:
             - 8.8.8.8         # Set DNS
             - 8.8.4.4
   ```

3. **Apply Changes:**
   Save the file and apply the changes:
   ```sh
   sudo netplan apply
   ```

---

## **2️⃣ Setting Permanent Static IP on CentOS/RHEL (with Network-Scripts)**

In CentOS and RHEL, network configuration is done using **network-scripts**.

### **Steps to Set Permanent Static IP:**

1. **Edit the Interface Configuration File:**
   The configuration file for network interfaces is located in `/etc/sysconfig/network-scripts/`. Edit the file for your interface (e.g., `ifcfg-eth0`):
   ```sh
   sudo nano /etc/sysconfig/network-scripts/ifcfg-eth0
   ```

2. **Configure Static IP:**
   Modify the file as follows:
   ```ini
   BOOTPROTO=none        # Disable DHCP
   ONBOOT=yes            # Enable interface at boot
   IPADDR=192.168.1.10   # Set static IP
   PREFIX=24             # Set subnet mask (255.255.255.0)
   GATEWAY=192.168.1.1   # Set Gateway
   DNS1=8.8.8.8          # Set DNS
   DNS2=8.8.4.4
   ```

3. **Restart Network Service:**
   After saving the file, restart the network service to apply changes:
   ```sh
   sudo systemctl restart network
   ```

---

## **3️⃣ Setting Permanent Static IP on Older Systems (using `ifconfig`)**

For older systems, network configuration is done through `/etc/network/interfaces` or similar files.

### **Steps to Set Permanent Static IP:**

1. **Edit the Interface Configuration File:**
   In some older systems, you may configure network settings in `/etc/network/interfaces`:
   ```sh
   sudo nano /etc/network/interfaces
   ```

2. **Configure Static IP:**
   Modify the file to look like this:
   ```ini
   iface eth0 inet static
   address 192.168.1.10
   netmask 255.255.255.0
   gateway 192.168.1.1
   dns-nameservers 8.8.8.8 8.8.4.4
   ```

3. **Restart Network Service:**
   After saving the file, restart the networking service:
   ```sh
   sudo systemctl restart networking
   ```

---

## **4️⃣ Enabling IP Forwarding Permanently**

To enable IP forwarding permanently, you need to modify the `/etc/sysctl.conf` file.

### **Steps to Enable IP Forwarding:**

1. **Edit the `sysctl.conf` file:**
   Open the file `/etc/sysctl.conf`:
   ```sh
   sudo nano /etc/sysctl.conf
   ```

2. **Enable IP Forwarding:**
   Add or modify the following line:
   ```ini
   net.ipv4.ip_forward = 1
   ```

3. **Apply Changes:**
   Apply the changes by running:
   ```sh
   sudo sysctl -p
   ```

---

## **5️⃣ Configuring DNS Permanently**

To configure DNS servers permanently:

### **Steps for Ubuntu/Debian:**

1. **Edit the `resolved.conf` file:**
   Open `/etc/systemd/resolved.conf`:
   ```sh
   sudo nano /etc/systemd/resolved.conf
   ```

2. **Set DNS Servers:**
   Add the following DNS settings:
   ```ini
   DNS=8.8.8.8 8.8.4.4
   FallbackDNS=1.1.1.1
   ```

3. **Restart the systemd-resolved service:**
   Apply changes by restarting the service:
   ```sh
   sudo systemctl restart systemd-resolved
   ```

---

## **6️⃣ Verifying Permanent Static IP**

After setting the static IP, use the following commands to verify that your settings are applied correctly:

### **Check IP Address:**
```sh
ip addr show
```
or, for older systems:
```sh
ifconfig
```

---

## **Conclusion:**
- **Ubuntu/Debian (Netplan):** Edit the file `/etc/netplan/*.yaml`.
- **CentOS/RHEL:** Edit the file `/etc/sysconfig/network-scripts/ifcfg-eth0`.
- **Older Systems:** Edit the file `/etc/network/interfaces`.
- **Permanent IP Forwarding:** Modify `/etc/sysctl.conf` and run `sysctl -p`.
- **Permanent DNS Configuration:** Use `/etc/systemd/resolved.conf` or `/etc/resolv.conf`.

🚀 **These methods will ensure that your static IP configuration persists after reboot!**

---

# Add DNS Manually
```
echo "nameserver 178.22.122.100" | sudo tee /etc/resolv.conf
echo "nameserver 185.51.200.2" | sudo tee /etc/resolv.conf
```
## Or 
### Set Custom DNS on Fedora / RHEL / CentOS (with NetworkManager):
1. Find Connection NAME:
```bash
nmcli con show
```
2. Set custom DNS:
```bash
nmcli con mod "<connection-name>" ipv4.dns "178.22.122.100 185.51.200.2"
```
3. Ignore automatic DNS:
```bash
nmcli con mod "<connection-name>" ipv4.ignore-auto-dns yes
```
4. Restart connection:
```bash
nmcli con down "<connection-name>" && nmcli con up "<connection-name>"
```
### Network Manager Text User Interface
```bash
nmtui 
```

---

### Set Custom DNS on Debian / Ubuntu (with systemd-resolved):
```bash
sudo nano /etc/systemd/resolved.conf
```
Inside the `[Resolve]` section, add or modify the following lines:
```conf
[Resolve]
DNS=178.22.122.100 185.51.200.2
FallbackDNS=8.8.8.8
```
Restart the systemd-resolved service
```bash
sudo systemctl restart systemd-resolved
```
Symlink the correct resolv.conf
```bash
sudo ln -sf /run/systemd/resolve/resolv.conf /etc/resolv.conf
```

---

# Full Network Reset + Cache Clean
```bash
# 1. Restart NetworkManager
sudo systemctl restart NetworkManager

# 2. Clean DNS cache
sudo systemd-resolve --flush-caches

# 3. Restart DNS resolver
sudo systemctl restart systemd-resolved

# 4. Clean DNF cache completely
sudo dnf clean all
sudo rm -rf /var/cache/dnf
sudo dnf makecache

# 5. Release and renew DHCP IP
sudo dhclient -r
sudo dhclient

# 6. Test DNS and repo connectivity
ping -c 3 google.com
dnf repolist
```
