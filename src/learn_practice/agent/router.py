import logging

try:
    from .schemas import IntentResult
except ImportError:
    from schemas import IntentResult


logger = logging.getLogger(__name__)


INTENT_KEYWORDS = {
    "weather": ["天气", "温度", "下雨", "晴天", "气温"],
    "order": ["订单", "退款", "物流", "发货", "快递"],
    "research": ["文档", "资料", "搜索", "查询知识", "查资料"],
    "chat": []
}


class IntentRouter:
    def detect_intent(self, user_input: str) -> IntentResult:
        normalized_text = user_input.lower()
        for intent, keywords in INTENT_KEYWORDS.items():
            for keyword in keywords:
                if keyword in normalized_text:
                    return IntentResult(intent=intent, confidence=0.95, matched_keyword=keyword)
        return IntentResult(intent="chat", confidence=0.60, matched_keyword=None)


class LlmIntentRouter:
    """两层路由：关键词命中直接返回（省一次 LLM 调用），未命中再交给模型分类。"""

    INTENT_DESCRIPTIONS = {
        "weather": "天气、温度、下雨、穿衣建议等",
        "order": "订单、退款、物流、快递等购物售后",
        "research": "查资料、搜文档、找概念解释",
        "chat": "问候、闲聊或无法归类",
    }

    def __init__(self, llm=None):
        self.keyword_router = IntentRouter()
        self.llm = llm

    def detect_intent(self, user_input: str) -> IntentResult:
        result = self.keyword_router.detect_intent(user_input)
        if result.intent != "chat" or self.llm is None:
            return result
        logger.info("[路由] 关键词未命中，交给 LLM 分类")
        classified = self.llm.classify_intent(user_input, self.INTENT_DESCRIPTIONS)
        if classified:
            intent, confidence = classified
            return IntentResult(intent=intent, confidence=confidence)
        return result  # LLM 失败也不崩，兜底回 chat
