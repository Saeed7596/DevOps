# Swap in Linux

Swap is a space on a disk that is used as virtual memory when the physical RAM (Random Access Memory) is fully utilized. When a system runs out of RAM, inactive pages in memory are moved to the swap space to free up RAM for active processes.

---

## **Why Use Swap?**

- **Extend Memory**: Swap provides additional memory when RAM is exhausted.
- **Stability**: Prevents applications from crashing due to lack of memory.
- **Hibernation**: Required for suspending a system to disk (hibernation).

---

## **Types of Swap**

1. **Swap Partition**: A dedicated disk partition for swap space.
2. **Swap File**: A file on an existing file system used as swap.

---

## **Check Current Swap Usage**

To view swap usage and details:
```bash
free -h
swapon --show
```
## **Creating Swap Space**
#### Using a Swap File
1: Create a Swap File
```bash
sudo fallocate -l 1G /swapfile
```
- `-l 1G`: Specifies the size of the swap file (1GB in this case).
If `fallocate` is not available, use `dd`:
```bash
sudo dd if=/dev/zero of=/swapfile bs=1M count=1024
```
2: Set Permissions
```bash
sudo chmod 600 /swapfile
```
3: Mark as Swap Space
```bash
sudo mkswap /swapfile
```
4: Enable the Swap File
```bash
sudo swapon /swapfile
```
5: Make Swap Persistent
Add the following line to `/etc/fstab`:
```vim
/swapfile none swap sw 0 0
```

---

#### Disable Swap
To temporarily disable swap:
```bash
sudo swapoff -a
```
