```yaml
version: '3.8'

services:
  zabbix-agent2:
    image: zabbix/zabbix-agent2:latest
    container_name: zabbix-agent2
    user: "0"
    environment:
      - ZBX_HOSTNAME=<chose a name>
      - ZBX_SERVER_HOST=<ip of zabbix proxy or agent>
      - ZBX_SERVER_PORT=10050
      - Plugins.Docker.Enable=true
      - Plugins.Docker.ContainerStats=true
      - Plugins.Mongodb.Enable=false
      - Plugins.Postgresql.Enable=false
      - Plugins.Mssql.Enable=false
      - Plugins.Ember.Enable=false
    network_mode: host
    volumes:
      - /etc/localtime:/etc/localtime:ro
      - /etc/timezone:/etc/timezone:ro
      - /var/run/docker.sock:/var/run/docker.sock
      # - /etc/zabbix/zabbix_agent2.d:/etc/zabbix/zabbix_agent2.d
    restart: always
```
###In Zabbix host add template Docker by Zabbix agent 2

If not work uncomment the comment in volume and:
```bash
nano /etc/zabbix/zabbix_agent2.d/zabbix_agent2.conf
```
```conf
Plugins.Docker.Enable=true
Plugins.Docker.ContainerStats=true
Plugins.Mongodb.Enable=false
Plugins.Postgresql.Enable=false
Plugins.Mssql.Enable=false
Plugins.Ember.Enable=false
```
```bash
mkdir -p /etc/zabbix/zabbix_agent2.d/plugins.d
touch /etc/zabbix/zabbix_agent2.d/plugins.d/mongodb.conf
touch /etc/zabbix/zabbix_agent2.d/plugins.d/postgresql.conf
```
