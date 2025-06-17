import requests

def get_repo_files(owner, repo, branch="main"):
    url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/{branch}?recursive=1"
    res = requests.get(url)
    if res.status_code == 200:
        return [item["path"] for item in res.json()["tree"] if item["type"] == "blob"]
    raise Exception(f"GitHub API Error: {res.status_code}")

def download_file(owner, repo, file_path, branch="main"):
    raw_url = f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{file_path}"
    res = requests.get(raw_url)
    if res.status_code == 200:
        return res.text
    raise Exception(f"Failed to download {file_path}: {res.status_code}")
