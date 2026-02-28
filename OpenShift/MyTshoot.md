# Network Connection Test
```bash
oc debig node/node-name

nc -vz IP PORT
```

```bash
ip route
ip addr
ss -plant
cat /etc/resolv.conf
tcpdump -ni any port 443

# DNS
dig @<cluster-dns-ip> google.com
```

# Certificate
```bash
# without ssl check
curl -k URL

# ssl check
curl -vI URL

openssl s_client -connect host:443 -servername host
```

# Create Ubuntu Image
Dockerfile
```Dockerfile
FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \
    traceroute \
    iputils-ping \
    net-tools \
    dnsutils \
    mtr \
    curl \
    nmap \
    iproute2 \
    tcpdump \
    iputils-tracepath \
    ethtool \
    bind9-host \
    vim \
    && rm -rf /var/lib/apt/lists/*

# Define default command to start bash sheel
CMD ["bash"]
```
```bash
docker built -t my-ubuntu:v22.04
docker save my-ubuntu:v22.04 -o my-ubuntu.tar

# In private registry
docker load -i my-ubuntu.tar
docker tag my-ubuntu:v22.04 my-registry.com/tools/my-ubuntu:v22.04
docker push my-registry.com/tools/my-ubuntu:v22.04
```
Deployment
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: network-tools
  namespace: test
spec:
  replicas: 1
  selector:
    matchLabels:
      app: network-tools
    template:
      metadata:
        labels:
          app: network-tools
      spec:
        affinity:
          nodeAffinity:
            requiredDuringSchedulingIgnoredDuringExecution:
              nodeSelectorTerms:
              - matchExpressions:
                - key: node-role.kubernetes.io/team-a
                  operator: Exists
        containers:
          - name: ubuntu-network-tools
            image: my-registry.com/tools/my-ubuntu:v22.04
            command: ["sleep", "3600"]
```

---

# nicolaka/netshoot
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: netshoot
  namespace: test
spec:
  replicas: 1
  selector:
    matchLabels:
      app: netshoot
  template:
    metadata:
      labels:
        app: netshoot
    spec:
      nodeSelector:
        node-role.kubernetes.io/team-a: ""
      containers:
      - name: netshoot
        image: nicolaka/netshoot:latest
        imagePullPolicy: IfNotPresent
        command: ["sleep", "infinity"]
        stdin: true
        tty: true
        resources:
          requests:
            cpu: 50m
            memory: 64Mi
          limits:
            cpu: 500m
            memory: 512Mi
        securityContext:
          allowPrivilegeEscalation: false
          readOnlyRootFilesystem: true
          capabilities:
            drop:
              - ALL
```