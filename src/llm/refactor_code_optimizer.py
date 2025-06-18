

def generate_test_cases(client, code, instruction):
    messages = [
        {
            "role": "system",
            "content": (
                "You are an expert Python developer and you have generated a good code."
                "But I need some modification on your developed code on given instruction"
                "Please re generate the code with with the given instruction"
                f"Your previously generated code is\n\n: {code} \n\n"
            )
        },
        {
            "role": "user",
            "content": f"Please Modify the code with following instruction:\n\n{instruction}"
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
