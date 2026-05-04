from __future__ import annotations

from jarvis.core.intent import match_intent
from jarvis.core.memory import Memory
from jarvis.services.brain import LocalBrain
from jarvis.tools.base import ToolResult
from jarvis.tools.browser import BrowserTool
from jarvis.tools.calculator import CalculatorTool
from jarvis.tools.system import SystemTool
from jarvis.tools.time_tool import TimeTool
from jarvis.tools.weather import WeatherTool
from jarvis.tools.wiki import WikiTool
from jarvis.utils.parser import extract_topic, normalize_text


HELP_TEXT = (
    "I can help with weather, forecasts, web search, opening sites, opening apps, "
    "math, time, and general questions. "
    "Say things like: 'weather in Kochi', 'open YouTube', 'open calculator', "
    "'what is Instagram', or '2+2'."
)


class Assistant:
    def __init__(self):
        self.memory = Memory()
        self.brain = LocalBrain()

        self.weather = WeatherTool()
        self.browser = BrowserTool()
        self.system = SystemTool()
        self.calculator = CalculatorTool()
        self.time_tool = TimeTool()
        self.wiki = WikiTool()

    def _weather_followup(self, text: str) -> bool:
        if self.memory.last_tool != "weather":
            return False
        if not self.memory.is_recent(minutes=180):
            return False

        t = normalize_text(text)
        trigger_words = (
            "tomorrow",
            "today",
            "forecast",
            "rain",
            "raining",
            "temperature",
            "humidity",
            "chance of rain",
            "what about",
            "how about",
        )

        if any(word in t for word in trigger_words):
            return True

        if len(t.split()) <= 3 and not any(
            word in t
            for word in ("open", "what", "who", "why", "how", "tell", "define", "explain", "search")
        ):
            return True

        return False

    def run(self, raw_text: str) -> ToolResult:
        text = normalize_text(raw_text)
        if not text:
            return ToolResult("Say something.")

        if any(word in text for word in ("clear memory", "reset memory", "forget everything", "forget this")):
            self.memory.clear()
            return ToolResult("Memory cleared.")

        intent = match_intent(text)

        if intent == "knowledge" and self._weather_followup(text):
            intent = "weather"

        if intent == "help":
            return ToolResult(HELP_TEXT)

        if intent == "system" and any(word in text for word in ("exit", "quit", "shutdown", "close jarvis")):
            return ToolResult("Shutting down.", exit=True)

        if intent == "weather":
            result = self.weather.execute({"input": text, "memory": self.memory})
            self.memory.update(tool="weather", city=result.city)
            self.memory.add_turn(text, result.text)
            return result

        if intent == "browser":
            result = self.browser.execute({"input": text, "memory": self.memory})
            self.memory.update(tool="browser")
            self.memory.add_turn(text, result.text)
            return result

        if intent == "system":
            result = self.system.execute({"input": text, "memory": self.memory})
            self.memory.update(tool="system")
            self.memory.add_turn(text, result.text)
            return result

        if intent == "calculate":
            result = self.calculator.execute({"input": text, "memory": self.memory})
            self.memory.update(tool="calculate")
            self.memory.add_turn(text, result.text)
            return result

        if intent == "time":
            result = self.time_tool.execute({"input": text, "memory": self.memory})
            self.memory.update(tool="time")
            self.memory.add_turn(text, result.text)
            return result

        topic = extract_topic(text)

        brain_answer = self.brain.ask(text, self.memory)
        if brain_answer:
            self.memory.update(tool="knowledge", topic=topic or self.memory.last_topic)
            self.memory.add_turn(text, brain_answer)
            return ToolResult(brain_answer, topic=topic)

        wiki_result = self.wiki.execute({"input": text, "memory": self.memory})
        self.memory.update(tool="wiki", topic=wiki_result.topic or topic)
        self.memory.add_turn(text, wiki_result.text)

        if wiki_result.text == "Couldn't find anything.":
            return ToolResult(
                "I do not know yet. For richer general Q&A, install and run Ollama locally.",
                topic=topic,
            )

        return wiki_result
