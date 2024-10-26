```yml
version: '3.8'

services:
  redis-stack:
    image: redis/redis-stack:latest
    container_name: redis-stack
    ports:
      - "6379:6379"
    volumes:
      - ./data:/data
    environment:
      - REDIS_PASSWORD=<PASSWORD>
    restart: unless-stopped
    command: >
      sh -c 'exec redis-server
      --requirepass "$${REDIS_PASSWORD}"
      --save 20 1
      --loglevel warning
      --protected-mode no
      --loadmodule /opt/redis-stack/lib/redisearch.so
      --loadmodule /opt/redis-stack/lib/rejson.so'
```
```bash
#docker engin
docker run -it --name redis-stack -d -p 6379:6379 --restart unless-stopped -v /path/data:/data -e REDIS_PASSWORD=<PASSWORD> redis/redis-stack:latest sh -c 'exec redis-server --requirepass "$REDIS_PASSWORD" --save 20 1 --loglevel warning --protected-mode no --loadmodule /opt/redis-stack/lib/redisearch.so --loadmodule /opt/redis-stack/lib/rejson.so'
```
