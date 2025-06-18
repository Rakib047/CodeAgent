
import sys
import os

# Dynamically add the root folder (/legacy_repo) to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.abspath(os.path.join(current_dir, ".."))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

import streamlit as st
from src.utils.github_utils import get_repo_files, download_file
from src.utils.token_utils import estimate_tokens
from src.llm.groq_client import get_groq_client
from src.llm.analyzer import analyze_large_code
from src.llm.refactorer import refactor_large_code
from src.llm.test_case_generator import generate_test_cases
from src.llm.doc_generator import generate_documentation
from src.llm.code_diff import generate_full_diff

from src.utils.github_utils import commit_file 



# Set up session state for conditional flow
if "refactor_step" not in st.session_state:
    st.session_state.refactor_step = 0  # 0 = idle, 1 = waiting for input

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

        # Button: Analyze Code
        if st.button("🔍 Analyze Code"):
            st.session_state.analysis_result = analyze_large_code(client, content, st)
        # Show previous analysis if available
        if "analysis_result" in st.session_state:
            st.markdown("### 🔍 Code Analysis")
            st.markdown(st.session_state.analysis_result)

        # Button: Refactor Code
        if st.button("🔧 Refactor Code"):
            st.session_state.refactor_step = 1  # Enable version input

        # Refactor step
        if st.session_state.get("refactor_step") == 1:
            st.session_state.python_version = st.text_input("🐍 Enter Python Version (e.g., python3.10)", key="version_input")
            python_version=st.session_state.python_version
            if st.button("✅ Start Refactoring"):
                if python_version.strip() == "":
                    st.warning("Please enter a Python version.")
                else:
                    st.session_state.refactor_result = refactor_large_code(client, content, st, python_version.strip())
                    st.session_state.refactor_step = 0  # Reset step
        # Show previous refactor result if available
        if "refactor_result" in st.session_state:
            st.markdown("### 🔧 Refactored Code")
            st.code(st.session_state.refactor_result, language="python")

                # --- Add branch input here ---
            commit_branch = st.text_input("Branch to commit to", value=branch, key="commit_branch")
            commit_message = st.text_input("Commit message", "Refactored code via CodeAgent", key="commit_message")

            if st.button("💾 Push Refactored Code to GitHub Repository"):
                try:
                    commit_file(
                        owner,
                        repo,
                        file,
                        st.session_state.refactor_result,
                        commit_message,
                        commit_branch  # Use the user-specified branch
                    )
                    st.success(f"Code committed to GitHub branch '{commit_branch}'!")
                except Exception as e:
                    st.error(f"Failed to commit: {e}")


        
            # Generating Test cases for Refactored code
            if st.button("Generate Test Cases"):
                st.session_state.generated_tese_tases = generate_test_cases(client, st.session_state.refactor_result)
                st.code(st.session_state.generated_tese_tases, language = 'python')

            # Add "Generate Documentation" button after refactoring
            if st.button("📜 Generate Documentation"):
                if st.session_state.refactor_result:
                    # Use the stored python_version from session state
                    python_version = st.session_state.python_version
                    st.session_state.documentation_result = generate_documentation(st.session_state.refactor_result, python_version=python_version, client=client)
                    st.markdown(st.session_state.documentation_result)
                else:
                    st.warning("No refactored code available to generate documentation.")

                # Show Full Code Diff button
            if st.button("📊 Show Full Code Diff"):
                st.session_state.code_diff = generate_full_diff(content, st.session_state.refactor_result)
                st.code(st.session_state.code_diff, language="diff")
            



    except Exception as e:
        st.error(f"❌ Error: {e}")

