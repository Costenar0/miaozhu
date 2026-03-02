from app.core.config import settings
from app.services.llm.base import BaseLLMProvider
from app.services.llm.openai_provider import OpenAIProvider


def create_llm_provider() -> BaseLLMProvider:
    """创建 LLM Provider 实例（通用 OpenAI 兼容接口）"""
    return OpenAIProvider(
        api_key=settings.LLM_API_KEY,
        base_url=settings.LLM_BASE_URL,
        model=settings.LLM_MODEL,
    )
