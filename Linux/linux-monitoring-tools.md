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

| Tool       | Primary Use               | Key Features                                   | Ideal For              |
|------------|---------------------------|-----------------------------------------------|------------------------|
| **htop**   | Process monitoring        | Tree view, search, interactive process control| General system usage   |
| **Glances**| Comprehensive monitoring  | Remote access, API integration, modular design| Broad system overview  |
| **Ctop**   | Docker container monitoring| Real-time container stats, lightweight        | Docker environments    |
| **Bpytop** | Resource monitoring       | Graphical interface, detailed metrics         | Users who prefer visuals|




