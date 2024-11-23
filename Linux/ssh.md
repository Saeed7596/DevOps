# Install
```bash
apt install openssh-server
systemctl status sshd
systemctl enable sshd
```
```bash
ssh-keygen
ssh -p <prot-number> username@remote_host
# In local machine:
ssh-copy-id -p 2222 username@remote_host # copy ~/.ssh/id_rsa.pub local machine to authorized_keys remote_host
nano .ssh/config
\
Host myserver
    HostName IP
    User myuser
    Port 2222
    IdentityFile ~/.ssh/id_rsa
\
ssh myserver
```
```bash
ls .ssh # Each user in the home directory has a .ssh directory, and the owner of this directory should be the user themselves.
```
# Change ssh port
```
sudo nano /etc/ssh/sshd_config
Port 2222
sudo ufw allow 2222/tcp
sudo ufw deny 22/tcp
sudo ufw status
sudo ufw app list
sudo ufw app info OpenSSH
# Make sure to open the port you are enabling in whatever firewall you are using.
sudo systemctl restart ssh
```
# Harden ssh
```bash
PasswordAuthentication no # Only users with SSH keys are allowed to login
PermitRootLogin no # User root does not access to login
PermitRootLogin prohibit-password # Only with SSH keys allowed to login
MaxAuthTries 3
MaxSessions 3
ClientAliveInterval 300
ClientAliveCountMax 0
LogLevel VERBOSE
sudo systemctl restart sshd
```
# Config ssh with ci cd
### in Destination server
```bash
~/.ssh$ cat id_rsa.pub > authorized_keys
and copy id_rsa in gitlab variables
```
