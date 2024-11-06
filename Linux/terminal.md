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
sudo -u username -i   ===>   # switch to user
ssh-keygen
sudo -s # switch to super user
# in Linux $ means normal user access and # means super user (root) access
```
----------------------------------
# Move file
```bash
rsync -a /path/to/folder1/ /path/to/folder2/
cp -r /path/to/folder1/* /path/to/folder2/
```
----------------------------------
# Standard Partition Steps
```vim
fdisk -> mkfs -> mount -> /etc/fstab -> mount -a
```
# fdisk
```bash
df -h
lsblk
sudo fdisk -l
sudo fdisk /dev/sdb #`p=print, n=new(p=primary, e=extended), d=delete, t=type, w=write(save)`
sudo mkfs -t ext4 /dev/sdb1
echo $? # If it returns 0, it means that the previous command was executed correctly
sudo mkdir /path/to-mount/directory
sudo mount /dev/sdb1 /path/to-mount/directory
blkid /dev/sdb1 # show UUID
sudo nano /etc/fstab
UUID=your-uuid /path/to-mount/directory ext4 defaults 0 2
mount -a # check
```
# LVM
```bash
sudo fdisk -l
sudo fdisk /dev/sdb # n , t=8e (type=Linux LVM) , w
pvs #show phisical volume
vgs #show volume group
lvs #show logical volume
sudo pvcreate /dev/sdb1
sudo vgcreate vg_data /dev/sdb1
sudo lvcreate -l 100%FREE -n lv_data vg_data # sizing = -L +5G
sudo mkfs.ext4 /dev/vg_data/lv_data
sudo mkdir /path/to-mount/directory
sudo mount /dev/vg_data/lv_data /path/to-mount/directory
echo '/dev/vg_data/lv_data /path/to-mount/directory ext4 defaults 0 0' | sudo tee -a /etc/fstab
mount -a # check
```
# Increasing the space of the Logical Volume
```bash
sudo lvextend -l 100%FREE -r /dev/vg_data/lv_data #if use -r don't resize2fs run next command
sudo resize2fs /dev/vg_data/lv_data
sudo apt install scsitools
rescan-scsi-bus
```
# Reducing the Logical Volume space (optional)
```bash
sudo resize2fs /dev/vg_data/lv_data 5G
sudo lvreduce -L 5G /dev/vg_data/lv_data
```
# Delete LVM
```bash
sudo lvremove /dev/vg_data/lv_data
sudo vgremove vg_data
sudo pvremove /dev/sdb1
```
# Unmount
```bash
sudo umount <mount_point_or_device>
```
# /etc/fstab number
```vim
The first number (backup): This number specifies whether this file system should be backed up by the dump command or not.

0 means no backup.
1 means to make a backup.
The second number (checking the file system): This number specifies whether the file system will be checked during boot and what is the priority of checking it.

0 means no checking.
1 means to check the root file system first.
2 is used for other filesystems to be checked after the root filesystem.
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
tar -czvf archive_name.tar.gz -C /path/to/directory .
zip -r archive_name.zip /path/to/directory
# open
tar -xzvf archive_name.tar.gz -C directory
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
scp -P <ssh port number>
```
------------------------------------
