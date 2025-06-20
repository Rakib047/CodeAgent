import requests
import base64
import streamlit as st

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


def branch_exists(owner, repo, branch):
    token = st.secrets["GITHUB_TOKEN"]
    url = f"https://api.github.com/repos/{owner}/{repo}/branches/{branch}"
    headers = {"Authorization": f"token {token}"}
    res = requests.get(url, headers=headers)
    return res.status_code == 200

def create_branch(owner, repo, new_branch, from_branch="main"):
    token = st.secrets["GITHUB_TOKEN"]
    headers = {"Authorization": f"token {token}"}
    # Get the latest commit SHA of the from_branch
    url = f"https://api.github.com/repos/{owner}/{repo}/git/ref/heads/{from_branch}"
    res = requests.get(url, headers=headers)
    if res.status_code != 200:
        raise Exception(f"Failed to get base branch '{from_branch}': {res.status_code} {res.text}")
    sha = res.json()["object"]["sha"]
    # Create new branch ref
    url = f"https://api.github.com/repos/{owner}/{repo}/git/refs"
    data = {
        "ref": f"refs/heads/{new_branch}",
        "sha": sha
    }
    res = requests.post(url, headers=headers, json=data)
    if res.status_code == 201:
        return True
    elif res.status_code == 422 and "Reference already exists" in res.text:
        # Branch already exists, treat as success
        return True
    else:
        raise Exception(f"Failed to create branch '{new_branch}': {res.status_code} {res.text}")

def commit_file(owner, repo, file_path, content, message, branch="main", base_branch="main"):
    token = st.secrets["GITHUB_TOKEN"]
    headers = {"Authorization": f"token {token}"}
    # Always try to create the branch (safe if it already exists)
    create_branch(owner, repo, branch, from_branch=base_branch)
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{file_path}"
    get_res = requests.get(url + f"?ref={branch}", headers=headers)
    sha = get_res.json().get("sha") if get_res.status_code == 200 else None
    data = {
        "message": message,
        "content": base64.b64encode(content.encode()).decode(),
        "branch": branch
    }
    if sha:
        data["sha"] = sha
    res = requests.put(url, headers=headers, json=data)
    if res.status_code in [200, 201]:
        return res.json()
    raise Exception(f"GitHub commit error: {res.status_code} {res.text}")