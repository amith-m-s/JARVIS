import unittest
import os
import sys

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from jarvis.utils.parser import normalize_text, extract_city, looks_like_math, extract_expression
from jarvis.tools.calculator import CalculatorTool
from jarvis.tools.time_tool import TimeTool
from jarvis.tools.system import SystemTool
from jarvis.core.memory import Memory
from jarvis.core.intent import match_intent


class TestJarvisParser(unittest.TestCase):
    def test_normalize_text(self):
        self.assertEqual(normalize_text("hey jarvis, do something"), "do something")
        self.assertEqual(normalize_text("jarvis: check weather"), "check weather")
        self.assertEqual(normalize_text("please open google"), "open google")
        self.assertEqual(normalize_text("   "), "")
        self.assertEqual(normalize_text(None), "")
        self.assertEqual(normalize_text("A" * 1200), "a" * 1000)

    def test_extract_city(self):
        self.assertEqual(extract_city("weather in Tokyo"), "tokyo")
        self.assertEqual(extract_city("forecast for New York"), "new york")
        self.assertEqual(extract_city("climate of Paris"), "paris")
        self.assertEqual(extract_city("temperature in Cape Town"), "cape town")
        self.assertEqual(extract_city("random text"), "random text")
        self.assertEqual(extract_city("random text that has many words"), None)

    def test_looks_like_math(self):
        self.assertTrue(looks_like_math("2+2"))
        self.assertTrue(looks_like_math("sqrt(16)"))
        self.assertTrue(looks_like_math("calculate sin(pi/2)"))
        self.assertFalse(looks_like_math("what is the weather in Tokyo"))

    def test_extract_expression(self):
        self.assertEqual(extract_expression("calculate 2+2"), "2+2")
        self.assertEqual(extract_expression("solve sin(pi/2)"), "sin(pi/2)")
        self.assertEqual(extract_expression("random text"), "")


class TestJarvisTools(unittest.TestCase):
    def setUp(self):
        self.memory = Memory()

    def test_calculator_tool(self):
        calc = CalculatorTool()
        # Basic arithmetic
        res = calc.execute({"input": "2+2", "memory": self.memory})
        self.assertEqual(res.text, "4")
        # Functions and constants
        res = calc.execute({"input": "sqrt(25)", "memory": self.memory})
        self.assertEqual(res.text, "5")
        res = calc.execute({"input": "sin(pi/2)", "memory": self.memory})
        self.assertEqual(res.text, "1")
        # Error cases
        res = calc.execute({"input": "unknown(25)", "memory": self.memory})
        self.assertEqual(res.text, "That does not look like a math expression.")
        res = calc.execute({"input": "1/0", "memory": self.memory})
        self.assertEqual(res.text, "Division by zero is not allowed.")

    def test_time_tool(self):
        time_tool = TimeTool()
        # Single timezone query
        res = time_tool.execute({"input": "time in New York", "memory": self.memory})
        self.assertIn("America/New_York", res.text)

        # Time difference query
        res = time_tool.execute({"input": "time difference between Tokyo and New York", "memory": self.memory})
        self.assertIn("Tokyo is 13 hours ahead of New York", res.text)

    def test_system_tool(self):
        system = SystemTool()
        # Hardware stats query
        res = system.execute({"input": "cpu usage", "memory": self.memory})
        self.assertIn("System Status:", res.text)
        self.assertIn("CPU Usage:", res.text)
        self.assertIn("RAM Usage:", res.text)

class TestJarvisIntent(unittest.TestCase):
    def test_match_intent(self):
        # Verify that "instagram" does not trigger "system" intent due to "ram" substring matching
        self.assertEqual(match_intent("what is instagram"), "knowledge")
        self.assertEqual(match_intent("samsung"), "knowledge")
        
        # Verify valid system triggers match correctly
        self.assertEqual(match_intent("cpu usage"), "system")
        self.assertEqual(match_intent("ram status"), "system")
        self.assertEqual(match_intent("system stats"), "system")


if __name__ == "__main__":
    unittest.main()
