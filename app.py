from fastapi import FastAPI, Header, HTTPException
from detector import is_scam
from llm_analyzer import generate_reply, llm_analyze_message

app = FastAPI()

API_KEY = "key123"

@app.post("/honeypot")
def honeypot(payload: dict, x_api_key: str = Header(...)):
    # Validate API key
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    message_text = payload["message"]["text"]

    # Scam detection & intelligence extraction
    scam_detected, intel = llm_analyze_message(message_text)

    # Generate agentic reply via Gemini
    reply = generate_reply(message_text)

    # Build response
    response = {
        "status": "success",
        "reply": reply,
        "scamDetected": scam_detected,
        "extractedIntelligence": {
            "bankAccounts": intel.bankAccounts,
            "upiIds": intel.upiIds,
            "phishingLinks": intel.phishingLinks,
            "phoneNumbers": intel.phoneNumbers,
            "suspiciousKeywords": intel.suspiciousKeywords
        }
    }

    return response
