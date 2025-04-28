# [Creating Highly Available Clusters with kubeadm](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/high-availability/)

## Initialize the Primary Control-Plane Node
* Important: Before you initialize cluster, you must config haproxy first.
```bash
kubeadm init   --control-plane-endpoint "<LOADBALANCER-IP>:6443"   --upload-certs   --apiserver-advertise-address "<MASTER1-IP>"   --apiserver-cert-extra-sans "<LOADBALANCER-IP>"   --pod-network-cidr "10.244.0.0/16"   --service-cidr "10.96.0.0/12"
```
```bash
kubeadm init --control-plane-endpoint "apisrv.example.ir:6443" --pod-network-cidr=10.244.0.0/16 --upload-certs
```

## Arguments Explained
| Argument | Description |
|:---|:---|
| `--control-plane-endpoint` | Virtual IP or DNS name of HAProxy load balancer. |
| `--upload-certs` | Uploads certificates for sharing with other control-plane nodes. |
| `--apiserver-advertise-address` | The IP address that the API Server advertises. |
| `--apiserver-cert-extra-sans` | Extra SANs (like LoadBalancer IP) for the API server certificate. |
| `--pod-network-cidr` | Pod network CIDR. Example: Flannel uses `10.244.0.0/16`. |
| `--service-cidr` | Service network CIDR. Default is `10.96.0.0/12`. |

---

## Add FQDN to /etc/hosts
We need to add the FQDN address in `/etc/hosts`:
```bash
nano /etc/hosts
```
```text
<HaProxyIPAddress> apisrv.example.ir  
```
Now we added our FQDN with haproxy IP address. In order for the traffic to be directed to haproxy and then from haproxy to the backend servers(k8s-master).

## **Note:** If you forget `--upload-certs`, you can manually upload later:
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

## Install CNI Plugin
Install a CNI for networking, e.g., Flannel:
```bash
kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml
```

---

## Join Additional Nodes
Use the `kubeadm join` commands generated after `init`.  
If needed, regenerate with:
```bash
kubeadm token create --print-join-command
```

---

# HAProxy

## Why High Availability (HA)?
Control-plane nodes manage cluster state.  
Without HA, a control-plane node failure would cause a full outage.  
HA distributes API server traffic across multiple nodes, ensuring resiliency.

## HAProxy Load Balancer Configuration
Example `/etc/haproxy/haproxy.cfg`:
```bash
global
    log /dev/log    local0
    maxconn 2048

defaults
    log     global
    mode    tcp
    option  tcplog
    timeout connect 10s
    timeout client 1m
    timeout server 1m

frontend kubernetes
    bind *:6443
    default_backend kubernetes-backend

backend kubernetes-backend
    balance roundrobin
    server master1 <MASTER1-IP>:6443 check
    server master2 <MASTER2-IP>:6443 check
    server master3 <MASTER3-IP>:6443 check
```

1. Installation 
```bash
apt install haproxy
```

2. haproxy config
```bash
nano /etc/haproxy/haproxy.cfg
```
```conf
#frontend
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

---

## References
- [Kubernetes HA Cluster Official Guide](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/high-availability/)
- [HAProxy Documentation](https://www.haproxy.org/)
