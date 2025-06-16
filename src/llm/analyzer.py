from ..utils.token_utils import estimate_tokens, split_code_into_chunks

def generate_analysis_summary(analysis_results):
    """Generate a summary of all analysis chunks"""
    if not analysis_results:
        return "## Summary\n\nNo analysis results available."
    
    # Count common issues across chunks
    common_issues = []
    if any("Python 2" in result.lower() or "python2" in result.lower() for result in analysis_results):
        common_issues.append("• Legacy Python 2 syntax detected across multiple sections")
    if any("hard-coded" in result.lower() or "hardcoded" in result.lower() for result in analysis_results):
        common_issues.append("• Hard-coded values found in the codebase")
    if any("deprecated" in result.lower() for result in analysis_results):
        common_issues.append("• Deprecated libraries or methods detected")
    if any("code smell" in result.lower() for result in analysis_results):
        common_issues.append("• Code quality issues identified")
    
    summary = "## 📊 Overall Analysis Summary\n\n"
    summary += f"**File analyzed in {len(analysis_results)} chunks**\n\n"
    
    if common_issues:
        summary += "**Common Issues Found:**\n"
        summary += '\n'.join(common_issues)
    else:
        summary += "**No major issues detected** - Code appears to follow good practices."
    
    return summary

def analyze_code_chunk(client, code_chunk, chunk_number=1, total_chunks=1):
    """Analyze a single chunk of code"""
    if not client:
        return "Groq API key not set or client not initialized."
    
    chunk_info = f" (Chunk {chunk_number}/{total_chunks})" if total_chunks > 1 else ""
    
    messages = [
        {
            "role": "system",
            "content": (
                "You are an expert Python developer and code reviewer. "
                "Provide a thorough, itemized analysis of the given Python code. "
                "Focus on specific issues found in this code segment."
            ),
        },
        {
            "role": "user",
            "content": (
                f"Analyze the following Python code{chunk_info} and provide a detailed report including:\n"
                "- Outdated or deprecated Python 2 syntax\n"
                "- Any code smells or anti-patterns\n"
                "- Detection of hard-coded values or deprecated libraries\n"
                "- Suggestions for syntax improvements and architectural refactoring\n"
                "Provide your answer as a numbered list or bullet points.\n\n"
                + code_chunk
            ),
        },
    ]

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages,
            temperature=0.7,
            top_p=0.9,
            max_completion_tokens=2048,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error analyzing chunk {chunk_number}: {str(e)}"


def analyze_large_code(client, code_snippet, st):
    """Analyze code with chunking support for large files"""
    if not client:
        return "Groq API key not set or client not initialized."

    tokens = estimate_tokens(code_snippet)

    if tokens <= 4000:
        return analyze_code_chunk(client, code_snippet)

    st.info(f"Large file detected ({tokens} estimated tokens). Analyzing in chunks...")
    chunks = split_code_into_chunks(code_snippet, max_tokens=3000)

    analysis_results = []
    progress_bar = st.progress(0)

    for i, chunk in enumerate(chunks):
        st.write(f"Analyzing chunk {i+1}/{len(chunks)}...")
        result = analyze_code_chunk(client, chunk, i + 1, len(chunks))

        if result and not result.startswith("Error"):
            analysis_results.append(f"## Analysis for Chunk {i+1}/{len(chunks)}\n\n{result}")
        else:
            analysis_results.append(f"## Chunk {i+1}/{len(chunks)} - Analysis Failed\n\n{result}")

        progress_bar.progress((i + 1) / len(chunks))

    summary = generate_analysis_summary(analysis_results)
    st.success("Code analysis completed!")
    return f"{summary}\n\n---\n\n" + "\n\n".join(analysis_results)
