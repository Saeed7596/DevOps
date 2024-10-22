# Zabbix MySQL BackUps
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
