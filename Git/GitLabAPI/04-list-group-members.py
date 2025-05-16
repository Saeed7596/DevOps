import gitlab

gl = gitlab.Gitlab('https://gitlab.com', private_token='YOUR_ACCESS_TOKEN')

# Replace with your GitLab group ID
GROUP_ID = 123456
group = gl.groups.get(GROUP_ID)

# List members of a group
for member in group.members.list():
    print(f"{member.name} ({member.username}) - {member.access_level}")
