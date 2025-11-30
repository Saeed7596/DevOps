# [Grafana](https://grafana.com/docs/grafana/latest/setup-grafana/installation/docker/)
1. Create a `docker-compose.yaml` file
```bash
# first go into the directory where you have created this docker-compose.yaml file
cd /path/to/docker-compose-directory

# now create the docker-compose.yaml file
touch docker-compose.yaml
```
2. Create the directory where you will be mounting your data, in this case is `/data` e.g. in your current working directory:
```bash
mkdir $PWD/data
```
3. Now, add the following code into the `docker-compose.yaml` file.
```yml
services:
  grafana:
    image: grafana/grafana-enterprise
    container_name: grafana
    restart: unless-stopped
    # if you are running as root then set it to 0
    # else find the right id with the id -u command
    user: '0'
    ports:
      - '3000:3000'
    # adding the mount volume point which we create earlier
    volumes:
      - '$PWD/data:/var/lib/grafana'
```
With some environment for zabbix
```yaml
services:
  grafana:
    image: grafana/grafana:latest
    container_name: grafana
    user: '0'
    ports:
      - "3000:3000"
    environment:
      #- GF_SECURITY_ADMIN_PASSWORD="your_password"
      - GF_SERVER_ROOT_URL=http://my.grafana.server/
      - GF_PLUGINS_PREINSTALL=grafana-clock-panel
      - GF_INSTALL_PLUGINS=alexanderzobnin-zabbix-app
      #- GF_INSTALL_PLUGINS=grafana-mongodb-datasource # This plugin need the licence
    volumes:
      - ./grafana_data:/var/lib/grafana
    networks:
      - monitoring
    restart: unless-stopped

networks:
  monitoring:
    external: true  # The network must already be created
    
volumes:
  grafana_data:
```
4. Save the file and run the following command:
```bash
docker compose up -d
```

# Password in first login is: `admin:admin`

---

# If cat install plugin:
```bash
wget "https://storage.googleapis.com/integration-artifacts/grafana-mongodb-datasource/release/1.22.0/linux/grafana-mongodb-datasource-1.22.0.linux_amd64.zip
docker cp /path/to/mongodb-datasource.zip grafana:/var/lib/grafana/plugins/
docker exec -it grafana /bin/bash
unzip mongodb-datasource.zip
docker restart grafana
```
