from groq import Groq
import os

def get_groq_client(api_key=None):
    key = "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"
    if not key:
        raise ValueError("GROQ API key is missing.")
    return Groq(api_key=key)
