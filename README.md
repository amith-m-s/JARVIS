# JARVIS AI

A **free, local-first AI assistant** built in Python with modular tools, hybrid input, persistent memory, and an optional local LLM brain via **Ollama**.

> Designed for offline-friendly usage, system automation, quick answers, and a scalable agent architecture.

---

## What it does

JARVIS AI supports:

- **Graphical User Interface (GUI)**: A sleek, dark-themed dashboard built with Tkinter using asynchronous threading to keep operations responsive.
- **Voice input and text input**: Direct microphone input or text console/GUI entries.
- **Text-to-speech output**: Local voice synthesis using `pyttsx3`.
- **System stats monitoring**: Local CPU load, RAM utilization, and disk capacity metrics using `psutil`.
- **Advanced math calculation**: Safe AST-based parsing supporting basic arithmetic, constants (`pi`, `e`), and functions like `sin`, `cos`, `sqrt`, `log`, etc.
- **Timezone & Time Differences**: Lookup current time in specific cities or compute time differences between different parts of the world.
- **Weather lookup**: Real-time reports and tomorrow's forecast using `wttr.in`.
- **Browser automation**: Open known websites and perform custom web searches.
- **System app launching**: Open notepad, calculator, and file explorer.
- **Wikipedia fallback**: Robust MediaWiki API client retrieving intro summaries.
- **Local AI responses**: Connects to your local Ollama server.
- **Persistent memory**: Track context, topics, and cities across interactions.

---

## Project Structure

```text
jarvis-ai/
├── main.py
├── requirements.txt
├── .env
├── data/
│   ├── memory.json
│   └── jarvis.log
├── tests/
│   └── test_tools.py
└── jarvis/
    ├── core/
    │   ├── agent.py
    │   ├── config.py
    │   ├── intent.py
    │   └── memory.py
    ├── services/
    │   ├── brain.py
    │   ├── gui.py
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

Create a `.env` file in the root directory:

```env
OLLAMA_URL=http://127.0.0.1:11434
OLLAMA_MODEL=llama3
TTS_RATE=185
WAKE_WORD=jarvis
```
*(Note: Using `127.0.0.1` instead of `localhost` is recommended to prevent DNS resolution latency or failures in multi-threaded GUI operations on Windows).*

---

## Run

To launch the assistant, run the main entry point:

```bash
python main.py
```

You will be prompted to choose an interaction mode:
1. **Voice**: Interactive hands-free voice control.
2. **Text**: Quick terminal command-line prompt.
3. **Hybrid**: Prompting choice between typing or speaking for each turn.
4. **GUI Dashboard**: Sleek, threaded desktop window dashboard.

---

## Running Automated Tests

A comprehensive unit test suite is provided. To execute the tests:

```bash
python -m unittest discover -s tests
```

---

## Project philosophy

JARVIS should behave like a real assistant, not just a collection of scripts. That means:
- Clean boundaries and modularity
- Predictable tool execution
- Robust fallback strategies
- Local privacy and offline-friendly features
- Threaded GUI performance to ensure zero lockups
- Standard logging for traceback records in `data/jarvis.log`

