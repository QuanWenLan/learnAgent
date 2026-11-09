"""真实 LLM 客户端：OpenAI 兼容接口，供意图路由和 skill 内的工具选择共用。

与离线客户端保持同接口（choose_function_call），可通过构造函数注入到任意 skill，
实现真实调用链路。配置见 config.py。
"""
import json
import logging
import re
import time

try:
    from .config import API_KEY, BASE_URL, MODEL
    from .schemas import ToolCall
except ImportError:
    from config import API_KEY, BASE_URL, MODEL
    from schemas import ToolCall


logger = logging.getLogger(__name__)


def _chat(messages: list, tools: list = None, purpose: str = "LLM 调用") -> dict:
    """调用 /chat/completions，返回 choices[0].message。purpose 用于日志标注本次调用目的。"""
    import requests

    body = {"model": MODEL, "messages": messages}
    if tools:
        body["tools"] = tools
    start = time.time()
    resp = requests.post(
        f"{BASE_URL}/chat/completions",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}",
        },
        json=body,
        timeout=60,
    )
    if resp.status_code >= 400:
        # 带上网关返回的错误详情，方便定位（如工具名不合法、schema 格式错误等）
        raise RuntimeError(f"LLM 网关返回 {resp.status_code}: {resp.text[:500]}")
    logger.info("[LLM] %s，耗时 %.1fs", purpose, time.time() - start)
    return resp.json()["choices"][0]["message"]


class OpenAiCompatLlm:
    """OpenAI 兼容网关的真实实现。"""

    def choose_function_call(self, user_input: str, tools: list = None):
        """把工具选择交给模型：命中返回 ToolCall，模型不需要工具时返回 None。"""
        # 本项目 schema 是裸的 {name, description, parameters}，
        # OpenAI 接口要求外包一层 {"type": "function", "function": ...}
        openai_tools = [{"type": "function", "function": t} for t in (tools or [])]
        message = _chat([{"role": "user", "content": user_input}], tools=openai_tools, purpose="选择工具")
        calls = message.get("tool_calls")
        if not calls:
            return None
        call = calls[0]
        try:
            arguments = json.loads(call["function"].get("arguments") or "{}")
        except json.JSONDecodeError:
            arguments = {}
        return ToolCall(
            tool_name=call["function"]["name"],
            arguments=arguments,
            tool_type="function_call",
        )

    def classify_intent(self, user_input: str, intent_descriptions: dict):
        """意图分类：成功返回 (intent, confidence)，失败返回 None。"""
        desc = "、".join(f"{name}（{text}）" for name, text in intent_descriptions.items())
        message = _chat([
            {"role": "system",
             "content": f"把用户输入分类到以下意图之一：{desc}。"
                        '只输出 JSON：{"intent": "意图名", "confidence": 0~1}'},
            {"role": "user", "content": user_input},
        ], purpose="意图分类")
        content = message.get("content") or ""
        start, end = content.find("{"), content.rfind("}")  # 模型可能包 markdown 代码块
        if start == -1 or end == -1:
            return None
        try:
            data = json.loads(content[start:end + 1])
            if data.get("intent") in intent_descriptions:
                return data["intent"], float(data.get("confidence", 0.8))
        except (json.JSONDecodeError, TypeError, ValueError):
            pass
        return None

    def extract_keyword(self, user_input: str) -> str:
        """从用户输入中提取用于资料搜索的关键词。"""
        message = _chat([
            {"role": "system", "content": "从用户输入中提取一个用于搜索资料的关键词，只输出关键词本身，不要任何解释。"},
            {"role": "user", "content": user_input},
        ], purpose="提取关键词")
        keyword = (message.get("content") or "").strip().strip('"')
        return keyword or user_input

    def generate_answer(self, user_input: str, tools: list, tool_call, result_data) -> str:
        """agentClaw 式结果回填：把工具调用与执行结果按 OpenAI 消息结构回放，
        让模型基于真实数据组织最终回答（替代 skill 里的模板拼接）。"""

        def _safe_name(name: str) -> str:
            # 网关要求函数名匹配 ^[a-zA-Z0-9_-]+$，MCP 的 "doc.search" 这类名字要清洗
            return re.sub(r"[^a-zA-Z0-9_-]", "_", name)

        result_text = result_data if isinstance(result_data, str) else json.dumps(result_data, ensure_ascii=False)
        call_id = "call_answer"
        messages = [
            {"role": "user", "content": user_input},
            {
                "role": "assistant",
                "content": "",
                "tool_calls": [{
                    "id": call_id,
                    "type": "function",
                    "function": {
                        "name": _safe_name(tool_call.tool_name),
                        "arguments": json.dumps(tool_call.arguments, ensure_ascii=False),
                    },
                }],
            },
            {"role": "tool", "tool_call_id": call_id, "content": result_text},
        ]
        openai_tools = [
            {"type": "function", "function": {**t, "name": _safe_name(t["name"])}}
            for t in (tools or [])
        ]
        message = _chat(messages, tools=openai_tools, purpose="生成回答")
        if message.get("tool_calls"):
            # 模型还想继续调用工具；本版本不展开多轮循环，直接把数据给用户
            return result_text
        return message.get("content") or ""

    def chat(self, user_input: str) -> str:
        """普通对话：不带工具，直接返回文本回复。"""
        message = _chat([{"role": "user", "content": user_input}], purpose="闲聊回复")
        return message.get("content") or ""
