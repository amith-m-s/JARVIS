from datetime import datetime

from jarvis.tools.base import Tool, ToolResult


class TimeTool(Tool):
    name = "time"

    def execute(self, args):
        now = datetime.now()
        return ToolResult(
            now.strftime("It is %I:%M %p on %A, %d %B %Y."),
        )
