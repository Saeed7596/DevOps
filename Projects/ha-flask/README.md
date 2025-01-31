# All nginx and ha should have same network_name
---
#internal error
```
docker exec -it <container_name_or_id> psql -U <db_user> -d <db_name>
```
```
        host="postgres", # postgres service name in docker-compose 
        database="mydatabase",
        user="myuser",
        password="mypassword"
```
```
docker exec -it postgres_db psql -U myuser -d mydatabase
```
```
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);
```

---

# For Test ha:
```
docker logs flask_app
```

---

# Test replica
docker exec -it postgres_db psql -U myuser -d mydatabase
TABLE users;
docker exec -it postgres_replica_1 psql -U myuser -d mydatabase
TABLE users;
