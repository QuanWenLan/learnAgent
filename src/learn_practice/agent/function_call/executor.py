import logging

try:
    from .registry import FUNCTION_REGISTRY
    from ..schemas import ToolCall, ToolResult
except ImportError:
    from function_call.registry import FUNCTION_REGISTRY
    from schemas import ToolCall, ToolResult


logger = logging.getLogger(__name__)


class FunctionExecutor:
    def __init__(self, registry=None):
        self.registry = registry or FUNCTION_REGISTRY

    def execute(self, tool_call: ToolCall) -> ToolResult:
        function = self.registry.get(tool_call.tool_name)
        if function is None:
            logger.warning("[function] 未注册的工具：%s", tool_call.tool_name)
            return ToolResult(
                tool_name=tool_call.tool_name,
                success=False,
                data=None,
                message="未找到对应的 function。",
                tool_type=tool_call.tool_type
            )
        logger.info("[function] 执行 %s(%s)", tool_call.tool_name, tool_call.arguments)
        data = function(**tool_call.arguments)
        return ToolResult(
            tool_name=tool_call.tool_name,
            success=True,
            data=data,
            message="function 执行成功。",
            tool_type=tool_call.tool_type
        )
