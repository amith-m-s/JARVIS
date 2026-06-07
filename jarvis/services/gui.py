from __future__ import annotations

import threading
import tkinter as tk
from tkinter import scrolledtext

from jarvis.core.agent import Assistant
from jarvis.services.tts import Speaker
from jarvis.services.voice import VoiceInput
from jarvis.utils.parser import normalize_text


class JarvisGUI:
    def __init__(self, root: tk.Tk, assistant: Assistant, speaker: Speaker, voice: VoiceInput):
        self.root = root
        self.assistant = assistant
        self.speaker = speaker
        self.voice = voice

        # Window styling
        self.root.title("JARVIS AI - Dashboard")
        self.root.geometry("600x700")
        self.root.configure(bg="#121212")

        # Layout grids
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)

        # Scrolled Text Box for Chat Output
        self.chat_history = scrolledtext.ScrolledText(
            self.root,
            state="disabled",
            wrap="word",
            bg="#1e1e1e",
            fg="#e0e0e0",
            insertbackground="white",
            font=("Consolas", 10),
            padx=10,
            pady=10,
            borderwidth=0,
            highlightthickness=0,
        )
        self.chat_history.grid(row=0, column=0, columnspan=2, padx=15, pady=15, sticky="nsew")

        # Color tags
        self.chat_history.tag_config("user", foreground="#81c784", font=("Consolas", 10, "bold"))
        self.chat_history.tag_config("jarvis", foreground="#64b5f6", font=("Consolas", 10, "bold"))
        self.chat_history.tag_config("system", foreground="#90a4ae", font=("Consolas", 10, "italic"))

        # Input Entry Frame
        self.input_frame = tk.Frame(self.root, bg="#121212")
        self.input_frame.grid(row=1, column=0, columnspan=2, padx=15, pady=(0, 15), sticky="ew")
        self.input_frame.columnconfigure(0, weight=1)

        # Input Entry Field
        self.input_field = tk.Entry(
            self.input_frame,
            bg="#212121",
            fg="#ffffff",
            insertbackground="white",
            font=("Arial", 11),
            borderwidth=1,
            relief="solid",
            highlightbackground="#37474f",
            highlightcolor="#64b5f6",
        )
        self.input_field.grid(row=0, column=0, padx=(0, 10), ipady=8, sticky="ew")
        self.input_field.bind("<Return>", lambda event: self.send_text_message())

        # Buttons Frame
        self.btn_frame = tk.Frame(self.input_frame, bg="#121212")
        self.btn_frame.grid(row=0, column=1, sticky="ew")

        # Send Button
        self.send_btn = tk.Button(
            self.btn_frame,
            text="Send",
            command=self.send_text_message,
            bg="#1976d2",
            fg="white",
            font=("Arial", 9, "bold"),
            relief="flat",
            activebackground="#1565c0",
            activeforeground="white",
            padx=15,
            pady=6,
        )
        self.send_btn.pack(side="left", padx=3)

        # Voice Button
        self.voice_btn = tk.Button(
            self.btn_frame,
            text="🎤 Listen",
            command=self.start_voice_thread,
            bg="#2e7d32",
            fg="white",
            font=("Arial", 9, "bold"),
            relief="flat",
            activebackground="#1b5e20",
            activeforeground="white",
            padx=15,
            pady=6,
        )
        self.voice_btn.pack(side="left", padx=3)

        # Welcome output
        self.append_message("System", "JARVIS Dashboard initialized. Ready for command.")

    def append_message(self, sender: str, text: str):
        self.chat_history.configure(state="normal")
        if sender == "You":
            self.chat_history.insert(tk.END, f"\nYou: {text}\n", "user")
        elif sender == "JARVIS":
            self.chat_history.insert(tk.END, f"\nJARVIS: {text}\n", "jarvis")
        else:
            self.chat_history.insert(tk.END, f"\n[{sender}]: {text}\n", "system")
        self.chat_history.configure(state="disabled")
        self.chat_history.see(tk.END)

    def send_text_message(self):
        query = self.input_field.get().strip()
        if not query:
            return
        self.input_field.delete(0, tk.END)
        self.append_message("You", query)

        # Process the query in a background thread to prevent UI freezing
        threading.Thread(target=self.process_query, args=(query,), daemon=True).start()

    def start_voice_thread(self):
        if not self.voice.enabled:
            self.append_message("System", "Voice capture is disabled or missing pyaudio dependencies.")
            return

        self.voice_btn.configure(state="disabled", text="Listening...", bg="#d32f2f")
        threading.Thread(target=self.listen_voice, daemon=True).start()

    def listen_voice(self):
        heard = self.voice.listen()
        self.root.after(0, self.reset_voice_button)
        if heard:
            self.root.after(0, lambda: self.append_message("You", f"{heard} (voice)"))
            self.process_query(heard)
        else:
            self.root.after(0, lambda: self.append_message("System", "Speech was not recognized or timed out."))

    def reset_voice_button(self):
        self.voice_btn.configure(state="normal", text="🎤 Listen", bg="#2e7d32")

    def process_query(self, query: str):
        text = normalize_text(query)
        if not text:
            return

        result = self.assistant.run(text)
        self.root.after(0, lambda: self.append_message("JARVIS", result.text))

        # Speak result in background thread
        self.speaker.say(result.text)

        if result.exit:
            self.root.after(1500, self.root.destroy)
