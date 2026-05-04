# JARVIS AI

A **free, local-first AI assistant** built in Python with modular tools, hybrid input, persistent memory, and an optional local LLM brain via **Ollama**.

> Designed for offline-friendly usage, system automation, quick answers, and a scalable agent architecture.

---

## What it does

JARVIS AI supports:

- Voice input and text input
- Text-to-speech output
- Weather lookup
- Browser automation
- System app launching
- Calculator
- Time/date
- Wikipedia fallback
- Local AI responses through Ollama
- Short-term persistent memory

---

## Why this project exists

Most assistants depend on paid APIs or cloud-only intelligence. This project is built to stay:

- **Free**
- **Local-first**
- **Modular**
- **Easy to extend**
- **Production-minded**

---

## Current architecture

```text
jarvis-ai/
├── main.py
├── requirements.txt
├── .env
├── data/
├── tests/
└── jarvis/
    ├── core/
    │   ├── agent.py
    │   ├── config.py
    │   ├── intent.py
    │   └── memory.py
    ├── services/
    │   ├── brain.py
    │   ├── tts.py
    │   └── voice.py
    ├── tools/
    │   ├── browser.py
    │   ├── calculator.py
    │   ├── system.py
    │   ├── time_tool.py
    │   ├── weather.py
    │   └── wiki.py
    └── utils/
        ├── logger.py
        └── parser.py
```

---

## How it works

1. User speaks or types a message
2. Intent detection decides whether it is:
   - an action request
   - a math query
   - a weather request
   - a general knowledge question
3. JARVIS executes the matching tool
4. If no tool fits, it falls back to:
   - Ollama local LLM
   - Wikipedia if Ollama is unavailable
5. The result is spoken and printed
6. Memory is updated for follow-up context

---

## Features implemented

- Hybrid voice/text interaction
- Context memory for recent turns
- Weather lookup using `wttr.in`
- Web search and browser launch
- System app launching
- Wikipedia summaries
- Local AI via Ollama
- Simple intent hierarchy
- JSON-based persistent memory

---

## Setup

### 1) Create and activate a virtual environment

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

macOS/Linux:

```bash
source .venv/bin/activate
```

### 2) Install dependencies

```bash
pip install -r requirements.txt
```

If voice input is used, install PyAudio too:

```bash
pip install pyaudio
```

### 3) Install Ollama and pull a model

```bash
ollama pull llama3
```

If you prefer another local model, set it in `.env`.

### 4) Configure environment variables

Create a `.env` file:

```env
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=llama3
TTS_RATE=185
WAKE_WORD=jarvis
```

---

## Run

```bash
python main.py
```

---

## Notes on offline support

This project is designed to be local-first, but there is one important detail:

- **Ollama is local**
- **Weather uses a public free endpoint**
- **Voice input may still depend on an online recognizer unless replaced with a fully offline speech-to-text engine**

For fully offline voice input, replace the current speech recognition path with an offline STT stack such as Vosk or whisper.cpp.

---

## Project philosophy

JARVIS should behave like a real assistant, not just a collection of scripts.

That means:

- clean boundaries
- predictable tool execution
- graceful fallback
- local privacy
- easy extension
- strong reliability

---

## Author

Built as a local-first AI assistant project with modular Python architecture.
