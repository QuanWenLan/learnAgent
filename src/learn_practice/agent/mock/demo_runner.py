import logging
import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
AGENT_DIR = os.path.dirname(CURRENT_DIR)
PARENT_DIR = os.path.dirname(AGENT_DIR)
for path in [AGENT_DIR, PARENT_DIR]:
    if path not in sys.path:
        sys.path.insert(0, path)

from main import SimpleAgent, print_response
from mock.mock_llm import MockLlm
from mock.functions import FUNCTION_REGISTRY
from function_call.executor import FunctionExecutor
from mcp.mcp_client import McpClient
from mock.mcp.fake_mcp_server import FakeMcpServer


DEMO_CASES = [
    "北京今天天气怎么样？",
    "帮我查一下订单 A1001 的物流状态",
    "帮我搜索一下 agent 相关资料",
    "你好，简单介绍一下你自己"
]


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(message)s", stream=sys.stdout)
    agent = SimpleAgent(
        use_real_llm=False,
        llm=MockLlm(),
        function_executor=FunctionExecutor(registry=FUNCTION_REGISTRY),
        mcp_client=McpClient(server=FakeMcpServer())
    )
    print("演示模式：离线 mock")
    for user_input in DEMO_CASES:
        intent_result, response = agent.run(user_input)
        print_response(intent_result, response)
