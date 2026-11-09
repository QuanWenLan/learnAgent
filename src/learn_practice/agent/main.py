import logging
import sys

try:
    from .bootstrap import CURRENT_DIR
    from .router import IntentRouter, LlmIntentRouter
    from .skills.chat_skill import ChatSkill
    from .skills.order_skill import OrderSkill
    from .skills.research_skill import ResearchSkill
    from .skills.weather_skill import WeatherSkill
except ImportError:
    from bootstrap import CURRENT_DIR
    from router import IntentRouter, LlmIntentRouter
    from skills.chat_skill import ChatSkill
    from skills.order_skill import OrderSkill
    from skills.research_skill import ResearchSkill
    from skills.weather_skill import WeatherSkill


logger = logging.getLogger(__name__)


class SimpleAgent:
    def __init__(self, use_real_llm: bool = True, llm=None, function_executor=None, mcp_client=None):
        if llm is None and use_real_llm:
            try:
                from .llm_client import OpenAiCompatLlm
            except ImportError:
                from llm_client import OpenAiCompatLlm
            llm = OpenAiCompatLlm()
        self.router = LlmIntentRouter(llm) if use_real_llm and llm is not None else IntentRouter()
        self.skills = {
            "weather": WeatherSkill(llm, executor=function_executor),
            "order": OrderSkill(llm, executor=function_executor),
            "research": ResearchSkill(llm, mcp_client=mcp_client),
            "chat": ChatSkill(llm)
        }

    def run(self, user_input: str):
        intent_result = self.router.detect_intent(user_input)
        skill = self.skills[intent_result.intent]
        logger.info("[agent] 意图=%s（置信度 %.2f），进入 skill：%s",
                    intent_result.intent, intent_result.confidence, skill.name)
        response = skill.run(user_input)
        return intent_result, response


def print_response(intent_result, response):
    # 过程信息（意图、skill、工具选择与执行）已由各环节的实时日志输出，
    # 这里只收尾展示最终回答；intent_result 保留在签名里供调用方兼容
    print("=" * 80)
    print(f"用户输入：{response.user_input}")
    print("最终回答：")
    print(response.answer)
    print("=" * 80)


if __name__ == "__main__":
    _ = CURRENT_DIR
    logging.basicConfig(level=logging.INFO, format="%(message)s", stream=sys.stdout)
    agent = SimpleAgent()
    mode = "真实 LLM 模式"
    print(f"欢迎进入简单 Agent 学习项目（{mode}），输入 quit 退出。")
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
