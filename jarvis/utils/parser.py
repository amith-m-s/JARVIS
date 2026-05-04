from __future__ import annotations

import re


WAKE_WORD_PATTERN = re.compile(r"^\s*jarvis[\s,:-]*", re.IGNORECASE)


def normalize_text(text: str) -> str:
    if not text:
        return ""
    text = text.strip().lower()
    text = WAKE_WORD_PATTERN.sub("", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def extract_city(text: str, fallback: str | None = None) -> str | None:
    t = normalize_text(text)

    preposition_patterns = [
        r"\b(?:in|at|for|of)\s+([a-zA-Z][a-zA-Z\s\-\.']+)$",
        r"^(?:weather|forecast|temperature|rain|raining|humidity|climate)\s+([a-zA-Z][a-zA-Z\s\-\.']+)$",
    ]

    for pattern in preposition_patterns:
        match = re.search(pattern, t)
        if match:
            candidate = match.group(1).strip()
            candidate = re.sub(r"\s+", " ", candidate)
            return candidate

    cleaned = re.sub(
        r"\b(weather|forecast|temperature|rain|raining|humidity|climate|is|it|going|to|be|what|about|tomorrow|today|how|much|chance|will|the)\b",
        " ",
        t,
    )
    cleaned = re.sub(r"[^a-zA-Z\s\-']", " ", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()

    if 1 <= len(cleaned.split()) <= 4:
        return cleaned

    return fallback


def extract_topic(text: str) -> str:
    t = normalize_text(text)

    t = re.sub(
        r"^(what is|who is|what are|who are|tell me about|tell me|tell about|explain|define|meaning of|about)\b",
        "",
        t,
    )
    t = re.sub(r"\b(is|are|was|were|the|a|an|of|to|for)\b", " ", t)
    t = re.sub(r"[^a-zA-Z0-9\s\-\+]", " ", t)
    t = re.sub(r"\s+", " ", t).strip()

    return t
MATH_ONLY = re.compile(r"^[\d\s\+\-\*\/\%\^\(\)\.]+$")

def looks_like_math(text: str) -> bool:
    t = normalize_text(text)

    # pure math like "2+2" or "(12/3)+4"
    if MATH_ONLY.fullmatch(t.replace("×", "*").replace("÷", "/").replace("^", "**")):
        return True

    # explicit math request with digits and an operator
    if any(k in t for k in ("calculate", "solve", "compute", "evaluate", "result of")):
        return bool(re.search(r"\d", t) and re.search(r"[\+\-\*\/%\^]", t))

    return False

def extract_expression(text: str) -> str:
    t = normalize_text(text).replace("×", "*").replace("÷", "/").replace("^", "**")

    # only extract if it actually looks like math
    if not looks_like_math(t):
        return ""

    expr = re.sub(r"[^0-9\+\-\*\/%\(\)\.\s\^]", " ", t)
    expr = re.sub(r"\s+", "", expr)
    return expr