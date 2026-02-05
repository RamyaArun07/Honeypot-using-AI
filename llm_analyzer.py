import json
import re
from intelligence import Intelligence
from llm_client import call_gemini


def _safe_json_extract(text: str) -> dict:
    """
    Safely extract JSON from Gemini response
    """
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        raise ValueError("No JSON found in LLM response")
    return json.loads(match.group())


def llm_analyze_message(text: str):
    """
    Scam detection and intelligence extraction using Gemini
    """
    prompt = f"""
You are a cybersecurity AI.

Analyze the message below and respond in STRICT JSON only.
Do NOT include explanations.

Tasks:
1. Decide if the message is a scam (true/false)
2. Extract:
   - bankAccounts
   - upiIds
   - phishingLinks
   - phoneNumbers
   - suspiciousKeywords

JSON format:
{{
  "isScam": true,
  "bankAccounts": [],
  "upiIds": [],
  "phishingLinks": [],
  "phoneNumbers": [],
  "suspiciousKeywords": []
}}

Message:
{text}
"""

    response = call_gemini(prompt)

    data = _safe_json_extract(response)

    intel = Intelligence()
    intel.bankAccounts = data.get("bankAccounts", [])
    intel.upiIds = data.get("upiIds", [])
    intel.phishingLinks = data.get("phishingLinks", [])
    intel.phoneNumbers = data.get("phoneNumbers", [])
    intel.suspiciousKeywords = data.get("suspiciousKeywords", [])

    return data.get("isScam", False), intel


def generate_reply(message_text: str) -> str:
    """
    Generate a natural, agentic reply via Gemini
    """
    prompt = f"""
You are an ordinary bank customer replying to a message.

Your goal is to keep the conversation going naturally and make the sender explain more.

Rules:
- Do NOT use greetings like "hello", "hi", or filler phrases
- Do NOT mention scams, fraud, police, or security
- Sound genuine, slightly confused, and cooperative
- Ask questions that encourage the sender to share details
- Ask about steps, payment method, or verification
- Keep the reply to 1–2 short sentences
- Reply as if this is a real conversation, not an analysis

Message received:
"{message_text}"

Reply:
"""

    response = call_gemini(prompt)
    return response.strip()
