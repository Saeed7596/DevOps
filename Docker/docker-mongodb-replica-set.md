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
      - ./mongo-keyfile:/etc/mongo-keyfile
    networks:
      - mongodb-net
    ports:
      - 27031:27017
    links:
      - mongo2
      - mongo3
    restart: always
    entrypoint: [ "/usr/bin/mongod", "--bind_ip_all", "--replSet", "dbrs", "--keyFile", "/etc/mongo-keyfile"]
  mongo2:
    container_name: mongo2
    image: mongo:7
    volumes:
      - ./mongors/data2:/data/db
      - ./mongo-keyfile:/etc/mongo-keyfile
    networks:
      - mongodb-net
    ports:
      - 27032:27017
    restart: always
    entrypoint: [ "/usr/bin/mongod", "--bind_ip_all", "--replSet", "dbrs", "--keyFile", "/etc/mongo-keyfile"]
  mongo3:
    container_name: mongo3
    image: mongo:7
    volumes:
      - ./mongors/data3:/data/db
      - ./mongo-keyfile:/etc/mongo-keyfile
    networks:
      - mongodb-net
    ports:
      - 27033:27017
    restart: always
    entrypoint: [ "/usr/bin/mongod", "--bind_ip_all", "--replSet", "dbrs", "--keyFile", "/etc/mongo-keyfile"]

networks:
  mongodb-net:
    external: true
```
```bash
openssl rand -base64 756 > mongo-keyfile
chmod 600 mongo-keyfile
chown 999:999 mongo-keyfile
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
            "host": "<ip-server>:27031",
            "priority": 3
        },
        {
            "_id": 2,
            "host": "<ip-server>:27032",
            "priority": 2
        },
        {
            "_id": 3,
            "host": "<ip-server>:27033",
            "priority": 1
        }
    ]
};
rs.initiate(config, { force: true });
rs.status();
EOF
```
```bash
chmod +x rs-init.sh
```
```bash
docker compose -f docker-mongo-replica.yml up -d
```
### 30 seconds wait
```bash
docker exec -it mongo1 /scripts/rs-init.sh
```
##Create user
```bash
docker exec -it mongo1 mongosh
```
```bash
use admin;
```
```bash
db.createUser({
    user: "username",
    pwd: "password",
    roles: [ { role: "root", db: "admin" } ]
});
```
## Test
```bash
docker exec -it mongo1 mongosh --eval "rs.status()"
```
## Compass
```bash
mongodb://<username>:<password>@<host1>:<port1>,<host2>:<port2>,<host3>:<port3>/?replicaSet=<replicaSetName>&authSource=admin
mongodb://username:password@localhost:27031,localhost:27032,localhost:27033/?replicaSet=dbrs&authSource=admin
mongodb://username:password@172.17.0.1:27031,172.17.0.1:27032,172.17.0.1:27034/?replicaSet=dbrs&authSource=admin
mongodb://username:password@ip-server:27031,ip-server:27032,ip-server:27033/?replicaSet=dbrs&authSource=admin
```
# MongoDB Replica Set Configuration

This document explains how to configure and initialize a **MongoDB Replica Set** using a script and provides an overview of its functionality.

---

## **What is a Replica Set?**
A Replica Set in MongoDB is a group of servers that maintain the same data, ensuring:
- **High availability**: If the primary server fails, a secondary takes over.
- **Data redundancy**: All members sync their data to prevent data loss.
- **Read scalability**: Secondary members can handle read operations.

---
`_id`: Name of the Replica Set (`dbrs` in this case). \
`version`: Version of the configuration. \
`members`: List of nodes in the Replica Set: \
`_id`: Unique ID for the node. \
`host`: Address and port of the MongoDB instance. \
`priority`: Determines which node is more likely to become the primary. \
`rs.initiate(config)`: Initializes the Replica Set with the provided configuration. \
`force: true`: Overrides the configuration if the Replica Set was previously initialized. \
`rs.status();`
- This command provides information about:
- Members' roles (Primary, Secondary, Arbiter).
- Synchronization status and potential errors.
- Connection health.
# Roles of Members
- Primary: Handles write operations and replicates data to secondaries.
- Secondary: Maintains a copy of the primary's data and can process read requests.
- Priority: Higher priority nodes are more likely to become the primary.
# Benefits of Using a Replica Set
1. Automatic failover: Secondary becomes primary if the primary fails.
2. Data redundancy: Prevents data loss through replication.
3. Read scalability: Distribute read requests to secondaries.
# How to Use
1. Define the configuration for your Replica Set.
2. Execute the script on one of the MongoDB nodes.
3. Check the status to confirm proper setup.
4. Use `priority` values to control which nodes are more likely to act as the primary.
