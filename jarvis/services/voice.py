from __future__ import annotations

try:
    import speech_recognition as sr
except Exception:
    sr = None


class VoiceInput:
    def __init__(self):
        self.enabled = False
        self.recognizer = None

        if sr is None:
            return

        try:
            self.recognizer = sr.Recognizer()
            self.enabled = True
        except Exception:
            self.enabled = False

    def listen(self) -> str | None:
        if not self.enabled or self.recognizer is None:
            return None

        try:
            with sr.Microphone() as source:
                print("🎤 Listening...")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.4)
                audio = self.recognizer.listen(source, timeout=6, phrase_time_limit=8)

            return self.recognizer.recognize_google(audio)
        except Exception:
            return None
