# Create User in OpenShift on helper VM!
```py
import subprocess
import yaml
import os
import base64
import time

# ---------[ Load kubeconfig and extract cluster info ]---------
KUBECONFIG_PATH = os.path.expanduser('~/.kube/config')

with open(KUBECONFIG_PATH, 'r') as f:
    kubeconfig = yaml.safe_load(f)

current_context = kubeconfig['current-context']
context = next(ctx for ctx in kubeconfig['contexts'] if ctx['name'] == current_context)
cluster_name = context['context']['cluster']

cluster_info = next(cl for cl in kubeconfig['clusters'] if cl['name'] == cluster_name)
server = cluster_info['cluster']['server']
ca_cert_data = cluster_info['cluster']['certificate-authority-data']

# ---------[ Get user inputs ]---------
username = input('Enter the username: ').strip()
namespace = input('Enter the namespace: ').strip()

user_dir = os.path.join(os.getcwd(), username)
os.makedirs(user_dir, exist_ok=True)

key_file = os.path.join(user_dir, f'{username}-key.pem')
csr_file = os.path.join(user_dir, f'{username}.csr')
crt_file = os.path.join(user_dir, f'{username}.crt')

# ---------[ Generate private key and CSR ]---------
subprocess.run(['openssl', 'genrsa', '-out', key_file, '2048'], check=True)
subprocess.run([
    'openssl', 'req', '-new', '-key', key_file, '-out', csr_file,
    '-subj', f'/CN={username}/O={namespace}'
], check=True)

# ---------[ Create and apply CSR YAML ]---------
with open(csr_file, 'rb') as f:
    csr_base64 = base64.b64encode(f.read()).decode('utf-8')

csr_name = f'{username}-csr'
csr_yaml = {
    'apiVersion': 'certificates.k8s.io/v1',
    'kind': 'CertificateSigningRequest',
    'metadata': {'name': csr_name},
    'spec': {
        'request': csr_base64,
        'signerName': 'kubernetes.io/kube-apiserver-client',
        'usages': ['client auth'],
        'groups': ['system:authenticated']
    }
}

csr_path = os.path.join(user_dir, f'{csr_name}.yaml')
with open(csr_path, 'w') as f:
    yaml.dump(csr_yaml, f)

subprocess.run(['kubectl', 'apply', '-f', csr_path], check=True)
subprocess.run(['kubectl', 'certificate', 'approve', csr_name], check=True)

# ---------[ Retrieve signed certificate ]---------
for _ in range(10):
    cert_output = subprocess.run(
        ['kubectl', 'get', 'csr', csr_name, '-o', 'jsonpath={.status.certificate}'],
        stdout=subprocess.PIPE, check=True
    )
    cert_data_b64 = cert_output.stdout.decode('utf-8')
    if cert_data_b64:
        with open(crt_file, 'wb') as f:
            f.write(base64.b64decode(cert_data_b64))
        break
    time.sleep(1)
else:
    raise RuntimeError('❌ Timed out waiting for certificate approval.')

# ---------[ Create Role and RoleBinding ]---------
role_file = os.path.join(user_dir, f'{username}-role.yaml')
role_binding_file = os.path.join(user_dir, f'{username}-rolebinding.yaml')

role_yaml = {
    'apiVersion': 'rbac.authorization.k8s.io/v1',
    'kind': 'Role',
    'metadata': {'namespace': namespace, 'name': f'{username}-role'},
    'rules': [{
        'apiGroups': [''],
        'resources': ['pods', 'services', 'configmaps'],
        'verbs': ['get', 'watch', 'list', 'create', 'update', 'delete']
    }]
}

role_binding_yaml = {
    'apiVersion': 'rbac.authorization.k8s.io/v1',
    'kind': 'RoleBinding',
    'metadata': {'name': f'{username}-rolebinding', 'namespace': namespace},
    'subjects': [{
        'kind': 'User',
        'name': username,
        'apiGroup': 'rbac.authorization.k8s.io'
    }],
    'roleRef': {
        'kind': 'Role',
        'name': f'{username}-role',
        'apiGroup': 'rbac.authorization.k8s.io'
    }
}

with open(role_file, 'w') as f:
    yaml.dump(role_yaml, f)
with open(role_binding_file, 'w') as f:
    yaml.dump(role_binding_yaml, f)

subprocess.run(['kubectl', 'apply', '-f', role_file], check=True)
subprocess.run(['kubectl', 'apply', '-f', role_binding_file], check=True)

# ---------[ Create user kubeconfig ]---------
user_kubeconfig = {
    'apiVersion': 'v1',
    'kind': 'Config',
    'clusters': [{
        'name': cluster_name,
        'cluster': {
            'server': server,
            'certificate-authority-data': ca_cert_data
        }
    }],
    'contexts': [{
        'name': f'{username}@{cluster_name}',
        'context': {
            'cluster': cluster_name,
            'user': username,
            'namespace': namespace
        }
    }],
    'current-context': f'{username}@{cluster_name}',
    'users': [{
        'name': username,
        'user': {
            'client-certificate-data': base64.b64encode(open(crt_file, 'rb').read()).decode('utf-8'),
            'client-key-data': base64.b64encode(open(key_file, 'rb').read()).decode('utf-8')
        }
    }]
}

kubeconfig_file = os.path.join(user_dir, f'{username}-kubeconfig.yaml')
with open(kubeconfig_file, 'w') as f:
    yaml.dump(user_kubeconfig, f)

print(f"\n✅ User '{username}' created and kubeconfig generated!")
print(f"📁 Files are in: {user_dir}")
print(f"🔑 Kubeconfig: {kubeconfig_file}")
```

---

# Test user
```bash
KUBECONFIG=/path/to/username/username-kubeconfig.yaml kubectl get pods
```
