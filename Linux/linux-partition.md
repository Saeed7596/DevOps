# LVM Partitioning Scheme (for a 100GB Disk)
| Mount Point   | Size  | Description                                         |
|---------------|-------|-----------------------------------------------------|
| `/boot/efi`   | 600M  | EFI system partition (for UEFI boot)                |
| `/boot`       | 1G    | Stores the kernel and bootloader files              |
| `/`           | 25G   | Root partition for OS and applications              |
| `/home`       | 30G   | User files and personal data                        |
| `/var`        | 15G   | Logs, cache, and databases                          |
| `swap`        | 4G    | Swap space (usually equal or half of your RAM)      |
| `/tmp`        | 2G    | Temporary files                                     |
| Free space    | ~22.4G| Reserved for future expansion of logical volumes    |

---

# `xfs` vs. `ext4` File System Comparison
| Feature              | `xfs`                                   | `ext4`                        |
|----------------------|------------------------------------------|-------------------------------|
| Performance (large files) | Excellent                           | Good                          |
| General performance   | Fast for most operations                | Stable and well-tested        |
| LVM Compatibility     | Great                                   | Great                         |
| Recovery Tools        | Limited                                 | More mature and available     |
| Best suited for       | Servers, databases, logs                | Desktops, general use         |

---

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

---

# Growpart Quick Guide
## Introduction
`growpart` is a Linux utility used to safely and automatically extend a partition to fill the available disk space without losing existing data. It's much safer and faster than manually editing partitions with `fdisk` or `parted`.

---

## When to Use
* You resized a virtual disk (VMware, Hyper-V, etc.)
* Your server needs more space on an existing partition
* You want to avoid manual and risky partition deletion/recreation

---

## How `growpart` Works
* It expands an existing partition (e.g., `/dev/sda3`) into the available free space
* It does **NOT** resize the filesystem itself (you must do that separately)

## Install Growpart
Depending on your Linux distribution:
**RHEL / CentOS / Rocky / AlmaLinux:**
```bash
sudo yum install cloud-utils-growpart
```

**Ubuntu / Debian:**
```bash
sudo apt update
sudo apt install cloud-guest-utils
```

**SUSE / openSUSE:**
```bash
sudo zypper install cloud-utils-growpart
```

---

## Basic Usage
```bash
sudo growpart /dev/<device> <partition_number>
```
**Example:**
```bash
sudo growpart /dev/sda 3
```
This expands `/dev/sda3` to use all free space on the disk.

---

### Resize Physical Volume
```bash
sudo pvresize /dev/sda3
```

---

### Extend Logical Volume (For Example: /home)
```bash
sudo lvextend -l +100%FREE /dev/rhel/home
```

---

## Next Step: Expand Filesystem
After extending the partition, you must also expand the filesystem inside it.

### If ext4 filesystem:
```bash
sudo resize2fs /dev/mapper/<your_logical_volume>
```
**Example for ext4:**
```bash
sudo resize2fs /dev/mapper/rhel-home
```
### If XFS filesystem:
```bash
sudo xfs_growfs /mount/point
```
**Example for XFS on `/home` mount point:**
```bash
sudo xfs_growfs /home
```

---

## Important Notes

* `growpart` does **not** destroy any data
* It works with both **MBR** and **GPT** partition tables
* If your system uses **LVM**, after `growpart`, you may also need to extend the Volume Group (VG) and Logical Volume (LV) accordingly
* In some rare cases, a reboot may be needed, but usually not

## Troubleshooting

* **"device not found" error:** Ensure you have the correct device name and partition number.
* **"not a partition table" error:** The target disk might not have a proper partition table.

---

# Check
```bash
df -h /home
sudo lvs
sudo vgs
sudo pvs
```

---

## Summary

| Step                        | Command Example                             |
| --------------------------- | ------------------------------------------- |
| 1. Install growpart         | `sudo yum install cloud-utils-growpart`     |
| 2. Expand Partition         | `sudo growpart /dev/sda 3`                  |
| 3. Resize Physical Volume   | `sudo pvresize /dev/sda3`                   |
| 4. Extend Logical Volume    | `sudo lvextend -l +100%FREE /dev/rhel/home` |
| 5. Expand Filesystem (ext4) | `sudo resize2fs /dev/mapper/rhel-home`      |
| 5. Expand Filesystem (xfs)  | `sudo xfs_growfs /home`                     |

---
