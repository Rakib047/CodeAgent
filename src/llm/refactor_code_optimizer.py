def optimize_refactored_code(client, code, instruction):
    messages = [
        {
            "role": "system",
            "content": (
                "You are an expert Python developer. "
                "The user has already received a good refactored version of the code, "
                "but now wants to modify it based on new instructions. "
                "Please apply the requested modifications and return the updated, clean Python code only."
            )
        },
        {
            "role": "user",
            "content": (
                f"Instruction for code modification:\n{instruction}\n\n"
                f"Previously generated code:\n{code}"
            )
        }
    ]
    
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages,
        temperature=0.3,
        top_p=0.9,
        max_tokens=2048 * 3
    )
    
    return response.choices[0].message.content.strip()
