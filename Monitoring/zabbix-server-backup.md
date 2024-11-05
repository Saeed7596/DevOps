# Zabbix MySQL BackUps
```
docker compose -f docker-zabbix-server.yml stop
```
```bash
#!/bin/bash

MYSQL_CONTAINER_NAME="mysql"
MYSQL_USER="zabbix"
MYSQL_PASSWORD="zabbix_password"
MYSQL_DATABASE="zabbix"

BACKUP_PATH="/path/to/backup"
DATE=$(date +"%Y%m%d_%H%M%S")
DB_BACKUP_FILE="$BACKUP_PATH/zabbix_db_backup_$DATE.sql"

docker exec -t $MYSQL_CONTAINER_NAME mysqldump -u $MYSQL_USER -p$MYSQL_PASSWORD $MYSQL_DATABASE > $DB_BACKUP_FILE

if [ $? -eq 0 ]; then
    echo "Database backup successfully saved to $DB_BACKUP_FILE"
else
    echo "Database backup failed"
fi
```
# Zabbix MySQL & Volume BackUps
```bash
#!/bin/bash

MYSQL_CONTAINER_NAME="mysql"
MYSQL_USER="zabbix"
MYSQL_PASSWORD="zabbix_password"
MYSQL_DATABASE="zabbix"

BACKUP_PATH="/path/to/backup"
DATE=$(date +"%Y%m%d_%H%M%S")

DB_BACKUP_FILE="$BACKUP_PATH/zabbix_db_backup_$DATE.sql"
VOLUMES_BACKUP_FILE="$BACKUP_PATH/zabbix_volumes_backup_$DATE.tar.gz"

docker exec -t $MYSQL_CONTAINER_NAME mysqldump -u $MYSQL_USER -p$MYSQL_PASSWORD $MYSQL_DATABASE > $DB_BACKUP_FILE

if [ $? -eq 0 ]; then
    echo "Database backup successfully saved to $DB_BACKUP_FILE"
else
    echo "Database backup failed"
    exit 1
fi

tar -cvzf $VOLUMES_BACKUP_FILE ./zabbix_server_data ./zabbix_web_data

if [ $? -eq 0 ]; then
    echo "Zabbix volumes backup successfully saved to $VOLUMES_BACKUP_FILE"
else
    echo "Zabbix volumes backup failed"
    exit 1
fi

```
# Restore Zabbix MySQL 
```bash
docker compose -f docker-zabbix-server.yml stop
docker exec -i mysql mysql -u zabbix -pzabbix_password zabbix < /path/to/backup/zabbix_db_backup.sql

docker exec -i <mysql_container_name> mysql -u zabbix -p'zabbix_pass' -e "DROP DATABASE IF EXISTS zabbix; CREATE DATABASE zabbix;"
docker exec -i <mysql_container_name> mysql -u zabbix -p'zabbix_pass' zabbix < /path/to/your/backup_file.sql
docker exec -i <mysql_container_name> mysql -u root -p'root_pass' zabbix < /path/to/your/backup_file.sql

docker compose -f docker-zabbix-server.yml start
```
# Restore Zabbix MySQL & Docker Volume
```bash
docker compose down
tar -xvzf /path/to/backup/zabbix_volumes_backup.tar.gz -C /path/to/compose/project
docker compose up -d
```
