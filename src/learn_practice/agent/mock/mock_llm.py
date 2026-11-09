try:
    from ..schemas import ToolCall
    from ..tool_schemas import FUNCTION_SCHEMAS
except ImportError:
    from schemas import ToolCall
    from tool_schemas import FUNCTION_SCHEMAS


class MockLlm:
    # tools 参数只为与真实 LLM (OpenAiCompatLlm) 的接口对齐，mock 实现不使用
    def choose_function_call(self, user_input: str, tools: list = None) -> ToolCall:
        if "天气" in user_input or "温度" in user_input:
            city = self._extract_city(user_input)
            return ToolCall(tool_name="get_weather", arguments={"city": city}, tool_type="function_call")
        if "订单" in user_input or "退款" in user_input or "物流" in user_input:
            order_id = self._extract_order_id(user_input)
            return ToolCall(tool_name="query_order", arguments={"order_id": order_id}, tool_type="function_call")
        keyword = self._extract_keyword(user_input)
        return ToolCall(tool_name="search_docs", arguments={"keyword": keyword}, tool_type="function_call")

    def _extract_city(self, user_input: str) -> str:
        for city in ["北京", "上海", "深圳"]:
            if city in user_input:
                return city
        return "北京"

    def _extract_order_id(self, user_input: str) -> str:
        for order_id in ["A1001", "A1002", "A1003"]:
            if order_id in user_input:
                return order_id
        return "A1001"

    def _extract_keyword(self, user_input: str) -> str:
        for keyword in ["agent", "skill", "function call", "mcp"]:
            if keyword in user_input.lower():
                return keyword
        return "agent"
