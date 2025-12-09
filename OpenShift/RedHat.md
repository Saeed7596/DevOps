# Some RedHat Challenges
## Sites
[Developers](https://developers.redhat.com/)
* While building, make sure you select Developer Subscription.

[Products Download](https://developers.redhat.com/products/rhel/download)

[Console](https://console.redhat.com/)

[Subscriptions](https://console.redhat.com/subscriptions/overview)

### show the ip address:
```bash
ip -br -c -4 a # -br: breake , -c: color , -4: show ipv4 , a: addr
hostname -I
nmcli device status
nmcli device show
```
### enable redhat subscription
```bash
sudo subscription-manager register
sudo subscription-manager register --username <username> --password <password>
```
```bash
sudo subscription-manager refresh
```
```bash
sudo subscription-manager repos --enable=rhel-9-for-x86_64-baseos-rpms
sudo subscription-manager repos --enable=rhel-9-for-x86_64-appstream-rpms
```
### show all repo
```bash
sudo subscription-manager repos --list
sudo subscription-manager repos --list-enabled
```
```bash
sudo subscription-manager list --available --all
```
### Update
```bash
sudo dnf clean all
sudo dnf repolist
sudo dnf update
```
# Refresh
```bash
sudo subscription-manager status
sudo subscription-manager refresh
sudo subscription-manager register --username <USER> --password <PASS>
```
# Un-registering a system
```bash
sudo subscription-manager remove --all
sudo subscription-manager unregister
sudo subscription-manager clean
```
```bash
cat /etc/*release
ls /etc/yum.repos.d/
sudo subscription-manager status
```

---

# Install Package
## Use dnf
```bash
sudo dnf update
sudo dnf install -y package_name
```
## Use rpm
```bash
sudo rpm -ivh package_name.rpm
sudo rpm -Uvh package_name.rpm        # Upgrade an RPM
```

# Uninstall Package
## Use dnf
```bash
sudo dnf list installed
sudo dnf list installed | grep <package_name>
sudo dnf remove <package_name>
sudo dnf autoremove
```
Example:
```bash
sudo yum list installed | grep httpd   # Find the httpd package
sudo yum remove httpd                  # Remove the httpd package
sudo yum autoremove                    # Remove unused dependencies
```
## Or Using rpm
```bash
rpm -qa
sudo rpm -e <package_name>             # Replace <package_name> with the full name of the package.
```
Example:
```bash
rpm -qa | grep httpd                   # Find the httpd package
sudo rpm -e httpd-2.4.6-97.el7.x86_64  # Remove the httpd package
```

---

### Add DNS Manually
```
echo "nameserver 178.22.122.100" | sudo tee /etc/resolv.conf
echo "nameserver 185.51.200.2" | sudo tee /etc/resolv.conf
```
### Or
#### Set Custom DNS on Fedora / RHEL / CentOS (with NetworkManager):
Find Connection NAME:
```bash
nmcli con show
```
Set custom DNS:
```bash
nmcli con mod "<connection-name>" ipv4.dns "178.22.122.100 185.51.200.2"
```
Ignore automatic DNS:
```bash
nmcli con mod "<connection-name>" ipv4.ignore-auto-dns yes
```
Restart connection:
```bash
nmcli con down "<connection-name>" && nmcli con up "<connection-name>"
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

---

# Chrony in Red Hat 9.x
```bash
sudo nano /etc/chrony.conf 
```
```nano
server <ntp-ip-address> iburst
```
```bash
sudo firewall-cmd --permanent --add-port=123/udp

sudo firewall-cmd --reload
```
```bash
sudo systemctl status chronyd
sudo systemctl restart chronyd
```
# Verify
```bash
chronyc sources -v 
chronyc tracking 
```
You should see the internal NTP server as `NTP source` and the status will show `^*` or `^+` indicating that it is synchronized.

And `Leap status` should be `Normal`.

---

### Change repo
> **Find the `dependency` in this [Site](https://rpmfind.net/linux/rpm2html/search.php)**
#### User epel
```bash
sudo dnf install epel-release
sudo dnf update
```
#### Or Use Rocky repo
```bash
nano smart-update.sh
```
```sh
#!/usr/bin/env bash
# smart-update.sh - Attempts RHEL registration first, falls back to Rocky Linux 9 mirrors if subscription fails.

set -euo pipefail
IFS=$'\n\t'

# -----------------------------
# Configuration
# -----------------------------
RHEL_USER="${1:-}"
RHEL_PASS="${2:-}"
LOG_FILE="./smart_update_$(date +%Y%m%d%H%M%S).log"

exec 3>&1 1>>${LOG_FILE} 2>&1
echo "--- Starting Smart Update Script ---"
echo "Log file: ${LOG_FILE}"

# -----------------------------
# Prerequisites Check
# -----------------------------
if [ -z "$RHEL_USER" ] || [ -z "$RHEL_PASS" ]; then
    echo "FATAL: Usage: $0 <RHEL_USERNAME> <RHEL_PASSWORD>" >&3
    exit 1
fi

command -v subscription-manager >/dev/null 2>&1 || { echo "FATAL: 'subscription-manager' not found." >&3; exit 1; }
command -v dnf >/dev/null 2>&1 || { echo "FATAL: 'dnf' not found." >&3; exit 1; }

# -----------------------------
# Functions
# -----------------------------

# Function to attempt RHEL registration and subscription
attempt_rhel_register() {
    echo "INFO: Attempting to register system with Red Hat..." >&3

    # 1. Unregister any existing subscriptions (clean slate)
    if sudo subscription-manager status | grep -q 'Current status: Subscribed'; then
        echo "INFO: Unregistering previous subscription."
        sudo subscription-manager unregister
    fi

    # 2. Register and Auto-Attach
    if sudo subscription-manager register --username "$RHEL_USER" --password "$RHEL_PASS" --auto-attach; then
        echo "SUCCESS: System successfully registered and subscribed to RHEL." >&3
        return 0
    else
        echo "WARNING: RHEL registration failed. Subscription credentials or status invalid." >&3
        return 1
    fi
}

# Function to switch to Rocky Linux repositories
switch_to_rocky_linux() {
    echo "INFO: Switching repositories to Rocky Linux 9 mirrors (Fallback Mode)..." >&3
    
    # Clean up RHEL repositories files created by subscription-manager
    # Note: We don't remove all *.repo, just the ones created by RHEL.
    sudo rm -f /etc/yum.repos.d/redhat.repo /etc/yum.repos.d/rhel-*.repo /etc/yum.repos.d/rhui-*.repo

    # Add Rocky Linux 9 repositories
    cat <<EOF | sudo tee /etc/yum.repos.d/rockylinux-fallback.repo
[baseos]
name=Rocky Linux 9 - BaseOS
baseurl=https://download.rockylinux.org/pub/rocky/9/BaseOS/x86_64/os/
enabled=1
gpgcheck=0

[appstream]
name=Rocky Linux 9 - AppStream
baseurl=https://download.rockylinux.org/pub/rocky/9/AppStream/x86_64/os/
enabled=1
gpgcheck=0

[extras]
name=Rocky Linux 9 - Extras
baseurl=https://download.rockylinux.org/pub/rocky/9/extras/x86_64/os/
enabled=1
gpgcheck=0
EOF
    echo "INFO: Rocky Linux repositories added."
}

# Function to perform the final update
perform_update() {
    echo "INFO: Cleaning DNF cache and updating system..." >&3
    sudo dnf clean all
    sudo dnf makecache

    if sudo dnf update -y; then
        echo "SUCCESS: System update completed." >&3
        return 0
    else
        echo "FATAL: DNF update failed. Check the log file for details." >&3
        return 1
    fi
}

# -----------------------------
# Main Logic
# -----------------------------

# Phase 1: Try RHEL Subscription
if attempt_rhel_register; then
    # SUCCESS PATH: RHEL is registered, repositories are configured by subscription-manager
    # Ensure any previous fallback repos are removed just in case
    sudo rm -f /etc/yum.repos.d/rockylinux-fallback.repo || true
    
    echo "INFO: Proceeding with RHEL official repositories." >&3
    perform_update
    
    # Keep the system registered after update
    echo "INFO: RHEL path finished. System remains subscribed." >&3
    
else
    # FAILURE PATH: RHEL subscription failed
    switch_to_rocky_linux
    
    # We must unregister the failed attempt to ensure subscription-manager does not interfere
    # This step is crucial if the registration attempt created temporary files or configurations.
    sudo subscription-manager unregister 2>/dev/null || true
    
    echo "INFO: Proceeding with Rocky Linux fallback repositories." >&3
    perform_update
    
    # Clean up: Remove the temporary Rocky Linux repo file and unregister the system
    echo "INFO: Fallback path finished. Please resolve RHEL subscription issue." >&3
    # Optional: Remove Rocky Linux repo file after update
    # sudo rm -f /etc/yum.repos.d/rockylinux-fallback.repo

fi

echo "--- Script Finished ---" >&3
```
```bash
chmod +x smart-update.sh
./smart-update.sh "YourRHELUsername" "YourRHELPassword"
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
```
or
```bash
wget https://rpmfind.net/linux/almalinux/9.5/AppStream/x86_64/os/Packages/libXScrnSaver-1.2.3-10.el9.x86_64.rpm
```
```bash
sudo rpm -i libXScrnSaver-1.2.3-10.el9.x86_64.rpm
```

# Route terminal internet traffic throw vpn (Oblivion)
```bash
Setting -> Network -> Proxy: Manual -> HTTP/HTTPS = 127.0.0.1:8086
```
### With command:
```bash
export http_proxy=http://your.proxy:port
export https_proxy=http://your.proxy:port
```
```bash
echo $http_proxy
echo $https_proxy
```
## Show external ip for check the vpn connection in terminal
```bash
curl ifconfig.me
```
Output should be the vpn ip
## Check cdn.redhat.com
```bash
curl -v https://cdn.redhat.com
host cdn.redhat.com
nc -vz cdn.redhat.com 443
```

---

# Install [Hiddiyfy](https://github.com/hiddify/hiddify-app)
Find the dependency in this [Site](https://rpmfind.net/linux/rpm2html/search.php)
```bash
wget https://rpmfind.net/linux/epel/9/Everything/x86_64/Packages/l/libayatana-appindicator-gtk3-0.5.93-4.el9.x86_64.rpm && wget https://rpmfind.net/linux/epel/9/Everything/x86_64/Packages/l/libayatana-ido-gtk3-0.10.1-4.el9.x86_64.rpm && wget https://rpmfind.net/linux/epel/9/Everything/x86_64/Packages/l/libayatana-indicator-gtk3-0.9.4-3.el9.x86_64.rpm && wget https://rpmfind.net/linux/epel/9/Everything/x86_64/Packages/l/libdbusmenu-16.04.0-19.el9.x86_64.rpm && wget https://rpmfind.net/linux/epel/9/Everything/x86_64/Packages/l/libdbusmenu-gtk3-16.04.0-19.el9.x86_64.rpm
```
```bash
sudo rpm -i libayatana-ido-gtk3-0.10.1-4.el9.x86_64.rpm && sudo rpm -i libayatana-indicator-gtk3-0.9.4-3.el9.x86_64.rpm && sudo rpm -i libdbusmenu-16.04.0-19.el9.x86_64.rpm && sudo rpm -i libdbusmenu-gtk3-16.04.0-19.el9.x86_64.rpm && sudo rpm -i libayatana-appindicator-gtk3-0.5.93-4.el9.x86_64.rpm
```
```bash
wget https://github.com/hiddify/hiddify-next/releases/latest/download/Hiddify-rpm-x64.rpm
```
```bash
sudo rpm -ivh Hiddify-rpm-x64.rpm
```
# Or Install [HiddiyfyCli](https://hiddify.com/fa/app/HiddifyCli-guide/#hiddifycli-hiddifyapp_1)
[Download](https://github.com/hiddify/hiddify-core/releases) the file and extrat
```bash
wget https://github.com/hiddify/hiddify-core/releases/download/v3.1.8/hiddify-cli-linux-amd64.tar.gz
tar -xzvf hiddify-cli-linux-amd64.tar.gz
```
Save your sublink as a `.txt` file
```bash
nano sublink.txt
```
```bash
./HiddifyCli run -c <config file or sublink>
./HiddifyCli run -c sublink.txt
```
Check the `Mixed Port`
```bash
echo $http_proxy
echo $https_proxy
# Output is empty!
export http_proxy="127.0.0.1:Mixed Port"
export https_proxy="127.0.0.1:Mixed Port"
# Mixed Port = 2334
export http_proxy="127.0.0.1:2334"
export https_proxy="127.0.0.1:2334"
```
You can save the config form Hiddiyfy app as a `.json` file, so now don't need set the port manually
```bash
./HiddifyCli run -c <config file or sublink> -d <HiddifyApp config file or URL>
./HiddifyCli run -c sublink.txt -d mu-config.json
```

# Route terminal internet traffic throw vpn (Hiddiyfy)
```bash
Setting -> Network -> Proxy: Manual -> HTTP/HTTPS = 127.0.0.1:2334
```
## Show external ip for check the vpn connection in terminal
```bash
curl ipinfo.io
```
Output should be the vpn ip

---

# Download rpm and move to air-gap
In Online Client
```bash
sudo dnf install --downloadonly --downloaddir=/tmp/pkgs \
  libvirt qemu-kvm mkisofs python3-devel jq ipmitool haproxy
```
```bash
tar czvf pkgs.tar.gz /tmp/pkgs
```

on server air-gap
```bash
sudo dnf install -y /path/to/pkgs/*.rpm
```

---

For example git
```bash
mkdir -p ~/git-offline
cd ~/git-offline
sudo dnf install -y dnf-plugins-core
sudo dnf download --resolve git
```
In air-gap Client:
```bash
cd git-offline
sudo rpm -Uvh *.rpm
```

---

# ab - Apache Benchmark
In Online Client
```bash
sudo dnf install --downloadonly --downloaddir=/tmp/httpd-tools httpd-tools
```
```bash
cd /tmp
tar -czvf httpd-tools.tar.gz httpd-tools
```
```bash
scp /tmp/httpd-tools.tar.gz /tmp/httpd-tools.tar.gz user@airgap:/tmp/
```
In air-gap Client:
```bash
cd /tmp
tar -xzvf httpd-tools.tar.gz
```
```bash
sudo dnf install /tmp/httpd-tools/*.rpm
```
```bash
which ab
ab -V
```
