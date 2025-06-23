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
                "3. Return the updated list of required packages **with correct version numbers** that are:\n"
                "   - Available on PyPI\n"
                "   - Compatible with the specified Python version\n"
                "   - Do not rely on removed or deprecated standard libraries (e.g., distutils in Python 3.12+)\n"
                "4. Ensure any package that depends on `distutils` works properly by:\n"
                "   - Using modern alternatives or newer versions that do not require it explicitly\n"
                "   - Ensuring `setuptools` is included if needed to support legacy builds\n\n"
                "Return ONLY the updated requirements.txt — one package per line, with valid version numbers.\n"
                "Do NOT include explanations, markdown, or extra text."
            )
        },
        {
            "role": "user",
            "content": (
                f"Target Python version: {python_version}\n\n"
                f"Current requirements.txt:\n{requirements_text}\n\n"
                f"Python code to analyze:\n{code}\n\n"
                "Now return the updated list of required packages — one per line with version numbers, and make sure all are installable for the given Python version."
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
