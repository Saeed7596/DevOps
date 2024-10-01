```bash
docker network create mongodb-net
```
```yaml
version: "3.3"
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
    external:
      name: mongodb-net
volumes:
  dbdata:
```
* Maybe you need to install this on server:
`mongodb-database-tools-ubuntu2204-x86_64-100.10.0.deb`
```sh
#!/bin/bash
echo "dumping started" &&
fromUri="mongodb://root:password@server ip:password/URL" &&
mongodump --uri "$fromUri" -o /tmp/temp_db_backup &&
echo "restoring started" &&
toUri="mongodb://root:password@server ip:password/URL" &&
mongorestore --uri "$toUri" /tmp/temp_db_backup --drop --nsExclude="admin.*" --nsExclude="config.*" --nsExclude="local.*" &&
echo "done"
rm -rf /tmp/temp_db_backup
echo "removed"
```
