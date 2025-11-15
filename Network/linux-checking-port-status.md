
# Checking Port Status in Linux

In Linux, there are several methods to check if a port is open or closed. Below are a few commonly used tools and commands to help you check the status of a port:

## 1. Using `nc` (Netcat)
Netcat (`nc`) is one of the most commonly used tools to check port status.

### Check if a port is open:
```bash
nc -zv <IP_Address> <Port>
```
- `-z`: Only checks if the port is open without sending any data.
- `-v`: Verbose mode to show more details.

**Example:**
```bash
nc -zv 192.168.1.100 27017
```
If the port is open, you will get output like:
```
Connection to 192.168.1.100 27017 port [tcp/*] succeeded!
```
If the port is closed, you will get output like:
```
nc: connect to 192.168.1.100 port 27017 (tcp) failed: Connection refused
```

## 2. Using `telnet`
`telnet` is another tool that can be used to check the status of a port.

### Check if a port is open:
```bash
telnet <IP_Address> <Port>
```
**Example:**
```bash
telnet 192.168.1.100 27017
```
If the port is open, you will see a message like "Connected". If it is closed, you will see a message like "Connection refused" or "Unable to connect".

## 3. Using `ss` or `netstat` to check open ports locally
To check the open ports on your local system, you can use either the `ss` or `netstat` command.

### Using `ss`:
```bash
ss -tuln
ss -s
```
This command lists all open TCP and UDP ports.

### Using `netstat`:
```bash
netstat -na #Show all ports
netstat -tuln
netstat -na | grep LISTEN
netstat -ant | grep ESTABLISHED | wc -l
```
This will show the open TCP and UDP ports along with the services using them.

## 4. Using `nmap` for port scanning
If you want to scan the ports on a remote host, you can use the `nmap` tool.

### Scan a specific port:
```bash
nmap -p <Port> <IP_Address>
```
**Example:**
```bash
nmap -p 27017 192.168.1.100
```

### Scan all ports:
```bash
nmap <IP_Address>
```

These methods will help you check the status of ports and determine if they are open or closed.

## 5. Other 
```bash
sudo netstat -tuln | grep <PORT_NUMBER>
sudo ss -tuln | grep <PORT_NUMBER>
sudo lsof -i:<PORT_NUMBER>
```
