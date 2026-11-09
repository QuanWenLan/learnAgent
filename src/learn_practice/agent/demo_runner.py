import logging
import sys

try:
    from .bootstrap import CURRENT_DIR
    from .main import SimpleAgent, print_response
except ImportError:
    from bootstrap import CURRENT_DIR
    from main import SimpleAgent, print_response


DEMO_CASES = [
    "北京今天天气怎么样？",
    "帮我查一下订单 A1001 的物流状态",
    "帮我搜索一下 agent 相关资料",
    "你好，简单介绍一下你自己"
]


if __name__ == "__main__":
    _ = CURRENT_DIR
    logging.basicConfig(level=logging.INFO, format="%(message)s", stream=sys.stdout)
    agent = SimpleAgent()
    print("演示模式：真实 LLM")
    for user_input in DEMO_CASES:
        intent_result, response = agent.run(user_input)
        print_response(intent_result, response)
