import gitlab

gl = gitlab.Gitlab('https://gitlab.com', private_token='YOUR_ACCESS_TOKEN')

# Replace with your GitLab project ID
PROJECT_ID = 12345678
project = gl.projects.get(PROJECT_ID)

# Download the repository archive
with open(f'{project.name}.tar.gz', 'wb') as f:
    project.repository_archive(streamed=True, action=f.write)
print(f"Repository for '{project.name}' downloaded.")
