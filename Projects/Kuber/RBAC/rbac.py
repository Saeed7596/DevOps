import subprocess
import yaml
import os
import base64

# ---------[ Default CA paths used by kubeadm ]---------
CA_CERT_PATH = '/etc/kubernetes/pki/ca.crt'
CA_KEY_PATH = '/etc/kubernetes/pki/ca.key'

# ---------[ Load kubeconfig and extract cluster information ]---------
KUBECONFIG_PATH = os.path.expanduser('~/.kube/config')

with open(KUBECONFIG_PATH, 'r') as f:
    kubeconfig = yaml.safe_load(f)

current_context = kubeconfig['current-context']
context = next(ctx for ctx in kubeconfig['contexts'] if ctx['name'] == current_context)
cluster_name = context['context']['cluster']

cluster_info = next(cl for cl in kubeconfig['clusters'] if cl['name'] == cluster_name)
server = cluster_info['cluster']['server']

with open(CA_CERT_PATH, 'rb') as f:
    ca_cert_data = base64.b64encode(f.read()).decode('utf-8')

# ---------[ Get username and namespace from user input ]---------
username = input('Enter the username: ').strip()
namespace = input('Enter the namespace: ').strip()

# ---------[ Create a directory for the user ]---------
user_dir = os.path.join(os.getcwd(), username)
os.makedirs(user_dir, exist_ok=True)

# ---------[ Generate user's private key and CSR ]---------
key_file = os.path.join(user_dir, f'{username}-key.pem')
csr_file = os.path.join(user_dir, f'{username}.csr')
crt_file = os.path.join(user_dir, f'{username}.crt')

subprocess.run(['openssl', 'genrsa', '-out', key_file, '2048'], check=True)
subprocess.run([
    'openssl', 'req', '-new', '-key', key_file, '-out', csr_file,
    '-subj', f'/CN={username}/O={namespace}'
], check=True)

# ---------[ Sign the CSR with the CA to generate certificate ]---------
subprocess.run([
    'openssl', 'x509', '-req', '-in', csr_file, '-CA', CA_CERT_PATH,
    '-CAkey', CA_KEY_PATH, '-CAcreateserial', '-out', crt_file,
    '-days', '365'
], check=True)

# ---------[ Create Kubernetes Role YAML ]---------
role_yaml = {
    'apiVersion': 'rbac.authorization.k8s.io/v1',
    'kind': 'Role',
    'metadata': {
        'namespace': namespace,
        'name': f'{username}-role'
    },
    'rules': [
        {
            'apiGroups': [''],
            'resources': ['pods', 'services', 'configmaps'],
            'verbs': ['get', 'watch', 'list', 'create', 'update', 'delete']
        }
    ]
}

role_file = os.path.join(user_dir, f'{username}-role.yaml')
with open(role_file, 'w') as f:
    yaml.dump(role_yaml, f)

subprocess.run(['kubectl', 'apply', '-f', role_file], check=True)

# ---------[ Create Kubernetes RoleBinding YAML ]---------
role_binding_yaml = {
    'apiVersion': 'rbac.authorization.k8s.io/v1',
    'kind': 'RoleBinding',
    'metadata': {
        'name': f'{username}-rolebinding',
        'namespace': namespace
    },
    'subjects': [
        {
            'kind': 'User',
            'name': username,
            'apiGroup': 'rbac.authorization.k8s.io'
        }
    ],
    'roleRef': {
        'kind': 'Role',
        'name': f'{username}-role',
        'apiGroup': 'rbac.authorization.k8s.io'
    }
}

rolebinding_file = os.path.join(user_dir, f'{username}-rolebinding.yaml')
with open(rolebinding_file, 'w') as f:
    yaml.dump(role_binding_yaml, f)

subprocess.run(['kubectl', 'apply', '-f', rolebinding_file], check=True)

# ---------[ Create a dedicated kubeconfig file for the user ]---------
user_kubeconfig = {
    'apiVersion': 'v1',
    'kind': 'Config',
    'clusters': [
        {
            'cluster': {
                'certificate-authority-data': ca_cert_data,
                'server': server
            },
            'name': cluster_name
        }
    ],
    'contexts': [
        {
            'context': {
                'cluster': cluster_name,
                'user': username,
                'namespace': namespace
            },
            'name': f'{username}@{cluster_name}'
        }
    ],
    'current-context': f'{username}@{cluster_name}',
    'users': [
        {
            'name': username,
            'user': {
                'client-certificate-data': base64.b64encode(open(crt_file, 'rb').read()).decode('utf-8'),
                'client-key-data': base64.b64encode(open(key_file, 'rb').read()).decode('utf-8')
            }
        }
    ]
}

kubeconfig_file = os.path.join(user_dir, f'{username}-kubeconfig.yaml')
with open(kubeconfig_file, 'w') as f:
    yaml.dump(user_kubeconfig, f)

print(f"\n✅ All resources for '{username}' have been created successfully!")
print(f"📂 Files are saved inside the folder: {user_dir}")
print(f"🔑 User kubeconfig: {kubeconfig_file}")
