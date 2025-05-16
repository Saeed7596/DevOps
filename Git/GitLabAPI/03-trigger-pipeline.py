import gitlab

gl = gitlab.Gitlab('https://gitlab.com', private_token='YOUR_ACCESS_TOKEN')

# Replace with your GitLab project ID
PROJECT_ID = 12345678
project = gl.projects.get(PROJECT_ID)

# Trigger a pipeline on the 'main' branch
pipeline = project.pipelines.create({'ref': 'main'})
print(f"Pipeline {pipeline.id} triggered.")
