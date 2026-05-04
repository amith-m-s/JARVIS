from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class ToolResult:
    text: str
    city: Optional[str] = None
    topic: Optional[str] = None
    exit: bool = False
    extra: dict[str, Any] = field(default_factory=dict)


class Tool:
    name = "tool"

    def execute(self, args: dict[str, Any]) -> ToolResult:
        raise NotImplementedError
