```bash
nano /etc/netplan/config.yaml
```
# Type1
```json
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
```json
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
