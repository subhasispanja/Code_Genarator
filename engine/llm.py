import os
from dotenv import load_dotenv
import streamlit as st
from google import genai

# Load local .env variables
load_dotenv()

# First try Streamlit Secrets, then local environment variable
API_KEY = st.secrets.get("GOOGLE_API_KEY") or os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    raise RuntimeError("GOOGLE_API_KEY not configured")

# Create Gemini client
client = genai.Client(api_key=API_KEY)

MODEL_NAME = "models/gemini-flash-latest"


def generate_code(prompt: str) -> str:
    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )

        if not response or not response.text:
            raise RuntimeError("Empty response from Gemini")

        return response.text.strip()

    except Exception as e:
        raise RuntimeError(f"LLM generation failed: {e}")