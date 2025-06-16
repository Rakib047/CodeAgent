import streamlit as st
from utils.git_repo_hendler import get_repo_files, download_file
from services.groqAI.version_converter import convert_python_version
import tiktoken

# Function to split text into chunks based on token limit
def chunk_text(text, max_tokens=2000):
    enc = tiktoken.get_encoding("cl100k_base")  # or appropriate tokenizer
    tokens = enc.encode(text)
    
    chunks = []
    for i in range(0, len(tokens), max_tokens):
        chunk = tokens[i:i + max_tokens]
        chunks.append(enc.decode(chunk))
    return chunks

def main_body(memory, setting):
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
                instruction = st.text_input('Enter Query about Code: ')

                convert_button = st.button("Analyse Code")
                if convert_button and content:
                    with st.spinner("Converting..."):
                        code_chunks = chunk_text(content, max_tokens=7000)
                        updated_chunks = []
                        
                        for i, chunk in enumerate(code_chunks):
                            st.info(f"Processing chunk {i+1} of {len(code_chunks)}...")
                            updated_chunk = convert_python_version(
                                code=chunk,
                                instruction=instruction,
                                memory=memory,
                                **setting
                            )
                            updated_chunks.append(updated_chunk)
                        
                        updated_code = "\n".join(updated_chunks)
                        st.subheader("Converted Code") 
                        st.write(updated_code)
                        
                    st.session_state.chat_history.append({'human': content, 'AI': updated_code})


            else:
                st.warning("No files found or invalid repository/branch.")
        except Exception as e:
            st.error(f"Error parsing GitHub URL: {e}")