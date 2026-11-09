import logging

try:
    from ..function_call.executor import FunctionExecutor
    from ..tool_schemas import FUNCTION_SCHEMAS
    from ..schemas import AgentResponse
    from .base import BaseSkill
except ImportError:
    from function_call.executor import FunctionExecutor
    from tool_schemas import FUNCTION_SCHEMAS
    from schemas import AgentResponse
    from skills.base import BaseSkill


logger = logging.getLogger(__name__)


class OrderSkill(BaseSkill):
    name = "order_skill"

    def __init__(self, llm=None, executor=None):
        self.llm = llm
        self.executor = executor or FunctionExecutor()

    def run(self, user_input: str) -> AgentResponse:
        logger.info("[%s] 由 LLM 选择工具...", self.name)
        tool_call = self.llm.choose_function_call(user_input, FUNCTION_SCHEMAS)
        if tool_call is None:
            logger.info("[%s] 模型未选择工具", self.name)
            return AgentResponse(
                user_input=user_input,
                intent="order",
                skill_name=self.name,
                answer="模型判断这个问题不需要查询订单。",
                steps=["识别为 order 意图", "进入 order skill", "模型未选择工具"]
            )
        logger.info("[%s] 选中工具 %s(%s)", self.name, tool_call.tool_name, tool_call.arguments)
        tool_result = self.executor.execute(tool_call)
        logger.info("[%s] 工具执行%s", self.name,
                    "成功" if tool_result.success else f"失败：{tool_result.message}")
        data = tool_result.data
        generate = getattr(self.llm, "generate_answer", None)
        if generate is not None:
            # 真实模式：工具结果回填给 LLM，生成自然回答
            logger.info("[%s] 工具结果回填，LLM 生成自然回答...", self.name)
            answer = generate(user_input, FUNCTION_SCHEMAS, tool_call, data)
        else:
            # mock 模式：模板拼接
            answer = (
                f"订单 {data['order_id']} 当前状态：{data['status']}；"
                f"物流：{data['logistics']}；说明：{data['eta']}"
            )
        return AgentResponse(
            user_input=user_input,
            intent="order",
            skill_name=self.name,
            answer=answer,
            steps=["识别为 order 意图", "进入 order skill", "由 LLM 选择 function", "执行订单 function（演示数据）"],
            tool_calls=[tool_call],
            tool_results=[tool_result]
        )
