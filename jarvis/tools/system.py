from __future__ import annotations

import os
import platform
import subprocess
import webbrowser

from jarvis.tools.base import Tool, ToolResult
from jarvis.utils.parser import normalize_text


class SystemTool(Tool):
    name = "system"

    def execute(self, args):
        text = normalize_text(args["input"])
        system_name = platform.system().lower()

        try:
            if "calculator" in text or "calc" in text:
                if system_name == "windows":
                    subprocess.Popen(["calc"])
                elif system_name == "darwin":
                    subprocess.Popen(["open", "-a", "Calculator"])
                else:
                    subprocess.Popen(["gnome-calculator"])
                return ToolResult("Opening calculator.")

            if "notepad" in text or "editor" in text:
                if system_name == "windows":
                    subprocess.Popen(["notepad"])
                elif system_name == "darwin":
                    subprocess.Popen(["open", "-a", "TextEdit"])
                else:
                    subprocess.Popen(["gedit"])
                return ToolResult("Opening notepad.")

            if "explorer" in text or "file manager" in text or "files" in text:
                if system_name == "windows":
                    os.startfile(os.getcwd())
                elif system_name == "darwin":
                    subprocess.Popen(["open", "."])
                else:
                    subprocess.Popen(["xdg-open", os.getcwd()])
                return ToolResult("Opening file explorer.")

            if "browser" in text:
                webbrowser.open("https://www.google.com")
                return ToolResult("Opening browser.")

            return ToolResult("That app is not supported yet.")
        except Exception:
            return ToolResult("I could not open that app on this system.")
