# Samba File Sharing Setup on Linux (Ubuntu Example)
This guide explains how to install and configure Samba on a Linux machine to share files across the network. It also includes steps for accessing the share from Linux and Windows clients.

---

## 🛠️ Requirements

- A Linux machine (e.g., Ubuntu Server)
- Root or sudo access
- Network connectivity with clients

---

## 📦 Step 1: Install Samba
```bash
sudo apt update
sudo apt install samba -y
```

---

## 📁 Step 2: Create a Shared Directory
```bash
sudo mkdir -p /srv/share
sudo chmod -R 777 /srv/share
```

> You can restrict permissions later based on your security needs.

---

## ⚙️ Step 3: Configure Samba
Edit the Samba configuration file:
```bash
sudo nano /etc/samba/smb.conf
```

Add the following section at the end of the file:
```ini
[SharedFiles]
   path = /srv/share
   browseable = yes
   writable = yes
   guest ok = yes
   create mask = 0777
   directory mask = 0777
```

> For user-based access, replace `guest ok = yes` with user authentication settings.

---

## 🔄 Step 4: Restart Samba Service
```bash
sudo systemctl restart smbd
```

---

## 🔓 Step 5: (Optional) Allow Samba Through Firewall
```bash
sudo ufw allow 'Samba'
```

---

## 💻 Accessing the Share
### From a Linux Client
#### Option 1: Using `smbclient` (like FTP)
```bash
# Ubuntu
sudo apt install samba-client -y
# RedHat
sudo dnf install samba-client -y
```
```bash
smbclient //<Samba-IP>/SharedFiles -N
```
* The `-N` option means without entering a username and password (when `guest ok = yes` is set on the Samba server).

Once inside, use:
```bash
`ls`           # List files
`put filename` # Upload file
`get filename` # Download file
```
# 📦 Monitoring File Transfer Progress with Samba
This guide helps you monitor the progress of a file being transferred (uploaded or downloaded) via Samba.
## 🔼 When Uploading a File (to the Samba Server)
1. SSH into the Samba server:
   ```bash
   ssh user@<Samba-IP>
   ```
2. Navigate to the shared directory (e.g., /srv/share):
```bash
cd /srv/share
```
3. Use watch to monitor file size growth in real-time:
```bash
watch -- du -h <filename>
```
## 🔽 When Downloading a File (from the Samba Server)
On the same host where the file is being downloaded (open a new terminal), go to the download destination directory.

---

#### Option 2: Mounting the Share
```bash
sudo apt install cifs-utils
sudo mkdir /mnt/share
sudo mount -t cifs //<Samba-IP>/SharedFiles /mnt/share -o guest
```

### From a Windows Client
In File Explorer, type:
```
\\<Samba-IP>\SharedFiles
```
Then use it as a normal folder (drag and drop files).

---

## 🔐 Optional: Add User Authentication
If you want to secure the share:
```bash
sudo adduser myuser
sudo smbpasswd -a myuser
```

Edit the config:
```ini
guest ok = no
valid users = myuser
```

Then restart Samba again:
```bash
sudo systemctl restart smbd
```

---

## ✅ Done!
Your Samba server is now ready to share files across the network!
