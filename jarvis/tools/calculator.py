from __future__ import annotations

import ast
import math
import operator as op
import re

from jarvis.tools.base import Tool, ToolResult
from jarvis.utils.parser import looks_like_math, extract_expression



# =========================
# Allowed operators
# =========================

_ALLOWED_OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Mod: op.mod,
    ast.Pow: op.pow,
    ast.FloorDiv: op.floordiv,
    ast.UAdd: op.pos,
    ast.USub: op.neg,
}


# =========================
# Supported math functions
# =========================

_MATH_FUNCTIONS = {
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "asin": math.asin,
    "acos": math.acos,
    "atan": math.atan,

    "sinh": math.sinh,
    "cosh": math.cosh,
    "tanh": math.tanh,

    "sqrt": math.sqrt,
    "cbrt": lambda x: x ** (1 / 3),

    "log": math.log,
    "log10": math.log10,
    "log2": math.log2,

    "exp": math.exp,

    "ceil": math.ceil,
    "floor": math.floor,
    "fabs": math.fabs,

    "factorial": math.factorial,

    "degrees": math.degrees,
    "radians": math.radians,

    "abs": abs,
    "round": round,

    "min": min,
    "max": max,
    "sum": sum,
}


# =========================
# Supported constants
# =========================

_MATH_CONSTANTS = {
    "pi": math.pi,
    "e": math.e,
    "tau": math.tau,
    "inf": math.inf,
}





# =========================
# Safe AST evaluator
# =========================

def safe_eval(node):
    # numbers
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Invalid constant")

    # compatibility
    if isinstance(node, ast.Num):
        return node.n

    # binary operators
    if isinstance(node, ast.BinOp):

        if type(node.op) not in _ALLOWED_OPERATORS:
            raise ValueError("Operator not allowed")

        left = safe_eval(node.left)
        right = safe_eval(node.right)

        return _ALLOWED_OPERATORS[type(node.op)](left, right)

    # unary operators
    if isinstance(node, ast.UnaryOp):

        if type(node.op) not in _ALLOWED_OPERATORS:
            raise ValueError("Unary operator not allowed")

        operand = safe_eval(node.operand)

        return _ALLOWED_OPERATORS[type(node.op)](operand)

    # constants
    if isinstance(node, ast.Name):

        if node.id in _MATH_CONSTANTS:
            return _MATH_CONSTANTS[node.id]

        raise ValueError(f"Unknown variable: {node.id}")

    # function calls
    if isinstance(node, ast.Call):

        if not isinstance(node.func, ast.Name):
            raise ValueError("Invalid function")

        func_name = node.func.id

        if func_name not in _MATH_FUNCTIONS:
            raise ValueError(f"Unknown function: {func_name}")

        func = _MATH_FUNCTIONS[func_name]

        args = [safe_eval(arg) for arg in node.args]

        return func(*args)

    raise ValueError("Unsupported expression")


# =========================
# Calculator Tool
# =========================

class CalculatorTool(Tool):

    name = "calculate"

    def execute(self, args):

        text = args["input"]

        # prevent false positives
        if not looks_like_math(text):
            return ToolResult("That does not look like a math expression.")

        expr = extract_expression(text)

        if not expr:
            return ToolResult("I could not read the math expression.")

        try:
            tree = ast.parse(expr, mode="eval")

            result = safe_eval(tree.body)

            # cleaner formatting
            if isinstance(result, float):

                if result.is_integer():
                    result = int(result)
                else:
                    result = round(result, 10)

            return ToolResult(str(result))

        except ZeroDivisionError:
            return ToolResult("Division by zero is not allowed.")

        except OverflowError:
            return ToolResult("The number is too large.")

        except Exception:
            return ToolResult("I could not calculate that.")