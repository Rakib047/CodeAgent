import requests

def get_github_raw_url(url: str) -> str:
    if "github.com" in url and "raw.githubusercontent.com" not in url:
        url = url.replace("https://github.com/", "https://raw.githubusercontent.com/")
        url = url.replace("/blob/", "/")
    return url

def get_file_content(uploaded_file) -> str:
    if uploaded_file:
        return uploaded_file.read().decode("utf-8")
    return ""

def get_git_file_content(github_url: str) -> str:
    if github_url:
        try:
            raw_url = get_github_raw_url(github_url)
            response = requests.get(raw_url)
            response.raise_for_status()
            return response.text
        except Exception as e:
            return f"ERROR: {e}"
    return ""