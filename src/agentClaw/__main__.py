"""包入口：python -m src.agentClaw 直接运行 Agent 演示。"""

from .agent import run_agent

QUESTION = "现在几点了？另外帮我算一下 (28 + 62) * 3 等于多少。"


if __name__ == "__main__":
    print(f"用户: {QUESTION}\n")
    answer = run_agent(QUESTION)
    print(f"\n最终回答: {answer}")
