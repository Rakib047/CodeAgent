from ..utils.token_utils import estimate_tokens, split_code_into_chunks

import streamlit as st

def refactor_code_chunk(client,code_chunk, python_version="python3"):
    """Refactor a single chunk of code using Groq"""
    if not client:
        return "Groq API key not set or client not initialized."

    messages = [
        {
            "role": "system",
            "content": (
                "You are an expert Python developer and refactoring assistant. "
                "Given legacy Python code, provide the updated python version syntax code keeping the code same. "
                #"Focus on readability, modularity, and best practices. "
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
            temperature=0.3,
            top_p=0.9,
            max_completion_tokens=4096,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"# Error refactoring this chunk: {str(e)}\n{code_chunk}"


def refactor_code_with_groq(client,code_snippet, python_version="python3"):
    """Refactor code with chunking support for large files using Groq"""
    if not client:
        return "Groq API key not set or client not initialized."

    estimated_tokens = estimate_tokens(code_snippet)

    if estimated_tokens <= 2000:
        return refactor_code_chunk(client,code_snippet, python_version)

    st.info(f"Large file detected ({estimated_tokens} estimated tokens). Processing in chunks...")
    chunks = split_code_into_chunks(code_snippet, max_tokens=2000)

    refactored_chunks = []
    progress_bar = st.progress(0)

    for i, chunk in enumerate(chunks):
        st.write(f"Processing chunk {i+1}/{len(chunks)}...")
        refactored_chunk = refactor_code_chunk(chunk, python_version)
        refactored_chunks.append(refactored_chunk)
        progress_bar.progress((i + 1) / len(chunks))

    combined_code = '\n\n'.join(refactored_chunks)
    cleaned_code = clean_refactored_code(combined_code)

    st.success("Refactoring completed!")
    return cleaned_code


def clean_refactored_code(code):
    """Clean up common issues in refactored code"""
    lines = code.split('\n')
    cleaned_lines = []
    seen_imports = set()

    for line in lines:
        stripped = line.strip()
        # Skip duplicate imports
        if stripped.startswith(('import ', 'from ')):
            if stripped not in seen_imports:
                seen_imports.add(stripped)
                cleaned_lines.append(line)
        else:
            cleaned_lines.append(line)

    return '\n'.join(cleaned_lines)

