from llm_analyzer import llm_analyze_message

def is_scam(message_text: str):
    """
    Wrapper for scam detection
    """
    return llm_analyze_message(message_text)
