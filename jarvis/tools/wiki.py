from __future__ import annotations

import requests

from jarvis.tools.base import Tool, ToolResult
from jarvis.utils.parser import extract_topic


class WikiTool(Tool):
    name = "wiki"

    def execute(self, args):
        text = args["input"]
        topic = extract_topic(text) or text

        headers = {
            "User-Agent": "JarvisAssistant/1.0 (contact: local-assistant@example.com)"
        }
        url = "https://en.wikipedia.org/w/api.php"

        try:
            # 1. Search for best matching page title
            search_params = {
                "action": "opensearch",
                "format": "json",
                "search": topic,
                "limit": 1,
            }
            search_res = requests.get(url, params=search_params, headers=headers, timeout=10)
            search_res.raise_for_status()
            search_data = search_res.json()

            if not (len(search_data) > 1 and search_data[1]):
                return ToolResult("Couldn't find anything.", topic=topic)

            best_title = search_data[1][0]

            # 2. Get introductory extract
            query_params = {
                "action": "query",
                "format": "json",
                "prop": "extracts",
                "exintro": True,
                "explaintext": True,
                "exsentences": 2,
                "titles": best_title,
                "redirects": 1,
            }
            query_res = requests.get(url, params=query_params, headers=headers, timeout=10)
            query_res.raise_for_status()
            query_data = query_res.json()

            pages = query_data.get("query", {}).get("pages", {})
            for page_id, page_data in pages.items():
                if page_id == "-1":
                    continue
                extract = page_data.get("extract", "").strip()
                if extract:
                    return ToolResult(extract, topic=best_title)

            return ToolResult("Couldn't find anything.", topic=topic)

        except Exception as e:
            from jarvis.utils import logger
            logger.error(f"Wikipedia search error: {e}", exc_info=True)
            return ToolResult("Couldn't find anything.", topic=topic)

