import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def get_api_key():
    if not GEMINI_API_KEY:
        # In a real scenario, we might want to prompt the user or handle this gracefully.
        # For now, we will return None and handle it in the calling code or let it crash if essential.
        return None
    return GEMINI_API_KEY
