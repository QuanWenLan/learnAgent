import os
import sys

AGENT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PARENT_DIR = os.path.dirname(AGENT_DIR)
for path in [AGENT_DIR, PARENT_DIR]:
    if path not in sys.path:
        sys.path.insert(0, path)

try:
    from ..bootstrap import CURRENT_DIR
    from ..router import IntentRouter
    from ..skill_config import SkillConfigLoader
    from .markdown_skill_runtime import MarkdownSkillRuntime
except ImportError:
    from bootstrap import CURRENT_DIR
    from router import IntentRouter
    from skill_config import SkillConfigLoader
    from mock.markdown_skill_runtime import MarkdownSkillRuntime


class MarkdownAgent:
    def __init__(self):
        self.router = IntentRouter()
        self.runtime = MarkdownSkillRuntime()
        self.loader = SkillConfigLoader(f"{CURRENT_DIR}/docs/skills")
        self.skill_configs = self.loader.load_all()

    def run(self, user_input: str):
        intent_result = self.router.detect_intent(user_input)
        skill_config = self.skill_configs[intent_result.intent]
        response = self.runtime.run(user_input, skill_config)
        return intent_result, response


def print_response(intent_result, response):
    print("=" * 80)
    print(f"用户输入：{response.user_input}")
    print(f"识别意图：{intent_result.intent}，置信度：{intent_result.confidence}")
    if intent_result.matched_keyword:
        print(f"命中关键词：{intent_result.matched_keyword}")
    print(f"使用 skill：{response.skill_name}")
    print("执行步骤：")
    for step in response.steps:
        print(f"- {step}")
    if response.tool_calls:
        print("工具调用：")
        for tool_call in response.tool_calls:
            print(f"- [{tool_call.tool_type}] {tool_call.tool_name} {tool_call.arguments}")
    print("最终回复：")
    print(response.answer)
    print("=" * 80)


if __name__ == "__main__":
    agent = MarkdownAgent()
    print("欢迎进入 Markdown skill runtime 演示，输入 quit 退出。")
    while True:
        user_input = input("请输入问题：").strip()
        if user_input.lower() in {"quit", "exit"}:
            print("已退出。")
            break
        if not user_input:
            print("请输入有效内容。")
            continue
        intent_result, response = agent.run(user_input)
        print_response(intent_result, response)
