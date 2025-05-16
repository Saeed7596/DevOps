import gitlab

gl = gitlab.Gitlab('https://gitlab.com', private_token='YOUR_ACCESS_TOKEN')

# Replace with your GitLab project ID
PROJECT_ID = 12345678
project = gl.projects.get(PROJECT_ID)

# Read public SSH key from file
key_title = "Deploy Key"
key_value = open("id_rsa.pub").read()

# Add SSH key to the project
project.keys.create({
    'title': key_title,
    'key': key_value,
    'can_push': False
})
print("Deploy key added.")
