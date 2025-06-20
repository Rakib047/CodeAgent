import re
from src.utils.github_utils import get_repo_files, download_file
import streamlit as st

def extract_python_packages(code):
    # Regular expression to extract import statements
    imports = re.findall(r'^\s*(?:import|from)\s+([a-zA-Z0-9_]+)', code, re.MULTILINE)
    return sorted(set(imports))  # Return unique packages sorted alphabetically

def get_requirements_from_python_files(owner, repo, branch="main"):
    files = get_repo_files(owner, repo, branch)
    python_files = [file for file in files if file.endswith('.py')]

    all_imports = set()
    for py_file in python_files:
        try:
            code = download_file(owner, repo, py_file, branch)
            all_imports.update(extract_python_packages(code))
        except Exception as e:
            st.error(f"Failed to process {py_file}: {e}")

    return sorted(all_imports)