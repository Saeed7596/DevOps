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
### Change repo
```bash
nano fix-repo.sh
```
```sh
#!/bin/bash

echo "[INFO] Adding CentOS Stream Repositories..."

cat <<EOF | sudo tee /etc/yum.repos.d/centos-stream.repo
[centos-stream-appstream]
name=CentOS Stream AppStream
baseurl=http://mirror.centos.org/centos-stream/9-stream/AppStream/x86_64/os/
enabled=1
gpgcheck=0

[centos-stream-baseos]
name=CentOS Stream BaseOS
baseurl=http://mirror.centos.org/centos-stream/9-stream/BaseOS/x86_64/os/
enabled=1
gpgcheck=0

[centos-stream-extras]
name=CentOS Stream Extras
baseurl=http://mirror.centos.org/centos-stream/9-stream/extras/x86_64/os/
enabled=1
gpgcheck=0
EOF

echo "[INFO] Cleaning old cache..."
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
