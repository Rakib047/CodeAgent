import requests

def get_repo_files(owner, repo, branch="main"):
    url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/{branch}?recursive=1"
    res = requests.get(url)
    if res.status_code == 200:
        return [f["path"] for f in res.json().get("tree", []) if f["type"] == "blob"]
    else:
        raise Exception(f"GitHub error: {res.status_code}")

def download_file(owner, repo, path, branch="main"):
    raw_url = f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{path}"
    res = requests.get(raw_url)
    if res.status_code == 200:
        return res.text
    else:
        raise Exception(f"File load error: {res.status_code}")
