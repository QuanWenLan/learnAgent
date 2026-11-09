try:
    from ..schemas import AgentResponse, ToolCall, ToolResult
    from ..tool_schemas import FUNCTION_SCHEMAS
    from .mock_llm import MockLlm
    from ..function_call.executor import FunctionExecutor
    from ..mcp.mcp_client import McpClient
    from ..skill_config import SkillConfig
    from .mcp.fake_mcp_server import FakeMcpServer
    from .functions import FUNCTION_REGISTRY
except ImportError:
    from schemas import AgentResponse, ToolCall, ToolResult
    from tool_schemas import FUNCTION_SCHEMAS
    from mock.mock_llm import MockLlm
    from function_call.executor import FunctionExecutor
    from mcp.mcp_client import McpClient
    from skill_config import SkillConfig
    from mock.mcp.fake_mcp_server import FakeMcpServer
    from mock.functions import FUNCTION_REGISTRY


FUNCTION_TOOL_NAMES = {tool['name'] for tool in FUNCTION_SCHEMAS}


class MarkdownSkillRuntime:
    def __init__(self):
        self.mock_llm = MockLlm()
        self.function_executor = FunctionExecutor(registry=FUNCTION_REGISTRY)
        self.mcp_client = McpClient(server=FakeMcpServer())

    def run(self, user_input: str, skill_config: SkillConfig) -> AgentResponse:
        steps = [
            f"识别为 {skill_config.intent} 意图",
            f"加载 Markdown skill：{skill_config.name}",
            "读取 skill 提示词与工具配置"
        ]
        tool_call = self._build_tool_call(user_input, skill_config, steps)
        tool_result = self._execute_tool_call(tool_call)
        answer = self._build_answer(skill_config, tool_result)
        steps.append("根据 skill 配置整理最终回复")
        return AgentResponse(
            user_input=user_input,
            intent=skill_config.intent,
            skill_name=f"{skill_config.name}_markdown_runtime",
            answer=answer,
            steps=steps,
            tool_calls=[tool_call] if tool_call else [],
            tool_results=[tool_result] if tool_result else []
        )

    def _build_tool_call(self, user_input: str, skill_config: SkillConfig, steps: list[str]):
        if not skill_config.tools:
            steps.append("当前 skill 没有配置工具，直接生成自然语言回复")
            return None
        first_tool = skill_config.tools[0]
        if first_tool in FUNCTION_TOOL_NAMES:
            steps.append("根据 skill 配置选择 function call 工具")
            tool_call = self.mock_llm.choose_function_call(user_input)
            if tool_call.tool_name not in skill_config.tools:
                tool_call.tool_name = first_tool
            return tool_call
        steps.append("根据 skill 配置选择 MCP 工具")
        keyword = self.mock_llm._extract_keyword(user_input)
        return ToolCall(
            tool_name=first_tool,
            arguments={"keyword": keyword},
            tool_type="mcp"
        )

    def _execute_tool_call(self, tool_call: ToolCall | None):
        if tool_call is None:
            return None
        if tool_call.tool_type == "mcp":
            return self.mcp_client.execute(tool_call)
        return self.function_executor.execute(tool_call)

    def _build_answer(self, skill_config: SkillConfig, tool_result: ToolResult | None) -> str:
        if tool_result is None:
            return f"已进入 {skill_config.name}，当前没有配置工具，因此直接返回说明。"
        if skill_config.intent == "weather":
            data = tool_result.data
            return f"{data['city']}今天天气{data['weather']}，气温 {data['temperature']}℃。建议：{data['advice']}"
        if skill_config.intent == "order":
            data = tool_result.data
            return f"订单 {data['order_id']} 当前状态：{data['status']}；物流：{data['logistics']}；说明：{data['eta']}"
        if skill_config.intent == "research":
            matches = tool_result.data.get('matches', [])
            lines = []
            for item in matches:
                lines.append(f"- {item['title']}：{item['summary']}")
            return "为你找到以下资料：\n" + "\n".join(lines)
        return f"已根据 {skill_config.name} 的 Markdown 提示词完成回复。"
