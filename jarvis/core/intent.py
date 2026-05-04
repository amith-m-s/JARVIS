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


def looks_like_math(text: str) -> bool:
    expr = extract_expression(text)
    return bool(expr) and any(ch.isdigit() for ch in expr) and any(op in expr for op in "+-*/%")


def match_intent(text: str) -> str:
    t = normalize_text(text)

    if any(word in t for word in HELP_WORDS):
        return "help"

    if any(word in t for word in EXIT_WORDS):
        return "system"

    if looks_like_math(t):
        return "calculate"

    if any(word in t for word in WEATHER_WORDS):
        return "weather"

    if any(word in t for word in TIME_WORDS):
        return "time"

    if any(q in t for q in QUESTION_WORDS) or t.endswith("?"):
        return "knowledge"

    if any(a in t for a in ACTION_WORDS):
        if any(app in t for app in APP_WORDS):
            return "system"
        if any(site in t for site in SITE_WORDS):
            return "browser"
        if "browser" in t:
            return "system"
        return "browser"

    if any(site in t for site in SITE_WORDS):
        return "browser"

    if re.fullmatch(r"[a-zA-Z][a-zA-Z\s\-']{1,40}", t):
        return "knowledge"

    return "knowledge"
