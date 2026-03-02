from abc import ABC, abstractmethod

from app.models.application import Application


class PromptBuilder(ABC):
    """提示词构建器接口"""

    @abstractmethod
    def build(
        self,
        app: Application,
        section_key: str,
        extra_prompt: str | None = None,
    ) -> tuple[str, str]:
        """构建提示词，返回 (system_prompt, user_prompt)"""
