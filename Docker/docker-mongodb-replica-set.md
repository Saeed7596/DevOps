# Mongodb Replica Set Docker Compose
```bash
docker network create mongodb-net
```
```bash
nano docker-mongo-replica.yml
```
```yml
version: '3.8'

services:
  mongo1:
    container_name: mongo1
    image: mongo:7
    volumes:
      - ./mongors/data1:/data/db
      - ./rs-init.sh:/scripts/rs-init.sh
    networks:
      - mongodb-net
    ports:
      - 27031:27017
    links:
      - mongo2
      - mongo3
    restart: always
    entrypoint: [ "/usr/bin/mongod", "--bind_ip_all", "--replSet", "dbrs" ]
  mongo2:
    container_name: mongo2
    image: mongo:7
    volumes:
      - ./mongors/data2:/data/db
    networks:
      - mongodb-net
    ports:
      - 27032:27017
    restart: always
    entrypoint: [ "/usr/bin/mongod", "--bind_ip_all", "--replSet", "dbrs" ]
  mongo3:
    container_name: mongo3
    image: mongo:7
    volumes:
      - ./mongors/data3:/data/db
    networks:
      - mongodb-net
    ports:
      - 27033:27017
    restart: always
    entrypoint: [ "/usr/bin/mongod", "--bind_ip_all", "--replSet", "dbrs" ]

networks:
  mongo_net:
    external: true
```
```bash
nano rs-init.sh
```
```conf
#!/bin/bash

mongosh <<EOF
var config = {
    "_id": "dbrs",
    "version": 1,
    "members": [
        {
            "_id": 1,
            "host": "mongo1:27017",
            "priority": 3
        },
        {
            "_id": 2,
            "host": "mongo2:27017",
            "priority": 2
        },
        {
            "_id": 3,
            "host": "mongo3:27017",
            "priority": 1
        }
    ]
};
rs.initiate(config, { force: true });
rs.status();

use admin;
db.createUser({
    user: "admin",
    pwd: "password",
    roles: [ { role: "root", db: "admin" } ]
});
EOF
```
```bash
chmod +x rs-init.sh
```
```bash
docker exec -it mongo1 bash
```
```bash
cd scripts/
./rs-init.sh
```
