import re

def clean_refactored_output(text: str) -> str:
    """
    Cleans the refactored code output by removing unwanted parts like markdown code formatting
    and unnecessary markers like 'Changes:', 'Note:', or 'Explanation:'.
    """
    # Remove triple backticks and language tags
    text = re.sub(r"```(?:python)?\n?", "", text)
    text = re.sub(r"\n?```$", "", text)

    # Remove everything after 'Changes:', 'Note:', etc.
    for marker in ["Changes:", "Note:", "Explanation:"]:
        if marker in text:
            text = text.split(marker)[0].strip()

    return text.strip()

def generate_documentation(refactored_code: str, python_version="python3", client=None):
    """
    Generate documentation for the refactored Python code, including inline docstrings, 
    comments for key logic, and a high-level summary in markdown format.
    This version only generates docstrings for the refactored code.
    """
    documentation = []

    # Generate docstrings and comments using an AI service (client can be Groq or similar)
    doc_string = f"Generated documentation for the refactored code in {python_version}:\n"

    messages = [
        {
            "role": "system",
            "content": (
                f"You are a Python expert. Generate docstrings for the following Python code:\n"
                f"Only provide the docstrings for the functions and classes. "
                f"DO NOT include any extra text, explanations, or analysis, just docstrings.\n"
                f"Ensure that the docstrings are correctly placed without affecting the code logic."
            )
        },
        {
            "role": "user",
            "content": f"Generate docstrings for this code:\n\n{refactored_code}"
        }
    ]

    # Call the client (e.g., Groq or another LLM service) to generate documentation
    if client:
        try:
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",  # Specify the model you want to use
                messages=messages,
                temperature=0.3,
                top_p=0.9,
                max_completion_tokens=4096
            )
            documentation.append(response.choices[0].message.content.strip())
        except Exception as e:
            raise Exception(f"Error while generating docstrings: {e}")
    
    doc_string += f"## Code Documentation\n\n" + "\n\n".join(documentation)

    # Match function and class definitions to append docstrings to them
    # Match function and method definitions
    function_pattern = r"def\s+(\w+)\(.*?\):"
    functions = re.findall(function_pattern, refactored_code)

    # Match class definitions
    class_pattern = r"class\s+(\w+)\(.*?\):"
    classes = re.findall(class_pattern, refactored_code)

    doc_string += "\n\n### Docstrings for Functions and Classes:\n"

    # Generate and map docstrings to respective functions and classes
    for func in functions:
        doc_string += f"\n#### Function: {func}\n"
        doc_string += f"\"\"\"Docstring for function {func}.\"\"\"\n"

    for cls in classes:
        doc_string += f"\n#### Class: {cls}\n"
        doc_string += f"\"\"\"Docstring for class {cls}.\"\"\"\n"

    return doc_string
