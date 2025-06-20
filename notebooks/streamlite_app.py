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

# --- Setup ---
st.set_page_config(page_title="CodeAgent", layout="wide")
st.title("🧠 CodeAgent: Code Analyzer & Refactorer")

if "refactor_step" not in st.session_state:
    st.session_state.refactor_step = 0

if "regenerate_clicked" not in st.session_state:
    st.session_state.regenerate_clicked = False

# --- GitHub Input ---
st.subheader("🔗 Load GitHub File")
url = st.text_input("GitHub Repository URL", placeholder="https://github.com/user/repo")
if url:
    owner, repo = url.split("/")[-2:]
    branch = st.text_input("🌿 Branch", value="main")

    try:
        # Track previously selected file
        if 'prev_file' not in st.session_state:
            st.session_state.prev_file = None

        files = get_repo_files(owner, repo, branch)
        file = st.selectbox("📄 Choose File", files)

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
        
        if st.button("🔍 Analyze Code"):
            st.session_state.analysis_result = analyze_large_code(client, content, st)
        # --- Analysis Result ---
        if "analysis_result" in st.session_state:
            with st.expander("🔍 Code Analysis", expanded=True):
                st.markdown(st.session_state.analysis_result)
                
        st.divider()
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔧 Refactor Code"):
                st.session_state.refactor_step = 1
        with col2:
            if st.button("📊 Show Full Code Diff") and "refactor_result" in st.session_state:
                st.session_state.code_diff = generate_full_diff(content, st.session_state.refactor_result)

         
        col1, col2 = st.columns(2)
        with col1:
        # --- Refactoring Input ---
            if "refactor_step" in st.session_state and st.session_state.refactor_step == 1:
                python_version = st.text_input("🐍 Python Version (e.g., python3.10)", key="version_input")
                if st.button("✅ Start Refactoring"):
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
                with st.expander("♻️ Modify Refactored Code", expanded=False):
                    if st.button("✏️ Re-generate"):
                        st.session_state.regenerate_clicked = True

                    if st.session_state.regenerate_clicked:
                        instruction = st.text_input("📌 Instruction to update code", key="instruction_input")
                        if st.button("🚀 Apply Modification"):
                            if instruction.strip():
                                st.session_state.refactor_result = optimize_refactored_code(
                                    client,
                                    st.session_state.refactor_result,
                                    instruction.strip()
                                )
                                st.success("✅ Code regenerated.")
                                st.session_state.regenerate_clicked = False
        with col2:
            if "code_diff" in st.session_state:
                with st.expander("📊 Code Diff", expanded=True):
                    st.code(st.session_state.code_diff, language="diff")

        st.divider()

        # --- Additional Features ---
        if "refactor_result" in st.session_state:
            col1, col2 = st.columns(2)

            with col1:
                if st.button("🧪 Generate Test Cases"):
                    st.session_state.generated_test_cases = generate_test_cases(client, st.session_state.refactor_result)
                if "generated_test_cases" in st.session_state:
                    st.code(st.session_state.generated_test_cases, language="python")

            with col2:
                if st.button("📜 Generate Documentation"):
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

    except Exception as e:
        st.error(f"❌ Error: {e}")