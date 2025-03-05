# Worker Node Failure
```bash
kubectl get nodes
kubectl describe node <node-name>

# Check the possible CPU, memory and disk space on the nodes.
top
htop
df -h

# Check container run time
systemctl status containerd

# Check kubelet
service kubelet status
service kubelet start
service kubelet restart
#or
systemctl status kubelet
systemctl start kubelet
systemctl daemon-reload
systemctl restart kubelet

journalctl -u kubelet -f

nano /var/lib/kubelet/config.yaml
nano /etc/kubernetes/kubelet.conf

# Check the Kubelet Certificates
openssl x509 -in /var/lib/kubelet/worker-1.crt -text
```

```bash
# Check kube-proxy
service kube-proxy status
sudo journalctl -u kube-proxy
```
