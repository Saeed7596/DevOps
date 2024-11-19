# Count header with nginx
* First line of `default.conf`
```conf 
log_format custom '$remote_addr - $remote_user [$time_local] "$request" '
                '$status $body_bytes_sent "$http_referer" '
                '"$http_user_agent" "$http_my_header"';

# or save just this headers
log_format custom '$http_host';
```
```conf
# add this if in location / part
        if ($http_referer = "https://example.ir/") {
            access_log /var/log/nginx/website-access.log custom;
        }
```
# Add volume in `docker-compose.yml`
```yml
volumes:
  - ./nginx_logs:/var/log/nginx
```
```bash
#for frirst time because can't create nginx_logs directory
docker compose - f docker-nginx.compose down
docker compose - f docker-nginx.compose up -d
#after any change in default.conf
docker compose - f docker-nginx.compose restart nginx
# or
docker exec nginx nginx -t
docker exec nginx nginx -s reload
```
# To send this logs to zabbix
```bash
apt install zabbix-sender
apt-get install jq
```
# If can't up the zabbix-agent with docker compose 
```
docker compose -f docker-zabbix.yml down
systemctl stop zabbix-agent.service
docker compose -f docker-zabbix.yml up -d
systemctl start zabbix-agent.service
```
```bash
nano count_requests.sh
```
```sh
#!/bin/bash
LOG_FILE="/your-path/nginx_logs/access.log"

declare -A count

while IFS= read -r line; do
  ((count["$line"]++))
done < "$LOG_FILE"

json_output="{"
for line in "${!count[@]}"; do
  json_output+="$(echo $line | jq -R .): ${count[$line]},"
done
json_output="${json_output%,}}"

#echo "$json_output"

zabbix_sender -z ip-zabbix-server-or-proxy -s "hostname-zabbix" -k "http.requests.count" -o "$json_output"

> "$LOG_FILE"
```
*in zabbix dashbord > select host > create item > type item:Zabbix trapper > key=http.requests.count*
----
*select item > Create dependet item > add Preprocessing > JSONPath = $.['example.ir']*
*or use this js file instead of JSONPath*
```js
var site1 = 'site1.com';
var site2 = 'site2.net';
var site3 = 'site3.ir';

var data = JSON.parse(value);

var count1 = data[site1] ? data[site1] : 0;
var count2 = data[site2] ? data[site2] : 0;
var count3 = data[site3] ? data[site3] : 0;

return count1 + count2 + count3;
```
```bash
chmod +x count_requests.sh
./count_requests.sh
crontab -e
```
```bash
* * * * * /path/to/your/script/count_requests.sh
```
