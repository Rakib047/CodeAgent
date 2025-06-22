def generate_updated_dependencies(client, requirements_text, python_version, code):
    messages = [
        {
            "role": "system",
            "content": (
                "You are an expert Python dependency manager and software compatibility checker.\n"
                "You will be given:\n"
                "- A Python code snippet.\n"
                "- The current requirements.txt content.\n"
                "- A target Python version.\n\n"
                "Your job is to:\n"
                "1. Analyze the code to determine which packages are actually required (based on imports).\n"
                "2. Remove any unused or deprecated packages.\n"
                "3. Return only the names of required external packages needed to run the code, excluding standard libraries.\n"
                "4. Do NOT include version numbers.\n"
                "5. Do NOT include any explanations, formatting, markdown, or extra text — just the list of required packages, one per line."
            )
        },
        {
            "role": "user",
            "content": (
                f"Target Python version: {python_version}\n\n"
                f"Current requirements.txt:\n{requirements_text}\n\n"
                f"Python code to analyze:\n{code}\n\n"
                "Now return only the updated list of required packages — one per line, no version numbers, no explanation."
            )
        }
    ]

    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=messages,
        temperature=0.2,
        top_p=0.95,
        max_completion_tokens=512
    )

    return response.choices[0].message.content.strip()
