"""最小的 Agent 循环：接收用户消息 -> 调用 LLM -> 执行工具调用 -> 反馈结果 -> 循环直到最终回答。

运行：
    .venv/Scripts/python.exe -m src.agentClaw

API 密钥、地址、模型等配置统一在 config.py 中维护。
工具的实现在 tools.py 中维护。
"""

import json

import requests

from .config import API_KEY, BASE_URL, MAX_ROUNDS, MODEL, USER_AGENT
from .tools import TOOLS, TOOL_SCHEMAS

# ---------------------------------------------------------------- LLM 调用


def call_llm(messages: list) -> dict:
    resp = requests.post(
        f"{BASE_URL}/chat/completions",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}",
            "User-Agent": USER_AGENT,
        },
        json={"model": MODEL, "messages": messages, "tools": TOOL_SCHEMAS},
        timeout=120,
    )
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]


# ---------------------------------------------------------------- Agent 循环


def run_agent(user_message: str) -> str:
    messages = [{"role": "user", "content": user_message}]

    for round_no in range(1, MAX_ROUNDS + 1):
        message = call_llm(messages)
        messages.append(message)

        tool_calls = message.get("tool_calls")
        if not tool_calls:
            return message.get("content") or ""

        print(f"[round {round_no}] LLM 请求调用 {len(tool_calls)} 个工具")
        for call in tool_calls:
            name = call["function"]["name"]
            try:
                args = json.loads(call["function"].get("arguments") or "{}")
            except json.JSONDecodeError:
                args = {}
            print(f"  -> {name}({args})")

            if name in TOOLS:
                try:
                    result = str(TOOLS[name](**args))
                except Exception as e:
                    result = f"工具执行出错: {e}"
            else:
                result = f"未知工具: {name}"
            print(f"  <- {result}")

            messages.append(
                {"role": "tool", "tool_call_id": call["id"], "content": result}
            )

    return "达到最大循环轮数，未能得到最终回答。"
