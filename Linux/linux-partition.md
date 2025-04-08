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

---

# Expanding Root Partition (`/`) with Additional Space

If you've added extra space to your disk and want to extend your root partition (`/`), follow these steps:

### 1. Check Disk Partitions
Use `fdisk` to manage your partitions:
```bash
sudo fdisk /dev/sda
```

### 2. List Current Partitions
To view the existing partitions, use the following command:
```bash
p
```

This will display the partitions on `/dev/sda`, showing the new 50GB space added to `sda3`.

### 3. Delete the Existing Partition (`sda3`)
To delete the existing partition, run:
```bash
d
3
```
This will delete partition `sda3` but without erasing data, as we’ll recreate it with the additional space.

### 4. Create a New Partition with Additional Space
Now create a new partition to use the additional space:
```bash
n
```
- Choose `p` for a primary partition.
- Set the partition number to `3` (to recreate partition `sda3`).
- Accept the default starting sector.
- Accept the default ending sector to use the full available space.

When asked if you want to remove the LVM signature, choose **N** to keep the LVM signature:
```bash
N
```

### 5. Save Changes
After making the changes, save them with:
```bash
w
```

### 6. Resize the Physical Volume (PV)
Now resize the physical volume to recognize the additional space:
```bash
sudo pvresize /dev/sda3
```

### 7. Extend the Logical Volume (`rhel-root`)
Next, extend the logical volume that holds the root (`/`) partition:
```bash
sudo lvextend -l +100%FREE /dev/mapper/rhel-root
```

### 8. Expand the Filesystem
Finally, expand the filesystem to utilize the new space:
```bash
sudo xfs_growfs /dev/mapper/rhel-root
```

### 9. Verify the Changes
Check the available space with:
```bash
df -h
lsblk
```

This should show the additional space available in the root partition (`/`).
