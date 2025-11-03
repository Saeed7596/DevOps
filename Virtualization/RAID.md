# 🧱 RAID Configuration on HP ProLiant DL380 Gen9

Before installing **VMware ESXi**, you need to configure RAID on your server using the built-in Smart Array controller.

---

## 🛠 Step 1: Access RAID Configuration Utility

1. Power on or reboot the server.
2. During the POST screen, watch for a message like:
- Press F8 to Configure Smart Array Controller
- It may also be `F9` or enter through **Intelligent Provisioning** (`F10`).
3. Press the key indicated to open the **Smart Array Configuration Utility**.

---

## ⚙️ Step 2: Create a RAID Array (Logical Drive)

1. Once inside the RAID utility, choose `Create Array` or `Create Logical Drive`.
2. Select the physical disks you want to include in the array.
3. Choose the RAID level:
- **RAID 0**: Striping (No redundancy)
- **RAID 1**: Mirroring (Recommended for 2 disks)
- **RAID 5**: Striping with parity (Min. 3 disks)
- **RAID 10**: Mirrored stripe (Min. 4 disks)
4. Set additional options (optional):
- Stripe size
- Caching and write policy
5. Confirm and create the logical drive.

---

## 💾 Step 3: Save and Exit

1. Save your configuration.
2. Exit the RAID utility.
3. Reboot the server.

---

## ✅ After RAID Setup

- Your new **logical drive** will now appear as a single disk during the ESXi installation.
- Proceed with booting into your ESXi installation media and follow the normal install steps.

---

## 📝 Notes

- Make sure all disks in the RAID are of similar size and speed for optimal performance.
- RAID 1 or 10 is generally preferred for critical systems due to redundancy.
- RAID 5 offers a good balance of storage and fault tolerance but has slower write performance.

---

Happy RAIDing! 🔧
