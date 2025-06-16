import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
import requests

def asked_to_gemini(user_input):

    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"

    headers = {
        "Content-Type": "application/json"
    }

    data = {
        "contents": [
            {
                "parts": [
                    {"text": user_input}
                ]
            }
        ]
    }

    response = requests.post(url, headers=headers, json=data).json()
    text = response['candidates'][0]['content']['parts'][0]['text']
    
    return text