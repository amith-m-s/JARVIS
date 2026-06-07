from __future__ import annotations

import requests

from jarvis.core.config import Config


SYSTEM_PROMPT = """You are JARVIS, a crisp, accurate, helpful assistant.
Answer naturally and clearly.
Use the provided context if it helps.
If the user asks a factual question, answer directly.
If the user asks a math question, solve it.
If you are unsure, say so honestly.
Keep answers short unless the user asks for detail."""


class LocalBrain:
    def ask(self, text: str, memory) -> str | None:
        context_lines = []

        if memory.last_city:
            context_lines.append(f"Weather context city: {memory.last_city}")
        if memory.last_topic:
            context_lines.append(f"Last topic: {memory.last_topic}")

        user_message = text
        if context_lines:
            user_message = "\n".join(context_lines) + "\n\nUser: " + text

        payload = {
            "model": Config.OLLAMA_MODEL,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                *memory.history[-12:],
                {"role": "user", "content": user_message},
            ],
            "stream": False,
            "options": {
                "temperature": 0.2,
            },
        }

        try:
            response = requests.post(
                f"{Config.OLLAMA_URL}/api/chat",
                json=payload,
                timeout=60,
            )
            if not response.ok:
                from jarvis.utils import logger
                logger.warning(
                    f"Ollama returned not ok status: {response.status_code}. "
                    f"Response: {response.text}. "
                    f"Ensure you have pulled the model '{Config.OLLAMA_MODEL}' using 'ollama pull {Config.OLLAMA_MODEL}'."
                )
                return None

            data = response.json()
            message = data.get("message", {})
            content = message.get("content", "").strip()
            return content or None
        except Exception as e:
            from jarvis.utils import logger
            logger.error(f"Ollama connection error: {e}", exc_info=True)
            return None
