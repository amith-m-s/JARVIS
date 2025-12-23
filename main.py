import os
import datetime
import webbrowser
import urllib.parse
import subprocess
import requests
import wikipedia
import pyttsx3
import warnings

from openai import OpenAI

# ---------------- CLEAN OUTPUT ----------------
try:
    from bs4 import GuessedAtParserWarning
    warnings.filterwarnings("ignore", category=GuessedAtParserWarning)
except Exception:
    pass

# ---------------- CONFIG ----------------
client = OpenAI()  # uses OPENAI_API_KEY
wikipedia.set_lang("en")

# ---------------- JARVIS ----------------
class Jarvis:
    def __init__(self):
        self.memory = []
        self.browser = webbrowser
        self.tts = pyttsx3.init()

    # ---------- SPEAK ----------
    def speak(self, text):
        print(f"Jarvis: {text}")
        try:
            self.tts.say(text)
            self.tts.runAndWait()
        except:
            pass

    # ---------- CHATGPT-LEVEL AI ----------
    def ai(self, user_input):
        if not os.getenv("OPENAI_API_KEY"):
            self.speak("AI systems are offline, sir.")
            return

        self.memory.append({"role": "user", "content": user_input})
        self.memory = self.memory[-12:]

        messages = [
            {
                "role": "system",
                "content": (
                    "You are JARVIS, an advanced AI assistant like ChatGPT. "
                    "Answer accurately, clearly, and precisely. "
                    "If a question has a factual answer, give it. "
                    "If reasoning is required, explain step by step."
                ),
            }
        ] + self.memory

        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
            )
            answer = response.choices[0].message.content.strip()
            self.memory.append({"role": "assistant", "content": answer})
            self.speak(answer)
        except Exception:
            self.speak("I encountered a temporary AI issue, sir.")

    # ---------- WEATHER ----------
    def weather(self, place):
        try:
            url = f"https://wttr.in/{urllib.parse.quote(place)}?format=3"
            r = requests.get(url, timeout=5)
            if r.status_code == 200 and r.text.strip():
                self.speak(r.text.strip())
            else:
                raise Exception
        except:
            self.speak(
                f"I'm unable to access live weather data right now, sir. "
                f"Opening detailed weather information for {place}."
            )
        self.browser.open(
            "https://www.google.com/search?"
            + urllib.parse.urlencode({"q": f"weather {place}"})
        )

    # ---------- WIKIPEDIA ----------
    def wiki(self, topic):
        try:
            summary = wikipedia.summary(topic, sentences=2)
            self.speak(summary)
            page = wikipedia.page(topic)
            self.browser.open(page.url)
        except:
            self.speak("Opening Wikipedia search results, sir.")
            self.browser.open(
                "https://en.wikipedia.org/wiki/Special:Search?"
                + urllib.parse.urlencode({"search": topic})
            )

    # ---------- SYSTEM ----------
    def system(self, cmd):
        try:
            if "notepad" in cmd:
                subprocess.Popen("notepad")
            elif "calculator" in cmd:
                subprocess.Popen("calc")
            elif "explorer" in cmd or "files" in cmd:
                subprocess.Popen("explorer")
            else:
                return False
            self.speak("Done, sir.")
            return True
        except:
            return False

    # ---------- ROUTER ----------
    def handle(self, text):
        t = text.lower().strip()

        if t in ("exit", "quit", "shutdown"):
            self.speak("Shutting down. Goodbye, sir.")
            return False

        if t.startswith("wikipedia "):
            self.wiki(t.replace("wikipedia ", ""))
            return True

        if "weather" in t:
            place = t.replace("weather", "").replace("in", "").strip()
            if place:
                self.weather(place)
            else:
                self.speak("Please specify a location, sir.")
            return True

        if t.startswith("open "):
            site = t.replace("open ", "")
            self.browser.open(
                "https://www.google.com/search?"
                + urllib.parse.urlencode({"q": site})
            )
            self.speak(f"Opening {site}, sir.")
            return True

        if self.system(t):
            return True

        # 🔥 EVERYTHING ELSE → CHATGPT-LEVEL AI
        self.ai(text)
        return True

    # ---------- LOOP ----------
    def run(self):
        self.speak("Jarvis online. Fully operational, sir.")
        while True:
            user = input("You: ")
            if not self.handle(user):
                break


# ---------------- RUN ----------------
if __name__ == "__main__":
    Jarvis().run()
