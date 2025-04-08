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
```bash
sudo useradd -m -s /bin/bash username
sudo passwd username
sudo usermod -aG sudo username
sudo -u username -i   ===>   # switch to user
ssh-keygen
sudo -s # switch to super user
# in Linux $ means normal user access and # means super user (root) access
```

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
netstat -tulnp # show usage port
> grep -o done logfile.log | wc -l # count "done" word in log file
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

