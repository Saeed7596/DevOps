# Deploy Stage
### Without Downtime:
```bash
docker compose --verbose -f ${CONTAINER_NAME}.compose up --pull "always" -d &&
docker images -a | grep "${NEXUS_ADDR}/${SERVICE_NAME}-${PRODUCT_NAME}-${ENVIRON}.*none" | awk '{ print $3; }' | xargs docker rmi || true
```
### If not work use this:
```bash
docker compose --verbose -f ${CONTAINER_NAME}.compose down || true &&
docker rmi "${NEXUS_ADDR}/${SERVICE_NAME}-${PRODUCT_NAME}-${ENVIRON}:${APP_VERSION}" || true &&
docker compose --verbose -f ${CONTAINER_NAME}.compose up -d
```

---

# SSH with gitlab-runner
In your destination client:
```bash
cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
```
Copy the `~/.ssh/id_rsa` value and create the vaiable in gitlab.
