def generate_updated_dependencies(client, requirements_text, python_version):
    messages = [
        {
            "role": "system",
            "content": (
                f"You are an assistant that updates Python dependencies. "
                f"You will be given a list of packages from a requirements.txt file. "
                f"Your task is to return only the updated versions that are compatible with Python {python_version}."
                f"Output must follow this format exactly: package==latest_version — one per line. "
                f"DO NOT write code, explanations, comments, or markdown. "
                f"DO NOT say anything except the updated list. Respond ONLY with the updated list."
                f"If any one has no updated version, keep that as it is."
            )
        },
        {
            "role": "user",
            "content": (
                f"My Python version is {python_version}. "
                f"Here are my current dependencies:\n\n{requirements_text}\n\n"
                f"Return only the updated versions that are compatible. "
                f"Format: package==latest_version in text format. Do NOT output code, markdown, or anything else."
            )
        }
    ]

    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=messages,
        temperature=0.5,
        top_p=0.95,
        max_completion_tokens=2048
    )
    return response.choices[0].message.content.strip()
