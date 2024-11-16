# Network Buffer Settings Optimization for Linux

This document provides a step-by-step guide on checking and adjusting the network buffer settings on a Linux system. It helps optimize the system for handling network traffic, especially in high-throughput environments.

## Prerequisites

- You need to have root (administrator) privileges on the system to modify kernel parameters.
- Ensure that `sysctl` is installed and accessible on your system.

## Step 1: Check Current Network Buffer Settings

Before making any changes, let's check the current values of the network buffer settings to understand the baseline.

Run the following commands to check the current values:

```bash
sysctl net.core.rmem_default
sysctl net.core.wmem_default
sysctl net.core.rmem_max
sysctl net.core.wmem_max
```
Sample Output:
```bash
net.core.rmem_default = 4096
net.core.wmem_default = 4096
net.core.rmem_max = 16777216
net.core.wmem_max = 16777216
```
`rmem_default`: Default size of the receive buffer (in bytes).
`wmem_default`: Default size of the send buffer (in bytes).
`rmem_max`: Maximum size of the receive buffer (in bytes).
`wmem_max`: Maximum size of the send buffer (in bytes).
If the values are too low for your use case (e.g., large file transfers, high network traffic), consider increasing them.

## Step 2: Update Network Buffer Settings
To adjust the network buffer settings for better performance, you can modify the kernel parameters using sysctl.

### Apply Changes Temporarily
To apply the new values temporarily (without reboot), use the following commands:
```bash
sudo sysctl -w net.core.rmem_default=10000000
sudo sysctl -w net.core.wmem_default=10000000
sudo sysctl -w net.core.rmem_max=16777216
sudo sysctl -w net.core.wmem_max=16777216
```
### Apply Changes Permanently
To make these changes persistent across system reboots, add them to the /etc/sysctl.conf file.

1. Open the file with a text editor:
```bash
sudo nano /etc/sysctl.conf
```
2. Add the following lines at the end of the file:
```bash
net.core.rmem_default = 10000000
net.core.wmem_default = 10000000
net.core.rmem_max = 16777216
net.core.wmem_max = 16777216
```
3. Save the file and exit the text editor.
4. Apply the changes by running:
```bash
sudo sysctl -p
```
This will reload the `sysctl.conf` file and apply the new settings.
## Step 3: Verify the Changes
After applying the changes, verify that the new values are applied correctly by running the following commands:
```bash
sysctl net.core.rmem_default
sysctl net.core.wmem_default
sysctl net.core.rmem_max
sysctl net.core.wmem_max
```
Sample Output:
```bash
net.core.rmem_default = 10000000
net.core.wmem_default = 10000000
net.core.rmem_max = 16777216
net.core.wmem_max = 16777216
```
Show all config:
```bash
sysctl -a
sysctl -a | grep net.core
grep "net.core" /etc/sysctl.conf
```
# Additional Optimizations
If you are dealing with high network traffic or large-scale deployments, consider the following optimizations:
1. 1. Increase Socket Buffer Size Dynamically
To ensure that sockets have enough buffer space during periods of high traffic, you can adjust the buffer size dynamically with sysctl. The following command can increase the maximum allowed socket buffer size:
```bash
sudo sysctl -w net.core.optmem_max=25165824
```
This will increase the maximum socket buffer to 24MB.
2. Optimize TCP Congestion Control
If you're running a high-performance network application, you might want to adjust the TCP congestion control algorithm. For instance, the bbr algorithm is useful for optimizing network throughput:
```bash
sudo sysctl -w net.ipv4.tcp_congestion_control=bbr
```
To make this change permanent, add the following line to `/etc/sysctl.conf`:
```bash
net.ipv4.tcp_congestion_control = bbr
```
```md
# bbr
## Step 1: Check TCP Congestion Control Algorithms on Linux
sysctl net.ipv4.tcp_available_congestion_control
Output: net.ipv4.tcp_available_congestion_control = cubic reno
* To check the current congestion control algorithm in use, run *
sysctl net.ipv4.tcp_congestion_control
Output: net.ipv4.tcp_congestion_control = cubic
## Step 2: Make Sure You Have Linux Kernel 4.9 or Above
uname -r
sudo nano /etc/sysctl.conf
* Add the following two lines at the end of the file. *
"
net.core.default_qdisc=fq
net.ipv4.tcp_congestion_control=bbr
"
sudo sysctl -p
* Now check the congestion control algorithm in use. *
sysctl net.ipv4.tcp_congestion_control
Output: net.ipv4.tcp_congestion_control = bbr
```
3. Increase Number of Open Files
If your system needs to handle many simultaneous connections, you may need to increase the number of open files allowed for processes:
```bash
sudo sysctl -w fs.file-max=1000000
```
To make this change permanent, add the following line to `/etc/sysctl.conf`:
```bash
fs.file-max = 1000000
```
4. Enable TCP Fast Open
For improving the connection establishment time, you can enable TCP Fast Open:
```bash
sudo sysctl -w net.ipv4.tcp_fastopen=1
```
```bash
net.ipv4.tcp_fastopen = 1
# for enable fastopen with (Pre-Shared Cookie server side) -> net.ipv4.tcp_fastopen = 2
# for enable fastopen with (Pre-Shared Cookie client & server side) -> net.ipv4.tcp_fastopen = 3
```
5. Monitor Performance
To keep track of the changes and network performance, you can use tools like `netstat`, `ss`, and `iftop`. These tools help monitor the network throughput and detect any potential bottlenecks.

