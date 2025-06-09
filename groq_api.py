import streamlit as st
import requests
import os
from groq import Groq  # Groq Python SDK client

st.set_page_config(page_title="GitHub Repo Browser", layout="wide")
st.title("CodeAgent: GitHub Repository Code Analysis and Refactoring")

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

# Initialize Groq client with your API key from environment
groq_api_key = "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"
if not groq_api_key:
    st.warning("Set your GROQ_API_KEY environment variable for AI analysis")

client = Groq(api_key=groq_api_key) if groq_api_key else None

def analyze_code_with_groq(code_snippet):
    if not client:
        return "Groq API key not set or client not initialized."
    messages = [
        {
            "role": "system",
            "content": (
                "You are an expert Python developer and code reviewer. "
                "Provide a thorough, itemized analysis of the given Python 2 code."
            ),
        },
        {
            "role": "user",
            "content": (
                "Analyze the following Python code and provide a detailed report including:\n"
                "- Outdated or deprecated Python 2 syntax\n"
                "- Any code smells or anti-patterns\n"
                "- Detection of hard-coded values or deprecated libraries\n"
                "- Suggestions for syntax improvements and architectural refactoring\n"
                "Provide your answer as a numbered list or bullet points.\n\n"
                + code_snippet
            ),
        },
    ]

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages,
        temperature=0.7,
        top_p=0.9,
        max_completion_tokens=512,
    )
    return response.choices[0].message.content


def refactor_code_with_groq(code_snippet, python_version="python3"):
    if not client:
        return "Groq API key not set or client not initialized."
    messages = [
        {
            "role": "system",
            "content": (
                "You are an expert Python developer and refactoring assistant. "
                "Given legacy Python 2 code, suggest a modern, idiomatic, and "
                "clean refactored version of the code focusing on readability, modularity, "
                "and best practices. "
                "Do not change the logic but improve syntax and structure. "
                "Refactor the code according to the following Python version: "
                + python_version
            ),
        },
        {
            "role": "user",
            "content": (
                "Refactor this Python 2 code snippet. Provide only the refactored code "
                "with minimal explanation:\n\n"
                + code_snippet
            ),
        },
    ]

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages,
        temperature=0.7,
        top_p=0.9,
        max_completion_tokens=1024,
    )

    return response.choices[0].message.content
    


# def generate_tests_with_groq(code_snippet):
#     if not client:
#         return "Groq API key not set or client not initialized."
#     messages = [
#         {
#             "role": "system",
#             "content": (
#                 "You are an expert Python developer specialized in writing test cases. "
#                 "Generate unit test functions for the given Python 2 code. "
#                 "Use unittest framework style. "
#                 "Include meaningful test cases for all public methods and functions."
#             ),
#         },
#         {
#             "role": "user",
#             "content": (
#                 "Generate Python 2 compatible unit tests for the following code:\n\n"
#                 + code_snippet
#             ),
#         },
#     ]

#     response = client.chat.completions.create(
#         model="llama-3.1-8b-instant",
#         messages=messages,
#         temperature=0.7,
#         top_p=0.9,
#         max_completion_tokens=512,
#     )
#     return response.choices[0].message.content




# ---------- UI ----------
github_url = st.text_input("🔗 Enter GitHub Repository URL", placeholder="https://github.com/owner/repo")

if github_url:
    try:
        parts = github_url.strip().replace("https://", "").replace("http://", "").split("/")
        owner = parts[1]
        repo = parts[2]

        branch = st.text_input("🌿 Branch name (default: main)", value="main")

        with st.spinner("Fetching files..."):
            file_list = get_repo_files(owner, repo, branch)

        if file_list:
            selected_file = st.selectbox("📄 Select a file to view", file_list)
            content = download_file(owner, repo, selected_file, branch)
            st.code(content, language=selected_file.split('.')[-1] if '.' in selected_file else "text")

            # New: Analyze with AI button
            if st.button("Analyze Code with AI"):
                if content:
                    with st.spinner("Analyzing code with AI..."):
                        try:
                            analysis_result = analyze_code_with_groq(content)
                            st.subheader("AI Analysis Result:")
                            st.write(analysis_result)
                        except Exception as e:
                            st.error(f"Failed to analyze code: {e}")
                else:
                    st.warning("No code content to analyze.")

                                # Refactor Code Button with Python version input
            python_version = st.text_input(
                "Enter the Python version for refactoring (e.g., python3.6, python3.7, etc.):"
            )

            if st.button("Suggest Code Refactor with AI"):
                if content and python_version:
                    with st.spinner("Generating refactor suggestion..."):
                        try:
                            refactor_result = refactor_code_with_groq(content, python_version)
                            st.subheader("AI Refactor Suggestion:")
                            st.code(refactor_result, language=selected_file.split('.')[-1] if '.' in selected_file else "python")
                        except Exception as e:
                            st.error(f"Failed to generate refactor suggestion: {e}")
                elif not python_version:
                    st.warning("Please specify a Python version for refactoring.")
                else:
                    st.warning("No code content to refactor.")

            # # Generate Tests Button
            # if st.button("Generate Unit Tests with AI"):
            #     if content:
            #         with st.spinner("Generating test functions..."):
            #             try:
            #                 tests_result = generate_tests_with_groq(content)
            #                 st.subheader("AI Generated Test Functions:")
            #                 st.code(tests_result, language="python")
            #             except Exception as e:
            #                 st.error(f"Failed to generate test functions: {e}")
            #     else:
            #         st.warning("No code content to generate tests for.")
        else:
            st.warning("No files found or invalid repository/branch.")
    except Exception as e:
        st.error(f"Error parsing GitHub URL: {e}")


# Refactor button
# if st.button("Suggest Code Refactor with AI"):
#     if content:
#         with st.spinner("Generating refactor suggestion..."):
#             try:
#                 refactor_result = refactor_code_with_groq(content)
#                 st.subheader("AI Refactor Suggestion:")
#                 st.code(refactor_result, language=selected_file.split('.')[-1] if '.' in selected_file else "python")
#             except Exception as e:
#                 st.error(f"Failed to generate refactor suggestion: {e}")
#     else:
#         st.warning("No code content to refactor.")
