# with local volume
```yml
version: "3.3"
services:
  mysql:
    container_name: mysql
    image: mysql:5.7
    environment:
      MYSQL_ROOT_PASSWORD: password
    ports:
      - 8889:3306
    volumes:
      - ./mysql_data:/var/lib/mysql
    restart: unless-stopped
    networks:
      - network-name

networks:
  network-name:
    external: true
```
# Docker volume
```yml
version: "3.3"
services:
  mysql:
    container_name: mysql
    image: mysql:5.7
    environment:
      MYSQL_ROOT_PASSWORD: password
    ports:
      - 8889:3306
    volumes:
      - mysql_data:/var/lib/mysql
    restart: unless-stopped
    networks:
      - network-name

networks:
  network-name:
    external: true

volumes:
  mysql_data:
```
```bash
# network must be exist
docker network create network-name
```
