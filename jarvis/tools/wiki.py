from __future__ import annotations

import wikipedia

from jarvis.tools.base import Tool, ToolResult
from jarvis.utils.parser import extract_topic

wikipedia.set_lang("en")


class WikiTool(Tool):
    name = "wiki"

    def execute(self, args):
        text = args["input"]
        topic = extract_topic(text) or text

        try:
            summary = wikipedia.summary(topic, sentences=2, auto_suggest=True, redirect=True)
            return ToolResult(summary, topic=topic)
        except wikipedia.DisambiguationError as e:
            choices = ", ".join(e.options[:5])
            return ToolResult(f"{topic} is ambiguous. Try: {choices}", topic=topic)
        except Exception:
            return ToolResult("Couldn't find anything.", topic=topic)
