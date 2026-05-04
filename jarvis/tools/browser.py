from __future__ import annotations

from urllib.parse import quote_plus
import webbrowser

from jarvis.tools.base import Tool, ToolResult
from jarvis.utils.parser import normalize_text


KNOWN_SITES = {
    "youtube": "https://www.youtube.com",
    "google": "https://www.google.com",
    "github": "https://github.com",
    "instagram": "https://www.instagram.com",
    "reddit": "https://www.reddit.com",
    "wikipedia": "https://www.wikipedia.org",
    "gmail": "https://mail.google.com",
    "stackoverflow": "https://stackoverflow.com",
    "stack overflow": "https://stackoverflow.com",
}


class BrowserTool(Tool):
    name = "browser"

    def execute(self, args):
        text = normalize_text(args["input"])

        if "browser" in text and not any(site in text for site in KNOWN_SITES):
            webbrowser.open("https://www.google.com")
            return ToolResult("Opening browser.")

        for site, url in KNOWN_SITES.items():
            if site in text:
                webbrowser.open(url)
                return ToolResult(f"Opening {site}.")

        query = text
        for prefix in ("open ", "launch ", "start ", "go to ", "visit ", "search ", "find "):
            if query.startswith(prefix):
                query = query[len(prefix) :]

        query = query.strip() or "google"
        webbrowser.open(f"https://www.google.com/search?q={quote_plus(query)}")
        return ToolResult(f"Searching {query}.")
