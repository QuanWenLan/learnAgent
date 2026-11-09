import logging

try:
    from ..schemas import AgentResponse
    from .base import BaseSkill
except ImportError:
    from schemas import AgentResponse
    from skills.base import BaseSkill


logger = logging.getLogger(__name__)


class ChatSkill(BaseSkill):
    name = "chat_skill"

    def __init__(self, llm=None):
        # 未注入自然语言客户端时保留确定性的离线兜底话术
        self.llm = llm

    def run(self, user_input: str) -> AgentResponse:
        answer = (
            "这是一个兜底闲聊 skill。当前没有命中天气、订单或资料检索意图，"
            "所以直接返回普通说明。"
        )
        steps = ["识别为 chat 意图", "进入 chat skill", "返回兜底说明"]
        if self.llm is not None:
            try:
                logger.info("[%s] LLM 直接生成回复...", self.name)
                answer = self.llm.chat(user_input)
                steps = ["识别为 chat 意图", "进入 chat skill", "由 LLM 直接生成回复"]
            except Exception:
                pass  # LLM 失败保持兜底话术
        return AgentResponse(
            user_input=user_input,
            intent="chat",
            skill_name=self.name,
            answer=answer,
            steps=steps
        )
