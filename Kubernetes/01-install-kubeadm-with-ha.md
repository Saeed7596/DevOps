# [Creating Highly Available Clusters with kubeadm](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/high-availability/)

## Initialize Cluster
* Important: Before you initialize cluster, you must config haproxy first.
```bash
kubeadm init --control-plane-endpoint "apisrv.example.ir:6443" --pod-network-cidr=10.244.0.0/16 --upload-certs
```

## Add FQDN to /etc/hosts
We need to add the FQDN address in `/etc/hosts`:
```bash
nano /etc/hosts
```
```text
<HaProxyIPAddress> apisrv.example.ir  
```
Now we added our FQDN with haproxy IP address. In order for the traffic to be directed to haproxy and then from haproxy to the backend servers(k8s-master).

## What happens if you forget to use `--upload-certs`?
1. Run this command:
```bash
sudo kubeadm init phase upload-certs --upload-certs
```
2. Output:
```text
Certificate key: 1234567890abcdef1234567890abcdef
```
3. When adding new control planes, you add this to the kubeadm join command:
```bash
kubeadm join <control-plane-endpoint> --token <token> \
    --discovery-token-ca-cert-hash sha256:<hash> \
    --control-plane --certificate-key <your-certificate-key>

```

---

# HAProxy
1. Installation 
```bash
apt install haproxy
```

2. haproxy config
```bash
nano /etc/haproxy/haproxy.cfg
```
```conf
#forntend
frontend k8s-api
  bind *:6443
  mode tcp
  option tcplog
  default_backend k8s-api

#backend
backend k8s-api
  mode tcp
  option tcplog
  option tcp-check
  balance roundrobin
  default-server inter 10s downinter 5s rise 2 fall 2 slowstart 60s maxconn 250 maxqueue 256 weight 100
  server k8s-api-1 192.168.168.51:6443 check

# Monitoring HAProxy
frontend stats
  bind *:8404
  stats enable
  stats uri /stats
  stats refresh 10
```
