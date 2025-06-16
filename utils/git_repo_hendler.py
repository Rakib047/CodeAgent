import requests
import streamlit as st
# ---------- Functions ----------
@st.cache_data(show_spinner=False)
def get_repo_files(owner: str, repo: str, branch: str = "main"):
    url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/{branch}?recursive=1"
    res = requests.get(url)
    if res.status_code == 200:
        tree = res.json().get("tree", [])
        files = [f["path"] for f in tree if f["type"] == "blob"]
        return files
    else:
        st.error(f"Failed to fetch file list: {res.status_code}")
        return []

@st.cache_data(show_spinner=False)
def download_file(owner: str, repo: str, path: str, branch: str = "main"):
    raw_url = f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{path}"
    res = requests.get(raw_url)
    if res.status_code == 200:
        return res.text
    else:
        return f"Error loading file: {res.status_code}"