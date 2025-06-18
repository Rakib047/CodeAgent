from groq import Groq
import os
from dotenv import load_dotenv
load_dotenv()

def get_groq_client():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("Missing GROQ_API_KEY in environment.")
    return Groq(api_key=api_key)