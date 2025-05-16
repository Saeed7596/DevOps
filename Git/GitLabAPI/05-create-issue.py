import gitlab

gl = gitlab.Gitlab('https://gitlab.com', private_token='YOUR_ACCESS_TOKEN')

# Replace with your GitLab project ID
PROJECT_ID = 12345678
project = gl.projects.get(PROJECT_ID)

# Create a new issue in the project
issue = project.issues.create({
    'title': 'Example issue from API',
    'description': 'This issue was created using python-gitlab'
})
print(f"Issue #{issue.iid} created.")
