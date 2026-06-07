from __future__ import annotations

import re
from datetime import datetime
from zoneinfo import ZoneInfo

from jarvis.tools.base import Tool, ToolResult
from jarvis.utils.parser import normalize_text

CITIES_TZ = {
    "london": "Europe/London",
    "tokyo": "Asia/Tokyo",
    "new york": "America/New_York",
    "newyork": "America/New_York",
    "los angeles": "America/Los_Angeles",
    "losangeles": "America/Los_Angeles",
    "chicago": "America/Chicago",
    "paris": "Europe/Paris",
    "berlin": "Europe/Berlin",
    "sydney": "Australia/Sydney",
    "singapore": "Asia/Singapore",
    "dubai": "Asia/Dubai",
    "mumbai": "Asia/Kolkata",
    "kolkata": "Asia/Kolkata",
    "delhi": "Asia/Kolkata",
    "new delhi": "Asia/Kolkata",
    "moscow": "Europe/Moscow",
    "beijing": "Asia/Shanghai",
    "shanghai": "Asia/Shanghai",
    "toronto": "America/Toronto",
    "seoul": "Asia/Seoul",
    "cape town": "Africa/Johannesburg",
    "capetown": "Africa/Johannesburg",
    "johannesburg": "Africa/Johannesburg",
    "nairobi": "Africa/Nairobi",
    "cairo": "Africa/Cairo",
    "sao paulo": "America/Sao_Paulo",
    "saopaulo": "America/Sao_Paulo",
    "buenos aires": "America/Argentina/Buenos_Aires",
    "gmt": "Etc/GMT",
    "utc": "Etc/UTC",
    "ist": "Asia/Kolkata",
    "est": "America/New_York",
    "pst": "America/Los_Angeles",
    "cst": "America/Chicago",
    "mst": "America/Denver",
}


class TimeTool(Tool):
    name = "time"

    def execute(self, args):
        text = normalize_text(args["input"])

        found_zones = []

        # 1. Look for literal timezone pattern (e.g. Europe/London)
        tz_pattern = re.compile(r"\b[a-zA-Z_]+/[a-zA-Z_]+(?:/[a-zA-Z_]+)?\b")
        matches = tz_pattern.findall(text)
        for match in matches:
            try:
                ZoneInfo(match)  # Test if valid
                found_zones.append((match, match))
            except Exception:
                pass

        # 2. Look for cities/aliases in text
        for city, tz_key in CITIES_TZ.items():
            if re.search(rf"\b{city}\b", text):
                if not any(z[1] == tz_key for z in found_zones):
                    found_zones.append((city, tz_key))

        if len(found_zones) >= 2:
            city1, tz1 = found_zones[0]
            city2, tz2 = found_zones[1]
            try:
                t1 = datetime.now(ZoneInfo(tz1))
                t2 = datetime.now(ZoneInfo(tz2))
                diff_seconds = t1.utcoffset().total_seconds() - t2.utcoffset().total_seconds()
                diff_hours = diff_seconds / 3600.0

                c1_formatted = city1.title()
                c2_formatted = city2.title()

                abs_diff = abs(diff_hours)
                diff_str = f"{abs_diff:g} hours" if abs_diff.is_integer() else f"{abs_diff:.1f} hours"

                if diff_hours > 0:
                    relation = "ahead of"
                elif diff_hours < 0:
                    relation = "behind"
                else:
                    relation = "at the same time as"

                output = (
                    f"{c1_formatted} is {diff_str} {relation} {c2_formatted}. "
                    f"Current time: {c1_formatted} ({t1.strftime('%I:%M %p')}), "
                    f"{c2_formatted} ({t2.strftime('%I:%M %p')})."
                )
                return ToolResult(output)
            except Exception as e:
                return ToolResult(f"Failed to calculate time difference: {str(e)}")

        elif len(found_zones) == 1:
            city, tz = found_zones[0]
            try:
                now = datetime.now(ZoneInfo(tz))
                return ToolResult(
                    now.strftime(f"In {city.title()}, it is %I:%M %p on %A, %d %B %Y (Timezone: {tz}).")
                )
            except Exception as e:
                return ToolResult(f"Could not load time for {city.title()}: {str(e)}")

        # Fallback to local system time
        now = datetime.now()
        return ToolResult(
            now.strftime("It is %I:%M %p on %A, %d %B %Y (local system time)."),
        )

