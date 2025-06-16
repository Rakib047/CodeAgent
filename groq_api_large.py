import streamlit as st
import requests
import os
from groq import Groq
import re

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

# Initialize Groq client
groq_api_key = "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"
client = Groq(api_key=groq_api_key) if groq_api_key else None

def estimate_tokens(text):
    """Rough token estimation (1 token ≈ 4 characters)"""
    return len(text) // 4

def split_code_into_chunks(code, max_tokens=2000):
    """Split code into logical chunks based on functions/classes"""
    lines = code.split('\n')
    chunks = []
    current_chunk = []
    current_tokens = 0
    
    i = 0
    while i < len(lines):
        line = lines[i]
        line_tokens = estimate_tokens(line)
        
        # Check if we need to start a new chunk
        if current_tokens + line_tokens > max_tokens and current_chunk:
            chunks.append('\n'.join(current_chunk))
            current_chunk = []
            current_tokens = 0
        
        current_chunk.append(line)
        current_tokens += line_tokens
        
        # If we're at a function/class definition, try to keep it together
        if line.strip().startswith(('def ', 'class ')) and i < len(lines) - 1:
            # Find the end of this function/class
            indent_level = len(line) - len(line.lstrip())
            j = i + 1
            while j < len(lines):
                next_line = lines[j]
                if next_line.strip() and (len(next_line) - len(next_line.lstrip())) <= indent_level:
                    break
                j += 1
            
            # If the function/class is small enough, keep it in current chunk
            func_lines = lines[i:j]
            func_tokens = sum(estimate_tokens(l) for l in func_lines)
            
            if current_tokens + func_tokens <= max_tokens:
                current_chunk.extend(func_lines[1:])  # Skip the first line as it's already added
                current_tokens += func_tokens - line_tokens  # Subtract line_tokens as it was already added
                i = j - 1  # Will be incremented at the end of loop
        
        i += 1
    
    if current_chunk:
        chunks.append('\n'.join(current_chunk))
    
    return chunks

def analyze_code_with_groq(code_snippet):
    if not client:
        return "Groq API key not set or client not initialized."
    
    # Check if code is too long
    estimated_tokens = estimate_tokens(code_snippet)
    if estimated_tokens > 3000:
        st.warning(f"Code is quite large ({estimated_tokens} estimated tokens). Analysis might be truncated.")
    
    messages = [
        {
            "role": "system",
            "content": (
                "You are an expert Python developer and code reviewer. "
                "Provide a thorough, itemized analysis of the given Python code."
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

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages,
            temperature=0.7,
            top_p=0.9,
            max_completion_tokens=2048,  # Increased limit
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error during analysis: {str(e)}"

def refactor_code_chunk(code_chunk, python_version="python3"):
    """Refactor a single chunk of code"""
    if not client:
        return "Groq API key not set or client not initialized."
    
    messages = [
        {
            "role": "system",
            "content": (
                "You are an expert Python developer and refactoring assistant. "
                "Given legacy Python code, provide a modern, idiomatic, and clean refactored version. "
                "Focus on readability, modularity, and best practices. "
                "Preserve the original logic and functionality. "
                f"Target Python version: {python_version}. "
                "IMPORTANT: Provide ONLY the refactored code without explanations or markdown formatting."
            ),
        },
        {
            "role": "user",
            "content": (
                "Refactor this Python code snippet. Return only the refactored code:\n\n"
                + code_chunk
            ),
        },
    ]

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages,
            temperature=0.3,  # Lower temperature for more consistent output
            top_p=0.9,
            max_completion_tokens=4096,  # Increased limit
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"# Error refactoring this chunk: {str(e)}\n{code_chunk}"

def refactor_code_with_groq(code_snippet, python_version="python3"):
    """Refactor code with chunking support for large files"""
    if not client:
        return "Groq API key not set or client not initialized."
    
    estimated_tokens = estimate_tokens(code_snippet)
    
    # If code is small enough, refactor directly
    if estimated_tokens <= 2000:
        return refactor_code_chunk(code_snippet, python_version)
    
    # For large files, split into chunks
    st.info(f"Large file detected ({estimated_tokens} estimated tokens). Processing in chunks...")
    chunks = split_code_into_chunks(code_snippet, max_tokens=2000)
    
    refactored_chunks = []
    progress_bar = st.progress(0)
    
    for i, chunk in enumerate(chunks):
        st.write(f"Processing chunk {i+1}/{len(chunks)}...")
        refactored_chunk = refactor_code_chunk(chunk, python_version)
        refactored_chunks.append(refactored_chunk)
        progress_bar.progress((i + 1) / len(chunks))
    
    # Combine all refactored chunks
    refactored_code = '\n\n'.join(refactored_chunks)
    
    # Clean up any duplicate imports or common issues
    refactored_code = clean_refactored_code(refactored_code)
    
    st.success("Refactoring completed!")
    return refactored_code

def clean_refactored_code(code):
    """Clean up common issues in refactored code"""
    lines = code.split('\n')
    cleaned_lines = []
    seen_imports = set()
    
    for line in lines:
        # Remove duplicate imports
        if line.strip().startswith(('import ', 'from ')):
            if line.strip() not in seen_imports:
                seen_imports.add(line.strip())
                cleaned_lines.append(line)
        else:
            cleaned_lines.append(line)
    
    return '\n'.join(cleaned_lines)

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
            
            # Show file info
            if content and not content.startswith("Error"):
                estimated_tokens = estimate_tokens(content)
                st.info(f"File size: {len(content)} characters, ~{estimated_tokens} tokens")
            
            st.code(content, language=selected_file.split('.')[-1] if '.' in selected_file else "text")

            # Analyze with AI button
            if st.button("🔍 Analyze Code with AI"):
                if content and not content.startswith("Error"):
                    with st.spinner("Analyzing code with AI..."):
                        try:
                            analysis_result = analyze_code_with_groq(content)
                            st.subheader("🎯 AI Analysis Result:")
                            st.write(analysis_result)
                        except Exception as e:
                            st.error(f"Failed to analyze code: {e}")
                else:
                    st.warning("No valid code content to analyze.")

            # Refactor Code section
            st.subheader("🔧 Code Refactoring")
            col1, col2 = st.columns([2, 1])
            
            with col1:
                python_version = st.selectbox(
                    "Select target Python version:",
                    ["python3", "python3.8", "python3.9", "python3.10", "python3.11", "python3.12"],
                    index=0
                )
            
            with col2:
                chunk_size = st.selectbox(
                    "Processing mode:",
                    ["Auto (Recommended)", "Small chunks (1000 tokens)", "Large chunks (3000 tokens)"],
                    index=0
                )

            if st.button("🚀 Refactor Code with AI"):
                if content and not content.startswith("Error"):
                    with st.spinner("Generating refactor suggestion..."):
                        try:
                            refactor_result = refactor_code_with_groq(content, python_version)
                            st.subheader("✨ AI Refactored Code:")
                            st.code(refactor_result, language="python")
                            
                            # Provide download option for large refactored code
                            if len(refactor_result) > 1000:
                                st.download_button(
                                    label="📥 Download Refactored Code",
                                    data=refactor_result,
                                    file_name=f"refactored_{selected_file}",
                                    mime="text/plain"
                                )
                        except Exception as e:
                            st.error(f"Failed to generate refactor suggestion: {e}")
                else:
                    st.warning("No valid code content to refactor.")
        else:
            st.warning("No files found or invalid repository/branch.")
    except Exception as e:
        st.error(f"Error parsing GitHub URL: {e}")