```bash
timedatectl
timedatectl list-timezones
timedatectl set-timezone Asia/Tehran
timedatectl set-ntp yes
```
### error = Failed to set ntp: NTP not supported
```bash
timedatectl show | grep NTPSynchronized # output => NTPSynchronized=no
```
```bash
sudo apt install systemd-timesyncd
sudo systemctl enable systemd-timesyncd
sudo systemctl start systemd-timesyncd
sudo systemctl restart systemd-timesyncd
sudo systemctl status systemd-timesyncd
sudo systemctl daemon-reload
```
```bash
timedatectl set-ntp yes
timedatectl show | grep NTPSynchronized # output => NTPSynchronized=yes
timedatectl status
```
```vim
System clock synchronized: yes
              NTP service: active
              RTC in local TZ: no
```
# Manual
```bash
sudo timedatectl set-ntp no
sudo date -s "YYYY-MM-DD HH:MM:SS"
sudo date -s "2024-11-25 20:30:30"
```
### With timestamp
```bash
curl -s https://api.keybit.ir/time/ | jq -r ".timestamp.en" | xargs -I {} sudo date -s @{}
```
### If use `ntp` or `chrony`
```bash
sudo systemctl stop ntp
sudo apt-get remove --purge ntp
sudo apt-get autoremove --purge
sudo apt-get autoclean
systemctl status ntp
```
