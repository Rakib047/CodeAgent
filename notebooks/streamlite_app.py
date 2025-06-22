import sys
import os
import streamlit as st

# Dynamically add the root folder (/legacy_repo) to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.abspath(os.path.join(current_dir, ".."))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from src.utils.github_utils import get_repo_files, download_file
from src.utils.token_utils import estimate_tokens
from src.llm.groq_client import get_groq_client
from src.llm.analyzer import analyze_large_code
from src.llm.refactorer import refactor_large_code
from src.llm.test_case_generator import generate_test_cases
from src.llm.doc_generator import generate_documentation
from src.llm.code_diff import generate_full_diff
from src.llm.refactor_code_optimizer import optimize_refactored_code
from src.utils.github_utils import commit_file
from src.llm.update_dependencies import generate_updated_dependencies
from src.utils.github_utils import create_pull_request
from src.llm.requirements_validation import validate_requirements_and_run_code

# --- Setup ---
st.set_page_config(page_title="CodeAgent", layout="wide")
st.title("CodeAgent: Code Analyzer & Refactorer")

if "refactor_step" not in st.session_state:
    st.session_state.refactor_step = 0

if "regenerate_clicked" not in st.session_state:
    st.session_state.regenerate_clicked = False

# --- GitHub Input ---
st.subheader("Load GitHub File")
url = st.text_input("GitHub Repository URL", placeholder="https://github.com/user/repo")
if url:
    owner, repo = url.split("/")[-2:]
    branch = st.text_input("Branch", value="main")

    try:
        # Track previously selected file
        if 'prev_file' not in st.session_state:
            st.session_state.prev_file = None

        files = get_repo_files(owner, repo, branch)
        file = st.selectbox("Choose File", files)

        # Reset session state when a new file is selected
        if file != st.session_state.prev_file:
            for key in st.session_state.keys():
                del st.session_state[key]
            st.session_state.prev_file = file  # Update with new file selection

        # Re-download and display the code
        content = download_file(owner, repo, file, branch)
        st.code(content, language="python")

        client = get_groq_client()

        st.divider()

        # --- Buttons ---
        
        if st.button("Analyze Code"):
            st.session_state.analysis_result = analyze_large_code(client, content, st)
        # --- Analysis Result ---
        if "analysis_result" in st.session_state:
            with st.expander("Code Analysis", expanded=True):
                st.markdown(st.session_state.analysis_result)

        st.divider()
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Refactor Code"):
                st.session_state.refactor_step = 1
        with col2:
            if st.button("Show Full Code Diff") and "refactor_result" in st.session_state:
                st.session_state.code_diff = generate_full_diff(content, st.session_state.refactor_result)

         
        col1, col2 = st.columns(2)
        with col1:
        # --- Refactoring Input ---
            if "refactor_step" in st.session_state and st.session_state.refactor_step == 1:
                python_version = st.text_input("Python Version (e.g., python3.10)", key="version_input")
                if st.button("Start Refactoring"):
                    if not python_version.strip():
                        st.warning("Please enter a Python version.")
                    else:
                        st.session_state.python_version = python_version.strip()
                        st.session_state.refactor_result = refactor_large_code(client, content, st, python_version.strip())
                        st.session_state.refactor_step = 0
            # --- Refactored Code ---
            if "refactor_result" in st.session_state:
                st.markdown("### 🛠 Refactored Code")
                st.code(st.session_state.refactor_result, language="python")

                # --- Regenerate with Instructions ---
                with st.expander("Modify Refactored Code", expanded=False):
                    if st.button("Re-generate"):
                        st.session_state.regenerate_clicked = True

                    if st.session_state.regenerate_clicked:
                        instruction = st.text_input("📌 Instruction to update code", key="instruction_input")
                        if st.button("Apply Modification"):
                            if instruction.strip():
                                st.session_state.refactor_result = optimize_refactored_code(
                                    client,
                                    st.session_state.refactor_result,
                                    instruction.strip()
                                )
                                st.success("Code regenerated.")
                                st.session_state.regenerate_clicked = False
        with col2:
            if "code_diff" in st.session_state:
                with st.expander("Code Diff", expanded=True):
                    st.code(st.session_state.code_diff, language="diff")

        st.divider()

        # --- Additional Features ---
        if "refactor_result" in st.session_state:
            col1, col2 = st.columns(2)

            with col1:
                if st.button("Generate Test Cases"):
                    st.session_state.generated_test_cases = generate_test_cases(client, st.session_state.refactor_result)
                if "generated_test_cases" in st.session_state:
                    st.code(st.session_state.generated_test_cases, language="python")

            with col2:
                if st.button("Generate Documentation"):
                    if st.session_state.python_version:
                        st.session_state.doc_string = generate_documentation(
                            st.session_state.refactor_result,
                            python_version=st.session_state.python_version,
                            client=client
                        )
                    else:
                        st.warning("Missing Python version.")
                if "doc_string" in st.session_state: 
                    st.markdown(st.session_state.doc_string)
        # --- Add branch input here ---
        commit_branch = st.text_input("Branch to commit to", value=branch, key="commit_branch")
        commit_message = st.text_input("Commit message", "Refactored code via CodeAgent", key="commit_message")

        if st.button("Push Refactored Code to GitHub Repository"):
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
        
        # ----- Updateing dependencies -------
        st.divider()
        if "requirements.txt" in files and "python_version" in st.session_state:
            requirements = download_file(owner, repo, "requirements.txt", branch)
            st.session_state.updated_requirements = generate_updated_dependencies(client, requirements, st.session_state.python_version, st.session_state.refactor_result)
            col1, col2 = st.columns(2)
            with col1:
                st.write("Old version")
                st.code(requirements, language="python")
            with col2:
                st.write("Updated version")
                st.code(st.session_state.updated_requirements, language = "python")
                
                commit_branch = st.text_input("Branch to commit to", value=branch, key="commit_rqrmts_branch")
                commit_message = st.text_input("Commit message", "Refactored code via CodeAgent", key="commit_rqrmts_msg")

                if st.button("Push Refactored Code to GitHub Repository", key = "rqrmts_btn"):
                    try:
                        commit_file(
                            owner,
                            repo,
                            "requirements.txt",
                            st.session_state.updated_requirements,
                            commit_message,
                            commit_branch  # Use the user-specified branch
                        )
                        st.success(f"Code committed to GitHub branch '{commit_branch}'!")
                    except Exception as e:
                        st.error(f"Failed to commit: {e}")

        # ----- Make Pull Request ------
        st.divider()
        st.subheader("Create Pull Request to `main`")

        pr_branch = st.text_input("PR Branch", value=commit_branch, key="pr_branch")
        pr_title = st.text_input("PR Title", value="Auto Refactor by CodeAgent", key="pr_title")
        pr_body = st.text_area("PR Description", value="This PR contains refactored code and/or updated dependencies generated by CodeAgent.", key="pr_body")

        if st.button("Create Pull Request", key = 'pr_button'):
            try:
                pr_result = create_pull_request(
                    owner=owner,
                    repo=repo,
                    head_branch=pr_branch,
                    base_branch="main",
                    title=pr_title,
                    body=pr_body
                )
                if pr_result["success"]:
                    st.success(pr_result["message"])
                    st.markdown(f"[View PR]({pr_result['url']})")
                else:
                    st.warning(pr_result["message"])
            except Exception as e:
                st.error(f"Failed to create PR: {e}")
        
        # --- Validate & Run Updated Code ---
        st.divider()
        # Save the refactored code to a Python file
        refactor_code_filename = "refactored_code.py"
        with open(refactor_code_filename, "w", encoding="utf-8") as file:
            file.write(st.session_state.refactor_result)

        if "refactor_result" in st.session_state and "updated_requirements" in st.session_state:
            st.subheader("Validate & Run Updated Code")
            if st.button("Run Refactored Code in Virtual Environment"):
                valid, message, installed = validate_requirements_and_run_code(
                    requirements_text=st.session_state.updated_requirements,
                    python_code_file=refactor_code_filename,
                    python_version=st.session_state.python_version
                )
                if valid:
                    st.code(message, language="text")
                    st.code("\n".join(installed), language="text")
                else:
                    st.error(message)

    except Exception as e:
        st.error(f"Error: {e}")