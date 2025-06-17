from .groq_client import get_groq_client
from ..utils.token_utils import estimate_tokens, split_code_into_chunks

import re


def clean_refactored_output(text: str) -> str:
    # Remove triple backticks and language tags
    text = re.sub(r"```(?:python)?\n?", "", text)
    text = re.sub(r"\n?```$", "", text)

    # Remove everything after 'Changes:', 'Note:', etc.
    for marker in ["Changes:", "Note:", "Explanation:"]:
        if marker in text:
            text = text.split(marker)[0].strip()

    return text.strip()

def extract_code_block(text):
    """Extracts the first Python code block from a markdown response."""
    match = re.search(r"```(?:python)?\s*(.*?)```", text, re.DOTALL)
    return match.group(1).strip() if match else text.strip()

def refactor_code_chunk(client, code_chunk, python_version="python3"):
    messages = [
        {
            "role": "system",
            "content": (
                f"You are a Python expert. Refactor the following code into clean, modern {python_version} syntax.\n"
                "Return ONLY the pure refactored code. DO NOT include markdown formatting (like ```), comments, or explanations.\n"
                "Do NOT include lists of changes, analysis, or any extra text. Just return clean code only."
            )
        },
        {
            "role": "user",
            "content": f"Refactor this Python code:\n\n{code_chunk}"
        }
    ]

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages,
        temperature=0.3,
        top_p=0.9,
        max_completion_tokens=4096
    )
    raw_output = response.choices[0].message.content.strip()
    return clean_refactored_output(raw_output)


def refactor_large_code(client, code_snippet, st=None, python_version="python3"):
    tokens = estimate_tokens(code_snippet)
    if tokens <= 2000:
        return refactor_code_chunk(client, code_snippet, python_version)

    if st: st.info("🔧 Refactoring code in chunks...")
    chunks = split_code_into_chunks(code_snippet)
    return "\n\n".join([
        extract_code_block(refactor_code_chunk(client, chunk, python_version))
        for chunk in chunks
    ])
