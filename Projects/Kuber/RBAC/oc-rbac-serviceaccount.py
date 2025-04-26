import subprocess
import yaml
import os

# ---------[ Load kubeconfig and extract cluster info ]---------
KUBECONFIG_PATH = os.path.expanduser('~/.kube/config')

with open(KUBECONFIG_PATH, 'r') as f:
    kubeconfig = yaml.safe_load(f)

current_context = kubeconfig['current-context']
context = next(ctx for ctx in kubeconfig['contexts'] if ctx['name'] == current_context)
cluster_name = context['context']['cluster']

cluster_info = next(cl for cl in kubeconfig['clusters'] if cl['name'] == cluster_name)
server = cluster_info['cluster']['server']

# ---------[ Get username and namespace from user input ]---------
username = input('Enter the username (and ServiceAccount name): ').strip()
namespace = input('Enter the namespace (project): ').strip()

# ---------[ Create directory for user ]---------
user_dir = os.path.join(os.getcwd(), username)
os.makedirs(user_dir, exist_ok=True)

# ---------[ Create namespace/project if not exists ]---------
print(f"Creating project/namespace '{namespace}' (if not exists)...")
subprocess.run(['oc', 'new-project', namespace], check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# ---------[ Create ServiceAccount ]---------
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
subprocess.run(['oc', 'apply', '-f', sa_file], check=True)

# ---------[ Create Role ]---------
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
subprocess.run(['oc', 'apply', '-f', role_file], check=True)

# ---------[ Create RoleBinding ]---------
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
subprocess.run(['oc', 'apply', '-f', rolebinding_file], check=True)

# ---------[ Get token of ServiceAccount ]---------
print("Retrieving ServiceAccount token...")
token = subprocess.check_output(['oc', 'sa', 'new-token', username, '-n', namespace]).decode('utf-8').strip()

# ---------[ Create kubeconfig using token ]---------
user_kubeconfig = {
    'apiVersion': 'v1',
    'kind': 'Config',
    'clusters': [
        {
            'cluster': {
                'insecure-skip-tls-verify': True,
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
                'token': token
            }
        }
    ]
}

kubeconfig_file = os.path.join(user_dir, f'{username}-kubeconfig.yaml')
with open(kubeconfig_file, 'w') as f:
    yaml.dump(user_kubeconfig, f)

print(f"\n✅ OpenShift resources for '{username}' created successfully!")
print(f"📂 All YAML files and kubeconfig saved in folder: {user_dir}")
print(f"🔑 kubeconfig file: {kubeconfig_file}")
