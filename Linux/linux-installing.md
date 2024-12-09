# Installing, Updating, and Removing a Package in Ubuntu

Ubuntu uses the **APT (Advanced Package Tool)** to manage software packages. Below are the steps to install, update, and remove a package.

## 1. Installing a Package
To install a package, use the `apt install` command. For example, to install **curl**:

```bash
sudo apt update      # Update the package list
sudo apt install curl # Install the package
```

- The `sudo apt update` command ensures that your local package index is up to date.
- The `sudo apt install <package-name>` installs the desired package.

## 2. Updating a Package
To update a specific package, use the `apt install` command with the package name. For instance:

```bash
sudo apt update           # Update the package list
sudo apt install --only-upgrade curl # Upgrade the curl package
```

- The `--only-upgrade` flag ensures that the package is only updated if it is already installed.

To update all packages on your system:

```bash
sudo apt update
sudo apt upgrade
sudo reboot
```

## 3. Removing a Package
To remove an installed package, use the `apt remove` command. For example, to remove **curl**:

```bash
sudo apt remove curl
```

- This removes the package but leaves its configuration files.

To remove the package along with its configuration files:

```bash
sudo apt purge curl
```

## 4. Cleaning Up
After installing, updating, or removing packages, you can free up disk space using:

```bash
sudo apt autoremove   # Removes unnecessary dependencies
sudo apt autoclean    # Removes cached package files
```

These commands help keep your system clean and efficient.

---

# .deb
## Download Package
```bash
wget -O package-name.deb "https://example.com/path-to-package.deb"
or
curl -o package-name.deb "https://example.com/path-to-package.deb"
```
## Install
```bash
sudo dpkg -i package-name.deb
```
- install dependency
  ```bash
  sudo apt-get install -f
  ```
## Check which Packages are installed
```bash
dpkg -l
or
dpkg --get-selections
# To find out if a package is already installed
dpkg -l | grep package-name
```
## Remove
```bash
sudo dpkg -r package-name
```
For more details on package management, you can refer to the official [Ubuntu documentation](https://help.ubuntu.com/).

