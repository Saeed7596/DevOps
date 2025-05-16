import gitlab

gl = gitlab.Gitlab('https://gitlab.com', private_token='YOUR_ACCESS_TOKEN')

# Replace with your project's ID (get from previous script)
PROJECT_ID = 12345678

project = gl.projects.get(PROJECT_ID)
for pipeline in project.pipelines.list():
    print(f"Pipeline ID: {pipeline.id}, Status: {pipeline.status}")
