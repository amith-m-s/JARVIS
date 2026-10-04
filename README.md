# JARVIS AI

Local-first desktop assistant prototype built in Python.

## Features

- Text and voice input.
- Local text-to-speech with pyttsx3.
- Optional local LLM integration through Ollama.
- System statistics and application launching.
- Calculator with AST-based expression parsing.
- Weather/time and Wikipedia utilities.
- Persistent local memory.
- Modular command/tool structure.
- Automated tests for core tools.

## Architecture

~~~
input -> intent/router -> tool/service -> response
                    |
                    +-> local LLM (optional)
                    +-> system tools
                    +-> web information tools
~~~

## Important scope note

This is a **desktop automation/learning project**, not a general-purpose AI agent. Some capabilities depend on the local operating system and external services.

Runtime files such as .env, local memory, logs, and virtual environments are intentionally excluded from version control.

## Run

~~~
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
ollama pull llama3
python main.py
~~~

Tests:

~~~
python -m unittest discover -s tests
~~~
