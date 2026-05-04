from __future__ import annotations

import requests
from urllib.parse import quote

from jarvis.tools.base import Tool, ToolResult
from jarvis.utils.parser import extract_city


def weather_emoji(desc: str) -> str:
    d = desc.lower()
    if any(w in d for w in ["thunder", "storm"]):
        return "⛈"
    if any(w in d for w in ["rain", "drizzle", "shower"]):
        return "🌧"
    if any(w in d for w in ["snow", "sleet", "blizzard"]):
        return "❄️"
    if any(w in d for w in ["fog", "mist", "haze", "smoke"]):
        return "🌫"
    if any(w in d for w in ["cloud", "overcast"]):
        return "☁️"
    if any(w in d for w in ["sun", "clear", "bright"]):
        return "☀️"
    if "partly" in d:
        return "⛅"
    return "🌡"


class WeatherTool(Tool):
    name = "weather"

    def execute(self, args):
        text = args["input"]
        memory = args["memory"]

        city = extract_city(text, fallback=memory.last_city)
        if not city:
            return ToolResult("Tell me a city.", city=None)

        try:
            url = f"https://wttr.in/{quote(city)}?format=j1"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()

            is_forecast = any(
                word in text.lower()
                for word in ["tomorrow", "forecast", "next day", "next"]
            )

            if is_forecast:
                days = data.get("weather", [])
                day = days[1] if len(days) > 1 else days[0]
                hourly = day.get("hourly", [])
                desc = "Clear"
                if hourly:
                    middle = hourly[min(len(hourly) - 1, 4)]
                    desc = middle.get("weatherDesc", [{"value": "Clear"}])[0]["value"]

                lo = day.get("mintempC", "?")
                hi = day.get("maxtempC", "?")
                emoji = weather_emoji(desc)
                return ToolResult(
                    f"Tomorrow in {city}: {emoji} {desc}, {lo}°C to {hi}°C.",
                    city=city,
                )

            current = data["current_condition"][0]
            desc = current["weatherDesc"][0]["value"]
            temp = current["temp_C"]
            feels = current["FeelsLikeC"]
            hum = current["humidity"]
            emoji = weather_emoji(desc)

            return ToolResult(
                f"{city}: {emoji} {temp}°C (feels like {feels}°C, humidity {hum}%, {desc.lower()}).",
                city=city,
            )
        except Exception:
            return ToolResult(f"Weather data source not available for {city}.", city=city)
