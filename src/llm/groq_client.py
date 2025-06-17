from groq import Groq
import os

def get_groq_client(api_key="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"):
    key = api_key 
    if not key:
        raise ValueError("Missing GROQ API key.")
    return Groq(api_key=key)





#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