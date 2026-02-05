import os
import requests

# Get your Gemini API Key from environment variable
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable not set")

GEMINI_URL = (
    "https://generativelanguage.googleapis.com/v1/models/"
    "gemini-2.5-flash:generateContent"
)

HEADERS = {
    "Content-Type": "application/json",
    "X-Goog-Api-Key": GEMINI_API_KEY
}

def call_gemini(prompt: str) -> str:
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }
    response = requests.post(GEMINI_URL, headers=HEADERS, json=payload, timeout=15)
    response.raise_for_status()
    data = response.json()
    return data["candidates"][0]["content"]["parts"][0]["text"]
