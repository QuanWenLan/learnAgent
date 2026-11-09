from abc import ABC, abstractmethod

try:
    from ..schemas import AgentResponse
except ImportError:
    from schemas import AgentResponse


class BaseSkill(ABC):
    name = "base"

    @abstractmethod
    def run(self, user_input: str) -> AgentResponse:
        pass
