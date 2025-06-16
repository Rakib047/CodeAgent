import streamlit as st
from src.utils.github_utils import get_repo_files, download_file
from src.utils.token_utils import estimate_tokens
from src.llm.groq_client import get_groq_client
from src.llm.analyzer import analyze_large_code
from src.llm.refactorer import refactor_code_with_groq

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Session state flags
if "show_python_input" not in st.session_state:
    st.session_state.show_python_input = False
if "ready_to_refactor" not in st.session_state:
    st.session_state.ready_to_refactor = False

st.set_page_config(page_title="CodeAgent", layout="wide")
st.title("🧠 CodeAgent: Code Analyzer and Refactorer")

url = st.text_input("🔗 GitHub Repository URL")
if url:
    owner, repo = url.split("/")[-2:]
    branch = st.text_input("🌿 Branch (default: main)", "main")

    try:
        files = get_repo_files(owner, repo, branch)
        file = st.selectbox("📄 Choose File to Analyze/Refactor", files)
        content = download_file(owner, repo, file, branch)
        st.code(content, language='python')
        client = get_groq_client()

        col1, col2 = st.columns(2)

        with col1:
            if st.button("🔍 Analyze Code"):
                analysis = analyze_large_code(client, content, st)
                st.markdown(analysis)

        with col2:
            if st.button("🔧 Refactor Code"):
                st.session_state.show_python_input = True

        if st.session_state.show_python_input:
            python_version = st.text_input("🐍 Enter Target Python Version (e.g., python3.10)", key="version_input")

            if st.button("✅ Start Refactoring"):
                refactor = refactor_code_with_groq(client, content, python_version=python_version)
                st.code(refactor, language='python')
                st.session_state.show_python_input = False  # Reset after completion

    except Exception as e:
        st.error(f"❌ Error: {e}")
