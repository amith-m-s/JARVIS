from __future__ import annotations

import re
from jarvis.utils import logger

WAKE_WORD_PATTERN = re.compile(r"^\s*(?:hey\s+)?jarvis[\s,:-]*", re.IGNORECASE)
FILLER_PATTERN = re.compile(r"\b(please|can you|could you|would you mind)\b", re.IGNORECASE)


def normalize_text(text: str) -> str:
    if not isinstance(text, str):
        return ""

    if len(text) > 1000:
        text = text[:1000]
        logger.warning("Input text truncated due to length > 1000 characters.")

    try:
        text = text.strip().lower()
        text = WAKE_WORD_PATTERN.sub("", text)
        text = FILLER_PATTERN.sub("", text)
        text = re.sub(r"\s+", " ", text)
        return text.strip()
    except Exception as e:
        logger.error(f"Error normalizing text: {e}", exc_info=True)
        return ""


def extract_city(text: str, fallback: str | None = None) -> str | None:
    if not isinstance(text, str):
        return fallback

    try:
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
    except Exception as e:
        logger.error(f"Error extracting city: {e}", exc_info=True)
        return fallback


def extract_topic(text: str) -> str:
    if not isinstance(text, str):
        return ""

    try:
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
    except Exception as e:
        logger.error(f"Error extracting topic: {e}", exc_info=True)
        return ""


MATH_ONLY = re.compile(r"^[\d\s\+\-\*\/\%\^\(\)\.a-zA-Z]+$")
MATH_FUNCS = {"sin", "cos", "tan", "sqrt", "log", "log10", "exp", "radians", "degrees", "pi", "e"}


def looks_like_math(text: str) -> bool:
    if not isinstance(text, str):
        return False

    try:
        t = normalize_text(text)

        # Strip math prefixes first
        for prefix in ("calculate ", "solve ", "compute ", "evaluate ", "result of "):
            if t.startswith(prefix):
                t = t[len(prefix):]

        cleaned = t.replace("×", "*").replace("÷", "/").replace("^", "**")

        # Tokenize to identify words, numbers, and symbols
        tokens = re.findall(r"[a-zA-Z]+|\d+|[^\w\s]", cleaned)
        if not tokens:
            return False

        letter_tokens = [tok for tok in tokens if tok.isalpha()]

        if letter_tokens:
            return all(tok in MATH_FUNCS for tok in letter_tokens)

        # If no letters exist, check if there are digits and operators
        has_digit = any(tok.isdigit() for tok in tokens)
        has_operator = any(tok in "+-*/%" for tok in tokens)
        return has_digit and has_operator
    except Exception as e:
        logger.error(f"Error in looks_like_math check: {e}", exc_info=True)
        return False


def extract_expression(text: str) -> str:
    if not isinstance(text, str):
        return ""

    try:
        t = normalize_text(text).replace("×", "*").replace("÷", "/").replace("^", "**")

        for prefix in ("calculate ", "solve ", "compute ", "evaluate ", "result of "):
            if t.startswith(prefix):
                t = t[len(prefix):]

        if not looks_like_math(t):
            return ""

        expr = re.sub(r"[^a-zA-Z0-9\+\-\*\/%\(\)\.\s\^]", " ", t)
        expr = re.sub(r"\s+", "", expr)
        return expr
    except Exception as e:
        logger.error(f"Error extracting math expression: {e}", exc_info=True)
        return ""