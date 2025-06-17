

def generate_test_cases(client, code_chunk):
    messages = [
        {
            "role": "system",
            "content": (
                "You are an expert Python developer and test engineer. "
                "Given a Python function, class, or script, generate well-structured unit test cases using the `pytest` framework. "
                "Ensure all important behaviors are covered, and use meaningful test method names.\n\n"
                "Only return raw test code without any explanations or markdown formatting."
            )
        },
        {
            "role": "user",
            "content": f"Generate test cases for the following code:\n\n{code_chunk}"
        }
    ]
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages,
        temperature=0.3,
        top_p=0.9,
        max_completion_tokens=2048*2
    )
    return response.choices[0].message.content.strip()
