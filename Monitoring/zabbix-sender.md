# Zabbix Sender vs Zabbix Agent

| Feature              | **Zabbix Sender**                                             | **Zabbix Agent**                                                |
|----------------------|--------------------------------------------------------------|-----------------------------------------------------------------|
| **Purpose**          | Sends data to Zabbix Server manually or from scripts.        | Collects and sends monitoring data automatically to Zabbix Server. |
| **Usage**            | Best for sending ad-hoc or custom metrics.                   | Best for continuous system monitoring.                         |
| **Installation**     | Requires `zabbix-sender` package.                            | Requires `zabbix-agent` package.                               |
| **Operation Mode**   | Command-line tool executed manually or within scripts.       | Runs as a background service (daemon).                        |
| **Data Collection**  | Does not collect data automatically; relies on input from scripts or commands. | Collects predefined metrics automatically, e.g., CPU, memory, disk. |
| **Real-time Sending**| Sends data immediately upon execution.                       | Sends data at regular intervals (configured in the agent).     |
| **Key Example**      | Send a custom metric from a script: `zabbix_sender -z <server> -s <host> -k <key> -o <value>` | Automatically sends data about system performance (e.g., CPU usage). |

#  Install zabbix-sender
```bash
apt install zabbix-sender
```
### If get this error: `E: Unable to locate package zabbix-sender`
- Update Repository
- Find your repo in this site [https://repo.zabbix.com/zabbix/](https://repo.zabbix.com/zabbix/)
- Download the .deb file for zabbix-sender and install it manually.
- for example, for linux `focal`
```bash
wget https://repo.zabbix.com/zabbix/7.2/release/ubuntu/pool/main/z/zabbix-release/zabbix-release_7.2-0.1%2Bubuntu20.04_all.deb
sudo dpkg -i ./zabbix-release_7.2-0.1+ubuntu20.04_all.deb
sudo apt update
sudo apt install zabbix-sender
```
### If you have `zabbix-agent` with docker compose, must stop the `zabbix-sender`
```bash
systemctl status zabbix-agent.service
systemctl stop zabbix-agent.service
```
