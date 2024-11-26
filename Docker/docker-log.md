# Managing and Clearing Docker Logs

This document explains how to manage and clear Docker container logs effectively.

---

## 1. **Remove and Restart the Container**  
The simplest way to clear logs is by removing and recreating the container. Be cautious, as this will delete all existing logs.

## 2. Manually Clear Log Files
Docker logs are stored in JSON files, typically at the following location:
```bash
/var/lib/docker/containers/<container_id>/<container_id>-json.log
```
Clear the log file:
```bash
sudo cat /dev/null > /var/lib/docker/containers/<container_id>/<container_id>-json.log
```
## 3. Limit Log Size and Rotation
To prevent excessive log accumulation, configure log limits using `docker-compose.yml` or the `docker run` command. \

Using `docker-compose.yml`:
```yml
services:
  your_service:
    image: your_image
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```
Using `docker run`:
```bash
docker run --log-opt max-size=10m --log-opt max-file=3 <image_name>
```
- `max-size`: Limits the log file size (e.g., 10MB).
- `max-file`: Specifies the number of log files to retain.

## 4. Remove Unused Containers
To free up space, remove stopped containers and their associated logs:
```bash
docker container prune
```
## 5. Additional Tips
```bash
docker logs <container_name>
docker logs -f --tail 50 <container_name>
```
