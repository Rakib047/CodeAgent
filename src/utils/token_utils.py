def estimate_tokens(text):
    return len(text) // 4

def split_code_into_chunks(code, max_tokens=2000):
    lines = code.split('\n')
    chunks, current_chunk, current_tokens = [], [], 0
    for line in lines:
        tokens = len(line) // 4
        if current_tokens + tokens > max_tokens:
            chunks.append('\n'.join(current_chunk))
            current_chunk, current_tokens = [], 0
        current_chunk.append(line)
        current_tokens += tokens
    if current_chunk:
        chunks.append('\n'.join(current_chunk))
    return chunks
