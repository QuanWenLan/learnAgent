"""Agent 的工具集：函数实现 + 工具注册表 + 提供给 LLM 的 JSON Schema。

新增工具三步走：
    1. 在下面实现一个函数（入参用基本类型，返回 str）；
    2. 把函数加入 TOOLS 注册表；
    3. 在 TOOL_SCHEMAS 里补一段说明（description 决定 LLM 何时会选它）。
"""

import ast
import operator
from datetime import datetime

import requests
from bs4 import BeautifulSoup

# ---------------------------------------------------------------- 工具实现


def get_current_time() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


_BIN_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}
_UNARY_OPS = {ast.UAdd: operator.pos, ast.USub: operator.neg}


def _eval_node(node):
    if isinstance(node, ast.Expression):
        return _eval_node(node.body)
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _BIN_OPS:
        return _BIN_OPS[type(node.op)](_eval_node(node.left), _eval_node(node.right))
    if isinstance(node, ast.UnaryOp) and type(node.op) in _UNARY_OPS:
        return _UNARY_OPS[type(node.op)](_eval_node(node.operand))
    raise ValueError(f"不支持的表达式: {ast.dump(node)}")


def calculate(expression: str) -> str:
    """安全地计算四则运算表达式，如 '3 * (4 + 5)'。"""
    try:
        result = _eval_node(ast.parse(expression, mode="eval"))
        return str(result)
    except Exception as e:
        return f"计算出错: {e}"


def web_search(query: str, max_results: int = 5) -> str:
    """用必应搜索网页，返回标题、链接和摘要。"""
    try:
        max_results = int(max_results)
    except (TypeError, ValueError):
        max_results = 5
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        )
    }
    try:
        resp = requests.get(
            "https://cn.bing.com/search",
            params={"q": query},
            headers=headers,
            timeout=15,
        )
        resp.raise_for_status()
    except Exception as e:
        return f"搜索请求失败: {e}"

    try:
        soup = BeautifulSoup(resp.text, "html.parser")
        results = []
        for li in soup.select("li.b_algo"):
            a = li.select_one("h2 a")
            if not a:
                continue
            p = li.select_one(".b_caption p") or li.select_one("p")
            snippet = p.get_text(strip=True) if p else ""
            results.append(f"标题: {a.get_text(strip=True)}\n链接: {a.get('href', '')}\n摘要: {snippet}")
            if len(results) >= max_results:
                break
    except Exception as e:
        return f"解析搜索结果失败: {e}"

    return "\n\n".join(results) if results else "没有找到相关结果。"


# ---------------------------------------------------------------- 工具注册


TOOLS = {
    "get_current_time": get_current_time,
    "calculate": calculate,
    "web_search": web_search,
}

TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "获取当前的日期和时间",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "计算一个数学表达式，支持 + - * / // % ** 和括号",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {"type": "string", "description": "要计算的表达式，如 '3 * (4 + 5)'"},
                },
                "required": ["expression"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": "在必应上搜索网页，获取实时信息，如天气、新闻、股票行情等。返回搜索结果的标题、链接和摘要。",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "搜索关键词，如 '深圳天气'、'贵州茅台 股价'"},
                    "max_results": {"type": "integer", "description": "返回结果条数，默认 5", "default": 5},
                },
                "required": ["query"],
            },
        },
    },
]
