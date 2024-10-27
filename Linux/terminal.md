# Some useful terminal command
```bash
lsb_release -a   ===>   #ubuntu version
dpkg --print-architecture   ===>   #show ubuntu architect  (arm or amd)
du -sh /path/to/directory   ===>   #show size of a folder & file 
```
----------------------------------
# Create user
```bash
sudo useradd -m -s /bin/bash username
sudo passwd username
sudo usermod -aG sudo username
sudo -u username -i   ===>   #switch to user
ssh-keygen
```
----------------------------------
# Check the service
```bash
systemctl list-unit-files
systemctl list-units --type=service
systemctl list-units --type=service --state=running
service --status-all
```
----------------------------------
```bash
netstat -tulnp # show usage port
> grep -o done logfile.log | wc -l # count "done" word in log file
```
----------------------------------
# Run container after reboot:
```bash
docker run -d --restart unless-stopped <container name>
docker update --restart unless-stopped <container name>
```
----------------------------------
```bash
docker cp <container_name>:<path_inside_container> <path_on_host>
docker cp <path_on_host> <container_name>:<path_inside_container>
```
----------------------------------
```bash
docker system df
docker builder prune
```
----------------------------------
```bash
usermod -aG docker NEWUSER
```
----------------------------------
# Config ssh with ci cd
### in Destination server
```bash
~/.ssh$ cat id_rsa.pub > authorized_keys
and copy id_rsa in gitlab variables
```
----------------------------------
# change docker registry
```bash
nano /etc/docker/daemon.json
```
```vim
{ "insecure-registries" : [ "IPNexus:port" ] 
}
```
```bash
sudo docker login registry.example.com
```
```bash
sudo systemctl restart docker
```
-----------------------------------
# Add local hosts
```bash
nano /etc/hosts
```
```vim
127.0.0.1 example.domain.com
```
-----------------------------------
# Git command
```bash
git config --global user.email "you@example.com"
git config --global user.name "Your Name"  
git commit -a -m 'Some message about the change'
git push origin 'branch-name'
```
------------------------------------
# Compress
```bash
tar -czvf archive_name.tar.gz /path/to/directory
zip -r archive_name.zip /path/to/directory
# open
tar -xzvf archive_name.tar.gz
unzip archive_name.zip
```
------------------------------------
# Send file
```bash
# Upload
scp /path/to/local/file username@remote_host:/path/to/remote/directory
scp -r /path/to/local/directory username@remote_host:/path/to/remote/directory
# Download 
scp username@remote_host:/path/to/remote/file /path/to/local/directory
scp -r username@remote_host:/path/to/remote/directory /path/to/local/directory
# if use another port
scp -P port number
```
------------------------------------
