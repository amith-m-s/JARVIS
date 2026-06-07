from __future__ import annotations

import re

from jarvis.utils.parser import extract_expression, normalize_text


HELP_WORDS = ("help", "what can you do", "commands", "capabilities")
EXIT_WORDS = ("exit", "quit", "shutdown", "close jarvis", "goodbye")
TIME_WORDS = ("time", "date", "day", "clock")
WEATHER_WORDS = (
    "weather",
    "forecast",
    "temperature",
    "rain",
    "raining",
    "humidity",
    "climate",
    "tomorrow",
)
QUESTION_WORDS = ("what is", "who is", "what are", "who are", "why", "how", "explain", "define", "tell me", "tell about")
ACTION_WORDS = ("open", "launch", "start", "go to", "visit", "search", "find", "run")
APP_WORDS = ("calculator", "calc", "notepad", "editor", "explorer", "file explorer", "browser", "terminal", "cmd", "settings")
SITE_WORDS = ("youtube", "google", "github", "instagram", "reddit", "wikipedia", "gmail", "stackoverflow", "stack overflow")
SYSTEM_WORDS = ("cpu", "ram", "memory", "system usage", "system stats", "hardware", "system status", "status")


def contains_word(text: str, words: tuple[str, ...]) -> bool:
    pattern = rf"\b({'|'.join(re.escape(w) for w in words)})\b"
    return bool(re.search(pattern, text, re.IGNORECASE))


def looks_like_math(text: str) -> bool:
    expr = extract_expression(text)
    if not expr:
        return False
    has_digit = any(ch.isdigit() for ch in expr)
    has_operator = any(op in expr for op in "+-*/%")
    has_math_func = any(func in expr for func in ("sin", "cos", "tan", "sqrt", "log", "exp", "pi", "e"))
    return has_digit and (has_operator or has_math_func)


def match_intent(text: str) -> str:
    t = normalize_text(text)

    if contains_word(t, HELP_WORDS):
        return "help"

    if contains_word(t, EXIT_WORDS):
        return "system"

    if contains_word(t, SYSTEM_WORDS):
        return "system"

    if looks_like_math(t):
        return "calculate"

    if contains_word(t, WEATHER_WORDS):
        return "weather"

    if contains_word(t, TIME_WORDS):
        return "time"

    if contains_word(t, QUESTION_WORDS) or t.endswith("?"):
        return "knowledge"

    if contains_word(t, ACTION_WORDS):
        if contains_word(t, APP_WORDS):
            return "system"
        if contains_word(t, SITE_WORDS):
            return "browser"
        if "browser" in t:
            return "system"
        return "browser"

    if contains_word(t, SITE_WORDS):
        return "browser"

    if re.fullmatch(r"[a-zA-Z][a-zA-Z\s\-']{1,40}", t):
        return "knowledge"

    return "knowledge"

