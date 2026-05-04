from __future__ import annotations

from jarvis.core.config import Config

try:
    import pyttsx3
except Exception:
    pyttsx3 = None


class Speaker:
    def __init__(self):
        self.enabled = False
        self.engine = None

        if pyttsx3 is None:
            return

        try:
            self.engine = pyttsx3.init()
            self.engine.setProperty("rate", Config.TTS_RATE)
            self.enabled = True
        except Exception:
            self.enabled = False

    def say(self, text: str) -> None:
        print(f"JARVIS: {text}")

        if not self.enabled or self.engine is None:
            return

        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception:
            pass
