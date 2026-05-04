from __future__ import annotations

import ast
import operator as op

from jarvis.tools.base import Tool, ToolResult
from jarvis.utils.parser import extract_expression


_ALLOWED = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Mod: op.mod,
    ast.Pow: op.pow,
    ast.UAdd: op.pos,
    ast.USub: op.neg,
}


def _safe_eval(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value

    if isinstance(node, ast.Num):
        return node.n

    if isinstance(node, ast.BinOp):
        left = _safe_eval(node.left)
        right = _safe_eval(node.right)
        operator = _ALLOWED[type(node.op)]
        return operator(left, right)

    if isinstance(node, ast.UnaryOp):
        operand = _safe_eval(node.operand)
        operator = _ALLOWED[type(node.op)]
        return operator(operand)

    raise ValueError("Unsupported expression")


class CalculatorTool(Tool):
    name = "calculate"

    def execute(self, args):
        text = args["input"]
        expr = extract_expression(text)

        if not expr:
            return ToolResult("I could not read the math expression.")

        try:
            tree = ast.parse(expr, mode="eval")
            result = _safe_eval(tree.body)

            if isinstance(result, float) and result.is_integer():
                result = int(result)

            return ToolResult(f"{result}")
        except Exception:
            return ToolResult("I could not calculate that.")
