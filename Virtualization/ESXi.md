# 🖥️ ESXi 8 Installation Guide for HP ProLiant DL380 Gen9

This guide walks you through the steps to install **VMware vSphere Hypervisor (ESXi) 8** on an **HP ProLiant DL380 Gen9** server.

---

## ✅ Prerequisites

- HP ProLiant DL380 Gen9 with latest firmware
- At least 8GB RAM (recommended 32GB+)
- USB drive (at least 8GB) or virtual media
- ESXi 8 ISO image (from VMware official site)
- iLO access (optional but recommended)
- Static IP or DHCP available

---

## 📥 Step 1: Prepare Installation Media

1. Download the **ESXi 8 ISO** from VMware's [official website](https://customerconnect.vmware.com).
2. Use **Rufus**, **Balena Etcher**, or **VMware USB Creator** to write the ISO to a USB drive.
3. Alternatively, mount ISO using iLO remote console (virtual media).

---

## 🛠 Step 2: BIOS and Firmware Update (Recommended)

1. Boot into iLO (press `F8` during POST).
2. Ensure firmware is up-to-date:
   - Use **HP SPP (Service Pack for ProLiant)** or HPE iLO.
3. In BIOS (`F9`), set:
   - Boot Mode: **UEFI**
   - Enable **Virtualization Technology**
   - Enable **VT-d** (if needed for passthrough)
   - Set USB boot (if using USB)

---

## 💽 Step 3: Boot and Install ESXi

1. Insert USB or mount ISO via iLO.
2. Reboot and press `F11` for **boot menu**, select your installation media.
3. ESXi installer will load.
4. Accept the license agreement.
5. Select installation disk (RAID volume or SSD).
6. Choose keyboard layout and set root password.
7. Confirm and begin installation.
8. After completion, remove installation media and reboot.

---

## ⚙️ Step 4: Post-Installation Configuration

1. On first boot, press `F2` to **Customize System**:
   - Set static IP
   - Configure DNS
   - Set hostname
2. Save and exit.

---

## 🌐 Step 5: Access ESXi Web UI

1. Open a browser and go to: `https://<your-esxi-ip>`
2. Login using:
   - Username: `root`
   - Password: *(your chosen password)*
3. You now have access to the **vSphere Host Client** UI.

---

## 📦 Step 6: Optional - Install HPE Custom ESXi Image

- HPE provides a customized image with:
  - HPE management agents
  - Optimized drivers for Gen9 hardware
- [Download from HPE VMware Support Site](https://www.hpe.com/info/esxi)

---

## 🔐 Step 7: Best Practices

- Change the default root password.
- Set up time synchronization (NTP).
- Enable SSH only when needed.
- Register the host in vCenter (if available).
- Backup host configuration.

---

## 🧯 Troubleshooting Tips

- If disks are not detected, check RAID configuration in `F10` (Intelligent Provisioning).
- Use iLO logs and console for remote diagnostics.
- Ensure UEFI boot mode is enabled.

---

Happy Virtualizing! 🚀
