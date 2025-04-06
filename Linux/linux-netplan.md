```bash
nano /etc/netplan/config.yaml
```
# Type1
```yml
network:
  ethernets:
    eth0:
      addresses: []
      dhcp4: true
      optional: true
      nameservers:
        addresses:
          - 78.157.42.100
          - 78.157.42.101
  version: 2
```
# Type2
```yml
network:
  ethernets:
    eth0:
      addresses: []
      nameservers:
        addresses: [178.22.122.100, 185.51.200.2]
      dhcp4: true
      optional: true
  version: 2
```

---

# Set Static IP 
```bash
hostname -I
nmcli device status
nmcli device show
```
```yaml
network:
  version: 2
  ethernets:
    ens160:
      dhcp4: no
      addresses: [192.168.252.215/24]
      gateway4: 192.168.252.1
      nameservers:
        addresses: [8.8.8.8, 8.8.4.4]
```
---

# Restart DNS servive
```bash
sudo systemctl restart systemd-resolved
```
```bash
sudo systemctl restart dnsmasq
```
```bash
sudo systemctl restart NetworkManager
```
