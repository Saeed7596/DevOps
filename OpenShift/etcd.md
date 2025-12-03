# [etcd backup](https://docs.redhat.com/en/documentation/openshift_container_platform/4.17/html/backup_and_restore/control-plane-backup-and-restore)

* **Tip**
You can check whether the proxy is enabled by reviewing the output of `oc get proxy cluster -o yaml`. The proxy is enabled if the `httpProxy`, `httpsProxy`, and `noProxy` fields have values set.

0. Get etcd Pods
    ```bash
    oc get pods -n openshift-etcd -l app=etcd
    ```


1. Start a debug session as root for a control plane node:
    ```bash
    oc debug --as-root node/<node_name>
    ```

2. Change your root directory to `/host` in the debug shell:
    ```bash
    chroot /host
    ```
3. If the cluster-wide proxy is enabled, export the `NO_PROXY`, `HTTP_PROXY`, and `HTTPS_PROXY` environment variables by running the following commands:
    ```bash
    export HTTP_PROXY=http://<your_proxy.example.com>:8080

    export HTTPS_PROXY=https://<your_proxy.example.com>:8080

    export NO_PROXY=<example.com>
    ```
4. Run the `cluster-backup.sh` script in the debug shell and pass in the location to save the backup to.
    * **Tip**: The `cluster-backup.sh` script is maintained as a component of the etcd Cluster Operator and is a wrapper around the `etcdctl snapshot save` command.
    ```bash
    /usr/local/bin/cluster-backup.sh /home/core/assets/backup
    ```
    Output:
   ```text
   snapshot db and kube resources are successfully saved to /home/core/assets/backup
   ```
In this example, two files are created in the `/home/core/assets/backup/` directory on the control plane host:

* `snapshot_<datetimestamp>.db`: This file is the etcd snapshot. The `cluster-backup.sh` script confirms its validity.
* `static_kuberesources_<datetimestamp>.tar.gz`: This file contains the resources for the static pods. If etcd encryption is enabled, it also contains the encryption keys for the etcd snapshot.

**Note**:

If etcd encryption is enabled, it is recommended to store this second file separately from the etcd snapshot for security reasons. However, this file is required to restore from the etcd snapshot.

Keep in mind that etcd encryption only encrypts values, not keys. This means that resource types, namespaces, and object names are unencrypted.

---

### Move backup files
1. In oc debug mode:
### Move backup files
1. In oc debug mode:
```bash
mkdir -p /tmp/etcd-backup
cp /home/core/assets/backup/snapshot_<datetimestamp>.db /tmp/etcd-backup/
cp /home/core/assets/backup/static_kuberesources_<datetimestamp> /tmp/etcd-backup/

chmod 644 /tmp/snapshot_<datetimestamp>.db
chmod 644 /tmp/static_kuberesources_<datetimestamp>.tar.gz
```
2. In your host:
```bash
sudo scp -i id_rsa -r core@<node-ip>:/tmp/etcd-backup .
```

---
