# Install mongos
```bash
wget https://downloads.mongodb.com/compass/mongosh-2.3.3-linux-x64.tgz
tar -zxvf mongosh-2.3.3-linux-x64.tgz
cd mongosh-2.3.3-linux-x64.tgz
chmod +x bin/mongosh
cd bin
sudo cp mongosh /usr/local/bin/
sudo cp mongosh_crypt_v1.so /usr/local/lib/
cd ..
sudo ln -s $(pwd)/bin/* /usr/local/bin/
```
-------------------------------
# Add key in zabbix
> in zabbix dashbord
> select host
> create item
> type item:Zabbix trapper
> key=mongodb_status
> Type of information= Text
-------------------------------
# Preprocessing
> in zabbix dashbord
> select Latest data of your host
> Name=mongodb_status then select Apply
> click on mongodb_status item
> Cerate dependent item
> Name=mongodb_Slow Ops Count
> Type: Dependent item
> Key=mongodb.slow_ops_count
> select tab Preprocessing
> JSONPath = $.slow_ops_count
-------------------------------
# Grafana
item = mongodb_Slow Ops Count
