import requests

# GitLab personal access token
ACCESS_TOKEN = 'your_access_token_here'

# Base URL of your GitLab instance (change if self-hosted)
GITLAB_URL = 'https://gitlab.com/api/v4'

# Project ID (can be obtained via API or UI)
PROJECT_ID = 12345678

# Branch details
NEW_BRANCH_NAME = 'new-branch'
REF_BRANCH = 'main'  # The branch to branch from

# Headers for authentication
headers = {
    'PRIVATE-TOKEN': ACCESS_TOKEN
}

# Step 1: Check if the branch already exists
check_url = f"{GITLAB_URL}/projects/{PROJECT_ID}/repository/branches/{NEW_BRANCH_NAME}"
check_response = requests.get(check_url, headers=headers)

if check_response.status_code == 200:
    print(f"Branch '{NEW_BRANCH_NAME}' already exists.")
else:
    # Step 2: Create the branch
    create_url = f"{GITLAB_URL}/projects/{PROJECT_ID}/repository/branches"
    payload = {
        'branch': NEW_BRANCH_NAME,
        'ref': REF_BRANCH
    }

    create_response = requests.post(create_url, headers=headers, data=payload)

    if create_response.status_code == 201:
        print(f"Branch '{NEW_BRANCH_NAME}' created successfully.")
    else:
        print(f"Failed to create branch. Status: {create_response.status_code}, Response: {create_response.text}")
