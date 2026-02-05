import re
from intelligence import Intelligence

def fallback_extract(text: str):
    intel = Intelligence()

    intel.upiIds += re.findall(r"\b[a-zA-Z0-9.\-_]{2,}@[a-zA-Z]{2,}\b", text)
    intel.phoneNumbers += re.findall(r"\b\d{10}\b", text)
    intel.phishingLinks += re.findall(r"https?://\S+", text)

    for word in ["verify", "urgent", "blocked", "account", "bank"]:
        if word in text.lower():
            intel.suspiciousKeywords.append(word)

    return intel
