# Update Red Hat Machine in Air-Gap enviroment.
## Method 1 
### Step 1: Download Updates & Dependencies (On the Connected Staging Machine)
```bash
mkdir -p /tmp/rhel9-updates
sudo dnf update --downloadonly --destdir=/tmp/rhel9-updates
```
Or, On one of the machines in the Air-gap environment, run the following command to get a list of installed packages:
```bash
rpm -qa --qf "%{NAME}\n" > /tmp/installed-packages.txt
sudo dnf download --resolve --destdir=/tmp/rhel9-updates $(cat installed-packages.txt)
```
* Note: This command resolves all dependencies and grabs the latest available versions (including the new Linux Kernel).

---

### Step 2: Transfer the Packages
Compress the downloaded RPM files, transfer the archive into your air-gapped network, and extract it on your target servers.
```bash
tar -czvf rhel9-updates.tar.gz /tmp/rhel9-updates
```

---

### Step 3: Install Updates (In the Air-Gapped Environment)
Navigate to the directory containing the transferred `.rpm` files and run the local installation command:
```bash
cd /path/to/extracted/rhel9-updates
sudo dnf localinstall *.rpm -y
```
ignore repository 
```bash
sudo dnf install --disablerepo="*" ./*.rpm --allowerasing -y
```

---

## Method 2: Creating a Local Repository (Best for Multi-Server Deployments)
If you have many servers to update or want to create a permanent internal update mirror, building a Local Repository is the best long-term solution.

### Step 1: Sync Repositories (On the Connected Staging Machine)
Install the required repository management tools and synchronize the primary RHEL 9 channels:

```bash
# Install utilities
sudo dnf install yum-utils createrepo -y

# Create storage layout
mkdir -p /tmp/local-repo/BaseOS
mkdir -p /tmp/local-repo/AppStream

# Synchronize official Red Hat repositories
reposync --repo=rhel-9-for-x86_64-baseos-rpms -p /tmp/local-repo/BaseOS --download-metadata
reposync --repo=rhel-9-for-x86_64-appstream-rpms -p /tmp/local-repo/AppStream --download-metadata
```

---

### Step 2: Transfer and Host the Repository
Move the `/tmp/local-repo` directory into the air-gapped network. You can host this directory on an internal `web server (Apache/Nginx)`   
or distribute it locally to each server's local storage (e.g., `/var/local-repo/`).

---

### Step 3: Configure Target Client Repositories
On the air-gapped servers, disable external repos and create a new local repo definition file:
```bash
sudo nano /etc/yum.repos.d/local-rhel9.repo
```
Add the following configuration (adjust the paths if using http:// instead of file:// storage):
```TOML
[local-baseos]
name=Red Hat Enterprise Linux 9 BaseOS - Local
baseurl=file:///var/local-repo/BaseOS/
enabled=1
gpgcheck=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-redhat-release

[local-appstream]
name=Red Hat Enterprise Linux 9 AppStream - Local
baseurl=file:///var/local-repo/AppStream/
enabled=1
gpgcheck=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-redhat-release
```

---

### Step 4: Run the System Update
Clear the cache and execute the global system update:
```bash
sudo dnf clean all
sudo dnf update -y
```

### Important Post-Update Checklist
1. Activating the New Kernel
Kernel updates are downloaded and installed alongside old versions,
but they cannot be hot-applied. To boot into the newly installed kernel,
you must `reboot` the system:

```Bash
sudo reboot
```
Verify the active kernel version after the reboot completes:
```bash
uname -r
```
2. Fallback Mechanism (GRUB)
RHEL preserves the last 3 working kernels by default. If your environment uses highly specialized software or proprietary device drivers
that conflict with the new kernel,  
you can safely select the previous working kernel configuration from the GRUB boot menu during the system startup sequence.
