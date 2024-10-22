```bash
#!/bin/bash

CONTAINER_NAME="gitlab-web-1"   # container name
BACKUP_DIR="/path/to/backup/dir"
BACKUP_FILE=$(docker exec $CONTAINER_NAME ls /var/opt/gitlab/backups | grep ".tar" | sort -V | tail -n 1) # newest backup file

docker exec $CONTAINER_NAME gitlab-backup create

if [ -n "$BACKUP_FILE" ]; then
    echo "Copying backup file: $BACKUP_FILE"
    docker cp "$CONTAINER_NAME:/var/opt/gitlab/backups/$BACKUP_FILE" "$BACKUP_DIR/"
    echo "Backup copied to $BACKUP_DIR/"
else
    echo "No backup file found!"
fi

```
```bash
chmod +x gitlab-backup.sh
./gitlab-backup.sh
```
