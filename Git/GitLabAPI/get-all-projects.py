# pip install python-gitlab
import gitlab

# Replace with your GitLab instance URL if it's self-hosted, otherwise use the default
GITLAB_URL = "https://gitlab.com"
# Replace with your GitLab personal access token
PRIVATE_TOKEN = "your_access_token_here"

# Connect to GitLab
gl = gitlab.Gitlab(GITLAB_URL, private_token=PRIVATE_TOKEN)

# Get List of all projects
projects = gl.projects.list(all=True, as_list=True, iterator=True)

# Print
for project in projects:
    print(f"{project.id}: {project.name}")
