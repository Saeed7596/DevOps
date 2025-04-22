[Vagrant](https://www.vagrantup.com/)
# 📦 Vagrant Cheat Sheet

## 🚀 Getting Started

```bash
vagrant init                   # Initialize a new Vagrantfile in current directory
vagrant up                     # Start and provision the Vagrant environment
vagrant ssh                   # SSH into the running VM
vagrant halt                  # Shut down the running VM
vagrant destroy               # Destroy the VM and all resources
```

---

## 📁 Boxes

```bash
vagrant box add <box-name>    # Add a new box
vagrant box list              # List all installed boxes
vagrant box remove <box-name> # Remove a box
```

---

## 🔄 Provisioning

```bash
vagrant provision             # Run the provisioners again
vagrant reload --provision   # Restart and re-provision the VM
```

---

## 📂 Synced Folders

- Shared folder between host and guest:
```ruby
config.vm.synced_folder "src/", "/home/vagrant/src"
```

---

## 🌍 Networking

```ruby
config.vm.network "forwarded_port", guest: 80, host: 8080
config.vm.network "private_network", type: "dhcp"
config.vm.network "public_network"
```

---

## 🧱 Multi-Machine Setup

```ruby
Vagrant.configure("2") do |config|
  config.vm.define "web" do |web|
    web.vm.box = "ubuntu/bionic64"
  end

  config.vm.define "db" do |db|
    db.vm.box = "ubuntu/bionic64"
  end
end
```

---

## 📝 Useful Commands

```bash
vagrant status                # Show status of the Vagrant machine
vagrant global-status         # List all Vagrant environments on system
vagrant suspend               # Suspend the VM
vagrant resume                # Resume a suspended VM
vagrant reload                # Restart the VM
```

---

## 🛠️ Vagrantfile Sample

```ruby
Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/bionic64"

  config.vm.network "forwarded_port", guest: 80, host: 8080
  config.vm.synced_folder "./data", "/vagrant_data"

  config.vm.provision "shell", inline: <<-SHELL
    apt-get update
    apt-get install -y apache2
  SHELL
end
```

---

## ✅ Tips

- Always use `vagrant halt` before `vagrant destroy` to safely shut down.
- Use `vagrant snapshot save <name>` and `vagrant snapshot restore <name>` for backup & recovery.

---

Happy Vagranting! 📦
