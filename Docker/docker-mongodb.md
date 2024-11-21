```bash
docker network create mongodb-net
```
```yml
#version: "3.9" # in latest update we don't need write the version
services:
  mongodb:
    container_name: mongodb
    image: mongo:7
    environment:
      MONGO_INITDB_ROOT_USERNAME: root
      MONGO_INITDB_ROOT_PASSWORD: password
    ports:
      - 27017:27017
    volumes:
      - ./dbdata:/data/db
    restart: unless-stopped
    networks:
      - mongodb-net

networks:
  mongodb-net:
    external: true
      #name: mongodb-net
#volumes: # if using local volume don't neet add volumes
#  dbdata:
```
# BackUp
* Maybe you need to install this on server ubuntu2204:
[`mongodb-database-tools-ubuntu2204-x86_64-100.10.0.deb`](https://www.mongodb.com/try/download/database-tools/releases/archive)
```sh
#!/bin/bash
echo "dumping started" &&
fromUri="mongodb://root:password@server ip:password/URL" &&
mongodump --uri "$fromUri" -o /tmp/temp_db_backup &&
echo "restoring started" &&
toUri="mongodb://root:password@server ip:password/URL" &&
mongorestore --uri "$toUri" /tmp/temp_db_backup --drop --nsExclude="admin.*" --nsExclude="config.*" --nsExclude="local.*" &&
echo "done" &&
rm -rf /tmp/temp_db_backup &&
echo "removed"
```
# BackUp and keep last 3 days
```sh
#!/bin/bash

BACKUP_DIR="/home/mongo/mongo_backup"
ARCHIVE_DIR="/home/mongo/mongo_archives"
DATE=$(date +"%Y-%m-%d_%H-%M-%S")

mkdir -p "$BACKUP_DIR"
mkdir -p "$ARCHIVE_DIR"

echo "Backup process started at $(date)"

FROM_URI="mongodb://url?authSource=admin"
mongodump --uri "$FROM_URI" -o "$BACKUP_DIR/$DATE"

tar -czf "$ARCHIVE_DIR/mongo_backup_$DATE.tar.gz" -C "$BACKUP_DIR" "$DATE"

rm -rf "$BACKUP_DIR/$DATE"

echo "Backup archived as mongo_backup_$DATE.tar.gz"

cd "$ARCHIVE_DIR"
ls -t | sed -e '1,3d' | xargs -d '\n' rm -f

echo "Cleanup completed. Backup process finished at $(date)"
```
# cronjob
```
sudo crontab -e
sudo crontab -l
```
```
0 3 * * * /path/to/backup.sh >> /var/log/mongo_backup.log 2>&1
```
### log
```
cat /var/log/mongo_backup.log
```
