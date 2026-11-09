try:
    from ..fake_data import KNOWLEDGE_BASE
    from ..functions import search_docs
except ImportError:
    from fake_data import KNOWLEDGE_BASE
    from mock.functions import search_docs


class FakeMcpServer:
    """模拟进程外的 MCP 服务。

    kb.search 是真正的本地知识库（本来就是本地能力，不算 mock）；
    doc.search 内部已接真实必应搜索，只保留 MCP 协议这一层"假装在进程外"。
    """

    def call_tool(self, tool_name: str, arguments: dict) -> dict:
        if tool_name == "kb.search":
            keyword = arguments.get("keyword", "agent").lower()
            content = KNOWLEDGE_BASE.get(keyword, "知识库中没有找到该关键词，返回 Agent 基础说明。")
            return {
                "tool_name": tool_name,
                "keyword": keyword,
                "content": content
            }
        if tool_name == "doc.search":
            keyword = arguments.get("keyword", "agent")
            matches = search_docs(keyword)
            return {
                "tool_name": tool_name,
                "keyword": keyword,
                "matches": matches
            }
        return {
            "tool_name": tool_name,
            "error": "不支持的 MCP 工具。"
        }
