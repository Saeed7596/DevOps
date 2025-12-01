# Some useful terminal command
```bash
lsb_release -a   ===>   #ubuntu version
dpkg --print-architecture   ===>   #show ubuntu architect  (arm or amd)
du -sh /path/to/directory   ===>   #show size of a folder & file
du -h
ls -lhS
```

---

# Check commands:
```bash
echo $?
```
* If it returns 0, it means that the previous command was executed correctly.

---

# Create user
**In Linux `$` means normal user access and `#` means super user (root) access.**
```bash
sudo useradd -m -s /bin/bash username
sudo passwd username
```
### Adding the User to the sudo Group (Ubuntu)
```bash
sudo usermod -aG sudo username
```
### Adding the User to the sudo Group (RedHat)
```bash
sudo usermod -aG wheel username
```
### Switch to User
```bash
sudo -u username -i
```
### Generate SSH Key
```bash
ssh-keygen
```
### Switch to Super User
```bash
sudo -s
```
### Adding the User to the sudo Group (Red Hat، CentOS، Fedora)
```bash
sudo usermod -aG wheel username
```

---

# Change username
```bash
# Switch to root
sudo -i

# Close all saeed sessions and processes
pkill -u olduser
killall -u olduser

who | grep olduser

pkill -KILL -u olduser
```
```bash
usermod -l newuser olduser
```

## Change home directory
The `-m` parameter will move the contents of `/home/olduser` to `/home/newuser`.
```bash
usermod -d /home/newuser -m newuser
```
### Verify
```bash
id newuser
echo ~newuser
```
```bash
grep vahid /etc/passwd
```
Output:
```bash
newuser:x:1001:1001::/home/newuser:/bin/bash
```
Logout and Login!

---

# Move file
```bash
rsync -a /path/to/folder1/ /path/to/folder2/
cp -r /path/to/folder1/* /path/to/folder2/
```

---

# Check the service
```bash
systemctl list-unit-files
systemctl list-units --type=service
systemctl list-units --type=service --state=running
service --status-all
```

---
# Network
### show the ip address:
```bash
ip -br -c -4 a # -br: breake , -c: color , -4: show ipv4 , a: addr
hostname -I
nmcli device status
nmcli device show
```
```bash
netstat -na    # show all ports
netstat -na | grep LISTEN
netstat -tulnp # show usage port
> grep -o done logfile.log | wc -l # count "done" word in log file
```
### If have problem to get package or get 403 error
```bash
sudo systemctl restart NetworkManager
```

---

# Add local hosts
```bash
nano /etc/hosts
```
```vim
127.0.0.1 example.domain.com
```

---

# Git command
```bash
git config --global user.email "you@example.com"
git config --global user.name "Your Name"  
git commit -a -m 'Some message about the change'
git push origin 'branch-name'
```

---

# Compress
```bash
tar -czvf archive_name.tar.gz -C /path/to/directory .
zip -r archive_name.zip /path/to/directory
# open
tar -xzvf archive_name.tar.gz -C directory
unzip archive_name.zip
```
```bash
sudo tar -cpf file-name.tar -C /path/to/directory .
```
* `c` = compress
* `p` = hold premission
* `f` = file name
* `.` = just files in this directory

```bash
tar -xpf file-name.tar -C /dest/path/
```
* `x` = extract

---

# Send file
```bash
# Upload
scp /path/to/local/file username@remote_host:/path/to/remote/directory
scp -r /path/to/local/directory username@remote_host:/path/to/remote/directory
# Download 
scp username@remote_host:/path/to/remote/file /path/to/local/directory
scp -r username@remote_host:/path/to/remote/directory /path/to/local/directory
# if use another port
scp -P <ssh port number>
```

---

# Kill PID
```bash
ps aux | grep filename.py
ps aux | grep 'oc mirror'
kill <PID>
```

---

# curl
curl is used in command lines or scripts to transfer data.
```bash
curl --version
curl https://example.com
curl -o output.out https://example.com # The received html output is saved in output.out
curl -o downloaded.zip https://tosinso.com/file.zip # Download file
curl -I https://example.com # HTTP headers
curl -v https://example.com
curl -vI https://example.com
```

---

# base64
```bash
echo -n 'my-string' | base64
bXktc3RyaW5n

echo -n 'bXktc3RyaW5n' | base64 --decode
my-string

base64 <<< 'Hello, World!'
SGVsbG8sIFdvcmxkIQo=

base64 -d <<< SGVsbG8sIFdvcmxkIQo=
Hello, World!
```

---

# Add self-sign CA
* You can download the CA from browser.
## Debian/Ubuntu:
```bash
sudo cp ca.crt /usr/local/share/ca-certificates/vcsa.crt
sudo update-ca-certificates
```
## RHEL/CentOS/Fedora
```bash
sudo cp ca.crt /etc/pki/ca-trust/source/anchors/
sudo update-ca-trust
```

---
