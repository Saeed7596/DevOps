# Linux Monitoring Tools: htop, Glances, Ctop, and Bpytop

This document provides an overview of four powerful Linux monitoring tools: **htop**, **Glances**, **Ctop**, and **Bpytop**, with their features, installation instructions, and usage details.

---

## **1. htop**

### **Overview**
`htop` is an interactive process viewer for Linux, providing a user-friendly, color-coded interface for monitoring system resources and processes.

### **Features**
- Real-time monitoring of CPU, memory, and process usage.
- Tree view of processes.
- Easy-to-use interface with keyboard navigation.
- Ability to search, filter, and sort processes.
- Supports terminating or renicing processes interactively.

### **Installation**
#### On Ubuntu/Debian:
```bash
sudo apt update
sudo apt install htop
htop
```

---

## **2. Glances**
### **Overview**
`Glances` is a cross-platform, multi-purpose monitoring tool designed to provide a broad view of system metrics.

### **Features**
- Displays CPU, memory, disk, network, and process metrics.
- Supports remote monitoring via web UI or API.
- Integration with tools like InfluxDB, Grafana, and Elasticsearch.
- Lightweight and highly configurable.
### **Installation** [Document](https://github.com/nicolargo/glances)
#### On Ubuntu/Debian:
```bash
sudo apt update
sudo apt install glances
```
#### Using pip:
```bash
sudo apt install python3-pip
pip3 install glances
```
#### Usage
```bash
glances
```
```bash
glances -w
```
- Access via a web browser at `http://<SERVER_IP>:61208`.

---

## **3. Ctop**
### **Overview**
`Ctop` is a command-line tool designed for monitoring Docker containers in real-time.

### **Features**
- Displays container-level metrics such as CPU and memory usage.
- Supports starting, stopping, and removing containers.
- Interactive and lightweight.
### **Installation**
1. Using Binary (Recommended):
Download the latest binary:
```bash
curl -Lo ctop https://github.com/bcicen/ctop/releases/latest/download/ctop-`uname -s`-`uname -m`
```
2. Make it executable:
```bash
chmod +x ctop
```
3. Move to a system path:
```bash
sudo mv ctop /usr/local/bin/
```
#### Usage
```bash
ctop
```
#### Key Shortcuts
- `q`: Quit
- `f`: Filter containers
- `Enter`: View detailed container stats

---

## **4. Bpytop**
### **Overview**
`Bpytop` is a Python-based resource monitoring tool with a visually appealing and interactive interface.
### **Features**
- Monitors CPU, memory, disk, and network usage.
- Provides real-time graphs and detailed metrics.
- Supports filtering and sorting processes.
- Fast and lightweight.
### **Installation**
#### Using pip:
```bash
sudo apt install python3-pip
pip3 install bpytop
```
#### Usage
```bash
bpytop
```

---

## **5. bmon**
### **Overview**
`bmon` (Bandwidth Monitor) is a real-time, terminal-based network bandwidth monitoring tool for Linux systems. It's simple, fast, and very helpful when you want to visualize incoming/outgoing traffic on your network interfaces.
### **Features**
- Real-time bandwidth monitoring
- Graphical interface (in terminal)
- Shows transmit/receive rates per interface
- Lightweight and easy to use
### **Installation**
#### On RHEL / CentOS / Fedora:
```bash
sudo dnf install bmon -y
```
#### On Debian / Ubuntu:
```bash
sudo apt install bmon -y
```
#### Usage
```bash
bmon
```
#### Key Shortcuts
- `q`    | Quit the program
- `d`    | Switch to details view
- `g`    | Switch to graphical view
- `t`    | Switch to text-only view
- `i`    | Show interface statistics
- `h`    | Help screen

---

| Tool       | Primary Use               | Key Features                                   | Ideal For             |
|------------|---------------------------|-----------------------------------------------|------------------------|
| **htop**   | Process monitoring        | Tree view, search, interactive process control| General system usage   |
| **Glances**| Comprehensive monitoring  | Remote access, API integration, modular design| Broad system overview  |
| **Ctop**   | Docker container monitoring| Real-time container stats, lightweight       | Docker environments    |
| **Bpytop** | Resource monitoring       | Graphical interface, detailed metrics         | Users who prefer visuals|
| **bmon**   | Network bandwidth monitor | Real-time graphs, per-interface stats, lightweight| Monitoring network traffic|


## **Conclusion**
- Use htop for process management and system overview.
- Choose Glances for comprehensive system monitoring with remote capabilities.
- Opt for Ctop to manage and monitor Docker containers efficiently.
- Try Bpytop if you want an intuitive and visually rich monitoring experience.

---

# `watch` Command Cheat Sheet

The `watch` command in Linux allows you to execute a command repeatedly at regular intervals and observe its output.

| **Option/Flag** | **Description**                                                                 | **Example**                              |
|------------------|---------------------------------------------------------------------------------|------------------------------------------|
| `-n seconds`    | Set the interval between command executions (default is 2 seconds).            | `watch -n 5 date`                        |
| `-d`            | Highlight differences between consecutive outputs.                             | `watch -d ls`                            |
| `-t`            | Turn off the header displaying interval and command.                          | `watch -t uptime`                        |
| `-e`            | Exit if the command returns a non-zero exit code.                             | `watch -e curl http://example.com`       |
| `-g`            | Exit when the output of the command changes.                                  | `watch -g ls`                            |
| `-x`            | Pass the command to the shell for execution (useful for complex commands).    | `watch -x 'df -h | grep sda1'`           |
| `--no-title`    | Same as `-t`, suppress the header display.                                     | `watch --no-title df -h`                 |

### **Basic Usage Example**
```bash
# Monitor disk usage every 2 seconds:
watch df -h

# Check for new files in the directory and highlight differences:
watch -d ls

# Run a command every 5 seconds without a header:
watch -n 5 -t free -m