To view the socket buffer size for each network connection:
```bash
netstat -an
```
To monitor real-time network traffic:
```bash
iftop
```
### **Further Optimizations for Low Latency and High Bandwidth Networks**

For systems that need to be optimized for low latency or high bandwidth, certain `sysctl` parameters can be adjusted to improve performance. Below are the recommended settings depending on the use case.

#### **Low Latency Networks:**
When aiming to reduce latency, you will prioritize minimizing the delay in data transmission. The following settings can help achieve low latency:

- `net.ipv4.tcp_window_scaling = 1`
  - Enables TCP window scaling, which allows the TCP window size to grow beyond 64KB, improving throughput on high bandwidth networks.
  
- `net.ipv4.tcp_reordering = 3`
  - Controls the number of times an IPv4 packet can be reordered in a TCP stream without TCP assuming packet loss. Higher values allow more reordering but could increase latency.

- `net.ipv4.tcp_low_latency = 1`
  - Prefers low latency over higher throughput, which helps with applications sensitive to delay.

- `net.ipv4.tcp_sack = 1`
  - Enables Selective Acknowledgement (SACK) for IPv4. This improves reliability and performance, especially in lossy networks, by allowing selective acknowledgment of received packets.

- `net.ipv4.tcp_timestamps = 1`
  - Enables TCP timestamps, which are useful for calculating round-trip time, but adds overhead. Use when needed in environments with high packet loss or latency.

- `net.ipv4.tcp_fastopen = 1`
  - Allows data to be sent in the opening SYN packet, reducing handshake time and improving connection establishment latency.

#### **High Bandwidth and Heavy Traffic Networks:**
For networks with high bandwidth and large volumes of traffic, the following settings are recommended to optimize performance:

- `net.ipv4.tcp_window_scaling = 1`
  - This is essential for utilizing large TCP window sizes, especially on high-speed networks.

- `net.ipv4.tcp_reordering = 3` (default or higher)
  - Reordering can be tolerated more on high bandwidth networks, preventing unnecessary retransmissions due to slight reordering.

- `net.ipv4.tcp_sack = 1`
  - Enables SACK for better retransmission management, useful for networks with high packet loss or congestion.

- `net.ipv4.tcp_fastopen = 1`
  - Speeds up the initial connection setup by sending data in the SYN packet, which is important for reducing connection setup times.

### **Additional Recommendations**
- **Real-Time Applications**: Consider setting your kernel to real-time mode if your application is sensitive to latency.
- **Traffic Shaping**: For environments with very high traffic, implementing proper traffic shaping can help manage load and avoid congestion.

# Troubleshooting
If you encounter any issues after applying the changes, check the following:

Ensure the values are being loaded correctly after a reboot by verifying the `/etc/sysctl.conf` file.
Use `dmesg` to check for any kernel errors or warnings related to network configuration.

# Conclusion
By following these steps, you can optimize the network buffer settings on your Linux system to improve performance for applications that rely heavily on network traffic. Always ensure that the changes are appropriate for your specific use case and monitor the system for performance improvements.
