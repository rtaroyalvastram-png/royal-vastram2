import requests
import json

token = "YOUR_GITHUB_TOKEN_HERE"
repo_name = "royal-vastram"
headers = {
    "Authorization": f"token {token}",
    "Accept": "application/vnd.github.v3+json"
}

# 1. Try to get the authenticated user
user_resp = requests.get("https://api.github.com/user", headers=headers)
if user_resp.status_code != 200:
    print(f"Error getting user: {user_resp.status_code} {user_resp.text}")
    exit(1)

user_data = user_resp.json()
username = user_data['login']
print(f"Authenticated as: {username}")

# 2. Create the repository
# We try to create it under the authenticated user
data = {
    "name": repo_name,
    "private": True,
    "description": "Royal Vastram Billing Application"
}

print(f"Creating repository '{repo_name}' for user '{username}'...")
resp = requests.post("https://api.github.com/user/repos", headers=headers, json=data)

if resp.status_code == 201:
    print("Repository created successfully!")
    print(resp.json()['html_url'])
elif resp.status_code == 422:
    print("Repository already exists (or name invalid).")
    # Check if it exists
    repo_url = f"https://api.github.com/repos/{username}/{repo_name}"
    check_resp = requests.get(repo_url, headers=headers)
    if check_resp.status_code == 200:
        print("Confirmed repository exists.")
    else:
        print(f"Could not access existing repository. Error: {resp.text}")
else:
    print(f"Failed to create repository: {resp.status_code} {resp.text}")
