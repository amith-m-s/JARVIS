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
            # Check for system status / hardware metrics
            if any(word in text for word in ("cpu", "ram", "memory", "usage", "hardware", "stats", "status")):
                import psutil
                cpu = psutil.cpu_percent(interval=0.1)
                mem = psutil.virtual_memory()
                drive = os.path.splitdrive(os.getcwd())[0] or "C:"
                disk = psutil.disk_usage(drive + "\\")

                mem_total = mem.total / (1024**3)
                mem_used = mem.used / (1024**3)
                disk_total = disk.total / (1024**3)
                disk_used = disk.used / (1024**3)

                status_text = (
                    f"System Status:\n"
                    f"  - CPU Usage: {cpu}%\n"
                    f"  - RAM Usage: {mem.percent}% ({mem_used:.1f} GB of {mem_total:.1f} GB used)\n"
                    f"  - Disk ({drive}): {disk.percent}% ({disk_used:.1f} GB of {disk_total:.1f} GB used)"
                )
                return ToolResult(status_text)

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
