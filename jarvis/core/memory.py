from __future__ import annotations

import json
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any


DATA_DIR = Path("data")
MEMORY_FILE = DATA_DIR / "memory.json"


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


class Memory:
    def __init__(self):
        self.last_tool: str | None = None
        self.last_city: str | None = None
        self.last_topic: str | None = None
        self.last_update: str | None = None
        self.history: list[dict[str, Any]] = []
        self._load()

    def _load(self) -> None:
        if not MEMORY_FILE.exists():
            return

        try:
            data = json.loads(MEMORY_FILE.read_text(encoding="utf-8"))
            self.last_tool = data.get("last_tool")
            self.last_city = data.get("last_city")
            self.last_topic = data.get("last_topic")
            self.last_update = data.get("last_update")
            self.history = data.get("history", [])
        except Exception:
            pass

    def save(self) -> None:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        payload = {
            "last_tool": self.last_tool,
            "last_city": self.last_city,
            "last_topic": self.last_topic,
            "last_update": self.last_update,
            "history": self.history[-16:],
        }
        MEMORY_FILE.write_text(
            json.dumps(payload, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

    def update(
        self,
        tool: str | None = None,
        city: str | None = None,
        topic: str | None = None,
    ) -> None:
        if tool is not None:
            self.last_tool = tool
        if city is not None:
            self.last_city = city
        if topic is not None:
            self.last_topic = topic
        self.last_update = utc_now_iso()
        self.save()

    def add_turn(self, user_text: str, assistant_text: str) -> None:
        self.history.append({"role": "user", "content": user_text})
        self.history.append({"role": "assistant", "content": assistant_text})
        self.history = self.history[-16:]
        self.last_update = utc_now_iso()
        self.save()

    def clear(self) -> None:
        self.last_tool = None
        self.last_city = None
        self.last_topic = None
        self.last_update = utc_now_iso()
        self.history = []
        self.save()

    def is_recent(self, minutes: int = 60) -> bool:
        if not self.last_update:
            return False
        try:
            ts = datetime.fromisoformat(self.last_update)
            return datetime.now(timezone.utc) - ts <= timedelta(minutes=minutes)
        except Exception:
            return False
