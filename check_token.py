import requests

token = "YOUR_GITHUB_TOKEN_HERE"
headers = {"Authorization": f"token {token}"}

resp = requests.get("https://api.github.com/user", headers=headers)
print(f"Status: {resp.status_code}")
print(f"User: {resp.json().get('login', 'Unknown')}")
print(f"Scopes: {resp.headers.get('X-OAuth-Scopes', 'None')}")

# Try to list repos to see if we can read
repos = requests.get("https://api.github.com/user/repos", headers=headers)
print(f"Can list repos? {repos.status_code}")
if repos.status_code == 200:
    print(f"First 3 repos: {[r['name'] for r in repos.json()[:3]]}")
