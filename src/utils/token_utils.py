def estimate_tokens(text):
    return len(text) // 4  # Approx. 1 token = 4 chars

def split_code_into_chunks(code, max_tokens=2000):
    lines = code.split('\n')
    chunks, current_chunk, token_count = [], [], 0

    for line in lines:
        tokens = len(line) // 4
        if token_count + tokens > max_tokens:
            chunks.append('\n'.join(current_chunk))
            current_chunk, token_count = [], 0
        current_chunk.append(line)
        token_count += tokens

    if current_chunk:
        chunks.append('\n'.join(current_chunk))
    return chunks
