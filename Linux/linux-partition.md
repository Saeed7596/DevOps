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
