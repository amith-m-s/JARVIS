import os

try:
    from dotenv import load_dotenv

    load_dotenv()
except Exception:
    pass

class Config:
    OLLAMA_URL = os.getenv("OLLAMA_URL", "http://127.0.0.1:11434")
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3") 
    TTS_RATE = int(os.getenv("TTS_RATE", "185"))
    WAKE_WORD = os.getenv("WAKE_WORD", "jarvis").lower()