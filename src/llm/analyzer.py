from .groq_client import get_groq_client
from ..utils.token_utils import estimate_tokens, split_code_into_chunks

def analyze_code_chunk(client, code_chunk, chunk_number=1, total_chunks=1):
    messages = [
        {
            "role": "system",
            "content": (
                "You are a senior Python code reviewer. "
                "Your job is to identify issues in Python code chunks. "
                "Focus only on detecting the following problems:\n"
                "- Outdated or deprecated Python syntax\n"
                "- Hard-coded values and magic numbers\n"
                "- Code smells (long functions, deep nesting, etc.)\n"
                "- Common anti-patterns (e.g., mutable default args, bad exception handling)\n"
                "- Bad practices affecting readability or maintainability\n\n"
                "Return a concise list of issues found in the code. Do not suggest fixes. "
                "Do not refactor. Only analyze problems."
            )
        },
        {
            "role": "user",
            "content": f"Analyze the following code chunk ({chunk_number}/{total_chunks}):\n\n{code_chunk}"
        }
    ]
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages,
        temperature=0.7,
        top_p=0.9,
        max_completion_tokens=2048
    )
    return response.choices[0].message.content.strip()


def analyze_large_code(client, code_snippet, st=None):
    tokens = estimate_tokens(code_snippet)
    if tokens <= 4000:
        return analyze_code_chunk(client, code_snippet)

    if st: st.info("🔍 Analyzing code in chunks...")
    chunks = split_code_into_chunks(code_snippet)
    return "\n\n".join([
        analyze_code_chunk(client, chunk, i + 1, len(chunks))
        for i, chunk in enumerate(chunks)
    ])
