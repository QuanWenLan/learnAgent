import logging

try:
    from ..function_call.functions import search_docs
except ImportError:
    from function_call.functions import search_docs

try:
    from ..mcp.mcp_client import McpClient
    from ..schemas import AgentResponse, ToolCall
    from .base import BaseSkill
except ImportError:
    from mcp.mcp_client import McpClient
    from schemas import AgentResponse, ToolCall
    from skills.base import BaseSkill


logger = logging.getLogger(__name__)


# MCP 工具的 schema，回填生成回答时随消息一起发给模型
DOC_SEARCH_TOOLS = [{
    "name": "doc.search",
    "description": "根据关键词搜索文档",
    "parameters": {
        "type": "object",
        "properties": {"keyword": {"type": "string", "description": "文档关键词"}},
        "required": ["keyword"],
    },
}]


class ResearchSkill(BaseSkill):
    name = "research_skill"

    def __init__(self, llm=None, mcp_client=None):
        self.llm = llm
        self.mcp_client = mcp_client or McpClient(tool_handlers={"doc.search": search_docs})

    def run(self, user_input: str) -> AgentResponse:
        keyword = self._extract_keyword(user_input)
        logger.info("[%s] 提取关键词：%s", self.name, keyword)
        tool_call = ToolCall(
            tool_name="doc.search",
            arguments={"keyword": keyword},
            tool_type="mcp"
        )
        tool_result = self.mcp_client.execute(tool_call)
        matches = tool_result.data.get("matches", [])
        logger.info("[%s] doc.search 返回 %d 条结果", self.name, len(matches))
        answer = self._compose_answer(user_input, tool_call, tool_result.data)
        return AgentResponse(
            user_input=user_input,
            intent="research",
            skill_name=self.name,
            answer=answer,
            steps=["识别为 research 意图", "进入 research skill", "提取搜索关键词", "通过 MCP client 调用 doc.search（必应实时数据）"],
            tool_calls=[tool_call],
            tool_results=[tool_result]
        )

    def _compose_answer(self, user_input: str, tool_call, data: dict) -> str:
        generate = getattr(self.llm, "generate_answer", None)
        if generate is not None:
            # 真实模式：工具结果回填给 LLM，生成自然回答；失败回落模板
            logger.info("[%s] 工具结果回填，LLM 生成自然回答...", self.name)
            try:
                return generate(user_input, DOC_SEARCH_TOOLS, tool_call, data)
            except Exception:
                logger.warning("[%s] 回填生成失败，回落模板回答", self.name)
        return self._template_answer(data)

    def _template_answer(self, data: dict) -> str:
        lines = []
        for item in data["matches"]:
            line = f"- {item['title']}：{item['summary']}"
            if item.get("link"):
                line += f"\n  {item['link']}"
            lines.append(line)
        return "为你找到以下资料：\n" + "\n".join(lines)

    def _extract_keyword(self, user_input: str) -> str:
        if self.llm is not None:
            try:
                return self.llm.extract_keyword(user_input)
            except Exception:
                pass  # LLM 失败不崩，回落关键词列表
        return self._keyword_fallback(user_input)

    def _keyword_fallback(self, user_input: str) -> str:
        normalized_text = user_input.lower()
        for keyword in ["agent", "skill", "function call", "mcp"]:
            if keyword in normalized_text:
                return keyword
        return "agent"
