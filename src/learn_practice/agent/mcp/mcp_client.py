import logging

try:
    from ..schemas import ToolCall, ToolResult
except ImportError:
    from schemas import ToolCall, ToolResult


logger = logging.getLogger(__name__)


class McpClient:
    def __init__(self, server=None, tool_handlers=None):
        self.server = server
        self.tool_handlers = tool_handlers or {}

    def execute(self, tool_call: ToolCall) -> ToolResult:
        logger.info("[mcp] 调用 %s(%s)", tool_call.tool_name, tool_call.arguments)
        if self.server is not None:
            data = self.server.call_tool(tool_call.tool_name, tool_call.arguments)
        else:
            handler = self.tool_handlers.get(tool_call.tool_name)
            if handler is None:
                data = {"tool_name": tool_call.tool_name, "error": "未配置 MCP 工具。"}
            else:
                handler_result = handler(**tool_call.arguments)
                if isinstance(handler_result, dict):
                    data = handler_result
                else:
                    data = {"tool_name": tool_call.tool_name, "matches": handler_result}
        success = "error" not in data
        message = "MCP 工具执行成功。"
        if not success:
            logger.warning("[mcp] %s 调用失败：%s", tool_call.tool_name, data["error"])
            message = data["error"]
        return ToolResult(
            tool_name=tool_call.tool_name,
            success=success,
            data=data,
            message=message,
            tool_type=tool_call.tool_type
        )
