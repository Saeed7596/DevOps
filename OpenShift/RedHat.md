# Some RedHat Challenges
### show the ip address:
```bash
ip -br -c -4 a # -br: breake , -c: color , -4: show ipv4 , a: addr
hostname -I
nmcli device status
nmcli device show
```
### enable redhat subscription
```bash
sudo subscription-manager repos --enable=rhel-9-for-x86_64-baseos-rpms
sudo subscription-manager repos --enable=rhel-9-for-x86_64-appstream-rpms
```
### show all repo
```bash
sudo subscription-manager repos --list
```
```bash
cat /etc/*release
ls /etc/yum.repos.d/
sudo subscription-manager status
```
### Add DNS Manually
```
echo "nameserver 178.22.122.100" | sudo tee /etc/resolv.conf
echo "nameserver 185.51.200.2" | sudo tee /etc/resolv.conf
```
### If have problem to get package or get 403 error
```bash
sudo systemctl restart NetworkManager
```
### Clean `dnf` cache and refresh completely
```bash
sudo dnf clean all
sudo rm -rf /var/cache/dnf
sudo dnf makecache
```
### Change repo
```bash
nano fix-repo.sh
```
```sh
#!/bin/bash

echo "[INFO] Switching Repositories to AlmaLinux Mirrors..."

sudo rm -f /etc/yum.repos.d/*.repo

cat <<EOF | sudo tee /etc/yum.repos.d/almalinux.repo
[baseos]
name=AlmaLinux BaseOS
baseurl=https://repo.almalinux.org/almalinux/9/BaseOS/x86_64/os/
enabled=1
gpgcheck=0

[appstream]
name=AlmaLinux AppStream
baseurl=https://repo.almalinux.org/almalinux/9/AppStream/x86_64/os/
enabled=1
gpgcheck=0

[extras]
name=AlmaLinux Extras
baseurl=https://repo.almalinux.org/almalinux/9/extras/x86_64/os/
enabled=1
gpgcheck=0
EOF

echo "[INFO] Cleaning cache..."
sudo dnf clean all

echo "[INFO] Making cache..."
sudo dnf makecache

echo "[INFO] Updating system..."
sudo dnf update -y

echo "------ Done ------"
```
```bash
chmod +x fix-repo.sh
./fix-repo.sh
```

---

# Install Oblivion
Download the rpm file [Oblivion](https://github.com/bepass-org/oblivion-desktop)
```bash
sudo rpm -i oblivion-desktop-linux-x86_64.rpm
```
# `libXScrnSaver` package:
You can download the `AlmaLinux` or `CentOS` rmp file.
```bash
https://rpmfind.net/linux/rpm2html/search.php?query=libXScrnSaver
```
```bash
wget https://mirror.chpc.utah.edu/pub/almalinux/9/AppStream/x86_64/os/Packages/libXScrnSaver-1.2.3-10.el9.x86_64.rpm
or
wget https://rpmfind.net/linux/almalinux/9.5/AppStream/x86_64/os/Packages/libXScrnSaver-1.2.3-10.el9.x86_64.rpm
```
```bash
sudo rpm -i libXScrnSaver-1.2.3-10.el9.x86_64.rpm
```
# Route terminal internet traffic throw vpn
```bash
Setting -> Network -> Proxy: Manual -> HTTP/HTTPS = 127.0.0.1:8086
```
## Show external ip for check the vpn connection in terminal
```bash
curl ifconfig.me
```
Output should be the vpn ip
