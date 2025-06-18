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


import base64
import streamlit as st

def commit_file(owner, repo, file_path, content, message, branch="main"):
    token = st.secrets["GITHUB_TOKEN"]
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{file_path}"
    headers = {"Authorization": f"token {token}"}
    # Get the SHA if the file exists (for update)
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