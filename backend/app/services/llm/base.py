from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass
class ChatResult:
    """LLM 调用结果，包含文本内容和 token 用量"""
    content: str = ""
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0


class BaseLLMProvider(ABC):
    """LLM 平台抽象基类"""

    @abstractmethod
    async def chat(
        self,
        system_prompt: str,
        user_prompt: str,
        max_tokens: int = 4096,
        temperature: float = 0.7,
    ) -> ChatResult:
        """发送消息并返回结果（含 token 用量）"""
