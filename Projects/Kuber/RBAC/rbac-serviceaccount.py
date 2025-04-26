import subprocess
import yaml
import os

# ---------[ Load kubeconfig and extract cluster information ]---------
KUBECONFIG_PATH = os.path.expanduser('~/.kube/config')

with open(KUBECONFIG_PATH, 'r') as f:
    kubeconfig = yaml.safe_load(f)

current_context = kubeconfig['current-context']
context = next(ctx for ctx in kubeconfig['contexts'] if ctx['name'] == current_context)
cluster_name = context['context']['cluster']

cluster_info = next(cl for cl in kubeconfig['clusters'] if cl['name'] == cluster_name)
server = cluster_info['cluster']['server']

# ---------[ Get username and namespace from user input ]---------
username = input('Enter the service account name: ').strip()
namespace = input('Enter the namespace: ').strip()

# ---------[ Create a directory for the user ]---------
user_dir = os.path.join(os.getcwd(), username)
os.makedirs(user_dir, exist_ok=True)

# ---------[ Create ServiceAccount YAML ]---------
sa_yaml = {
    'apiVersion': 'v1',
    'kind': 'ServiceAccount',
    'metadata': {
        'name': username,
        'namespace': namespace
    }
}

sa_file = os.path.join(user_dir, f'{username}-sa.yaml')
with open(sa_file, 'w') as f:
    yaml.dump(sa_yaml, f)

subprocess.run(['kubectl', 'apply', '-f', sa_file], check=True)

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
            'kind': 'ServiceAccount',
            'name': username,
            'namespace': namespace
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

print(f"\n✅ ServiceAccount '{username}' and associated Role/RoleBinding have been created successfully!")
print(f"📂 Files are saved inside the folder: {user_dir}")
