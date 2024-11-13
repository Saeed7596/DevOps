```bash
nano /etc/systemd/system/mongodb_status.service
```
```vim
[Unit]
Description=MongoDB Monitoring Script

[Service]
ExecStart=/usr/bin/python3 /home/monitoring/mongodb_status.py
Restart=always
User=your_user

[Install]
WantedBy=multi-user.target
```
```bash
sudo systemctl daemon-reload
sudo systemctl enable mongodb_status.service
sudo systemctl start mongodb_status.service
```
```bash
sudo systemctl stop mongodb_status.service
sudo systemctl disable mongodb_status.service
```
