from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class ToolCall:
    tool_name: str
    arguments: Dict[str, Any]
    tool_type: str


@dataclass
class ToolResult:
    tool_name: str
    success: bool
    data: Any
    message: str
    tool_type: str


@dataclass
class AgentResponse:
    user_input: str
    intent: str
    skill_name: str
    answer: str
    steps: List[str] = field(default_factory=list)
    tool_calls: List[ToolCall] = field(default_factory=list)
    tool_results: List[ToolResult] = field(default_factory=list)


@dataclass
class IntentResult:
    intent: str
    confidence: float
    matched_keyword: Optional[str] = None
