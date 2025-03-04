# **Linux Networking Commands and Configuration Files**

| Command/File | Description | Example |
|-------------|------------|---------|
| `ip link` | Displays the status of network interfaces (UP/DOWN, MAC address). | `ip link` |
| `ip addr` | Shows IP addresses assigned to interfaces. | `ip addr` |
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

