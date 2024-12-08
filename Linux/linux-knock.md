# Knock Package in Ubuntu

The `knock` package is a tool used to perform port knocking. Port knocking is a method of opening ports on a firewall by generating a specific connection sequence to pre-defined closed ports.

## First
[Change SSH Port](https://github.com/Saeed7596/DevOps/blob/main/Linux/ssh.md)

## Installing Knock
To install the `knock` package on Ubuntu, use the following commands:

```bash
sudo apt update
sudo apt install knockd
```
## Configuration
1. Edit the Configuration File
The main configuration file for `knockd` is located at `/etc/knockd.conf`. Edit it to define the sequences for opening and closing ports. For example:
```ini
[openSSH]
sequence = 7000,8000,9000
seq_timeout = 10
command = /sbin/iptables -A INPUT -s %IP% -p tcp --dport 2222 -j ACCEPT
tcpflags = syn

[closeSSH]
sequence = 9000,8000,7000
seq_timeout = 10
command = /sbin/iptables -D INPUT -s %IP% -p tcp --dport 2222 -j ACCEPT
tcpflags = syn
```
2. `nano /etc/default/knockd`
This file controls the runtime behavior of knockd, including whether it runs in daemon mode and on which network interfaces.

Key options:

- `START_KNOCKD`: Set to 1 to enable the service on startup.
- `KNOCKD_OPTS`: Specify additional options such as the interface -i eth0.
With `ip a` find the eth
Example:
```bash
# Enable knockd
START_KNOCKD=1

# Listen on a specific interface
KNOCKD_OPTS="-i eth18"
```
3. Restart the Knock Service
After making changes, restart the service to apply the configuration:
```bash
sudo systemctl restart knockd
sudo systemctl status knockd
sudo systemctl enable knockd
```

---

## Using Knock

To send a knock sequence from a client, use the `knock` command:
```bash
sudo apt install knockd
knock -v <target-ip> 7000 8000 9000
knock -v <target-ip> 9000 8000 7000
```
Explanation of Flags and Parameters:
- `knock`: The tool used to send port-knocking sequences.
- `-v`: Enables verbose output, which provides detailed feedback about the knock process.
- `<target-ip>`: The IP address of the target machine where the knock sequence is sent.
- `7000 8000 9000`: The sequence of ports to "knock" on in order. These must match the sequence configured on the target system.
