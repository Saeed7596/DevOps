```yml
version: '3.8'

services:
  nexus:
    image: sonatype/nexus3:3.57.0
    container_name: nexus
    environment:
      - SONATYPE_DIR=/opt/sonatype
      - NEXUS_HOME=/opt/sonatype/nexus
      - NEXUS_DATA=/nexus-data
      - SONATYPE_WORK=/opt/sonatype/sonatype-work
      - INSTALL4J_ADD_VM_PARAMS=-Xms2703m -Xmx2703m -XX:MaxDirectMemorySize=2703m
    volumes:
      - ./nexus-data:/nexus-data
    ports:
      - "8081:8081"
      - "8083:8083"
      - "8084:8084"
      - "8483:8483"
    restart: always
    command: ["/opt/sonatype/nexus/bin/nexus", "run"]

volumes:
  nexus-data:
```

Find the admin password with:
```bash
docker exec -it nexus cat /nexus-data/admin.password
```
