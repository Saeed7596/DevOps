```yml
version: '3.8'
services:
  grafana:
    image: grafana/grafana:latest
    container_name: grafana
    user: '0'
    ports:
      - "3000:3000"
    environment:
      #- GF_SECURITY_ADMIN_PASSWORD="your_password"
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
# If cat install plugin:
```bash
wget "https://storage.googleapis.com/integration-artifacts/grafana-mongodb-datasource/release/1.22.0/linux/grafana-mongodb-datasource-1.22.0.linux_amd64.zip
docker cp /path/to/mongodb-datasource.zip grafana:/var/lib/grafana/plugins/
docker exec -it grafana /bin/bash
unzip mongodb-datasource.zip
docker restart grafana
```
