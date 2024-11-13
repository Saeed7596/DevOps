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
1. in zabbix dashbord
2. select host
3. create item
4. type item:Zabbix trapper
5. key=mongodb_status
6. Type of information= Text
-------------------------------
# Preprocessing
1. in zabbix dashbord
2. select Latest data of your host
3. Name=mongodb_status then select Apply
4. click on mongodb_status item
5. Cerate dependent item
6. Name=mongodb_Slow Ops Count
7. Type: Dependent item
8. Key=mongodb.slow_ops_count
9. select tab Preprocessing
10. JSONPath = $.slow_ops_count
-------------------------------
# Grafana
`item = mongodb_Slow Ops Count`
