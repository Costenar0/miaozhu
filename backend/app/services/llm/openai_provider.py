import asyncio
import logging

from openai import AsyncOpenAI, APIConnectionError, APITimeoutError, APIError
import httpx

from app.services.llm.base import BaseLLMProvider, ChatResult

logger = logging.getLogger(__name__)

# 单次调用上限
_API_MAX_TOKENS = 8192
# 判断是否被截断的阈值（completion_tokens >= 此值视为截断）
_TRUNCATION_THRESHOLD = _API_MAX_TOKENS - 200
# 最大续写轮数
_MAX_CONTINUATION_ROUNDS = 5
# 重试配置
_MAX_RETRIES = 3
_RETRY_DELAYS = [2, 5, 10]  # 重试间隔（秒）


class OpenAIProvider(BaseLLMProvider):
    """通用 OpenAI 兼容 LLM Provider"""

    def __init__(self, api_key: str, base_url: str, model: str):
        self.model = model
        self.client = AsyncOpenAI(
            api_key=api_key,
            base_url=base_url,
            timeout=300.0,  # 5 分钟超时，避免 API 无响应时永久挂住
        )

    async def _single_chat(
        self,
        messages: list[dict],
        max_tokens: int,
        temperature: float,
    ) -> ChatResult:
        """单次 API 调用（带重试机制）"""
        last_error = None

        for attempt in range(_MAX_RETRIES):
            try:
                response = await self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    max_tokens=min(max_tokens, _API_MAX_TOKENS),
                    temperature=temperature,
                )
                content = response.choices[0].message.content or ""
                usage = response.usage
                return ChatResult(
                    content=content,
                    prompt_tokens=usage.prompt_tokens if usage else 0,
                    completion_tokens=usage.completion_tokens if usage else 0,
                    total_tokens=usage.total_tokens if usage else 0,
                )
            except (APIConnectionError, APITimeoutError, httpx.RemoteProtocolError, httpx.ConnectError) as e:
                last_error = e
                if attempt < _MAX_RETRIES - 1:
                    delay = _RETRY_DELAYS[attempt]
                    logger.warning(
                        "LLM API network error (attempt %d/%d): %s. Retrying in %ds...",
                        attempt + 1, _MAX_RETRIES, str(e), delay
                    )
                    await asyncio.sleep(delay)
                else:
                    logger.error(
                        "LLM API failed after %d attempts: %s",
                        _MAX_RETRIES, str(e)
                    )
            except APIError as e:
                logger.error("LLM API error (non-retryable): %s", str(e))
                raise

        raise ConnectionError(f"Failed after {_MAX_RETRIES} retries") from last_error

    async def chat(
        self,
        system_prompt: str,
        user_prompt: str,
        max_tokens: int = 4096,
        temperature: float = 0.7,
    ) -> ChatResult:
        logger.info("LLM chat: model=%s, max_tokens=%d", self.model, max_tokens)

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]

        # 单次就够的直接返回
        if max_tokens <= _API_MAX_TOKENS:
            result = await self._single_chat(messages, max_tokens, temperature)
            logger.info(
                "LLM response: %d chars, tokens(prompt=%d, completion=%d, total=%d)",
                len(result.content), result.prompt_tokens, result.completion_tokens, result.total_tokens,
            )
            return result

        # ── 多轮续写 ──────────────────────────────────────
        all_content: list[str] = []
        total_prompt_tokens = 0
        total_completion_tokens = 0
        total_all_tokens = 0
        remaining = max_tokens

        # 第一轮
        result = await self._single_chat(messages, remaining, temperature)
        all_content.append(result.content)
        total_prompt_tokens += result.prompt_tokens
        total_completion_tokens += result.completion_tokens
        total_all_tokens += result.total_tokens
        remaining -= result.completion_tokens

        logger.info(
            "LLM round 1: %d chars, completion_tokens=%d, remaining=%d",
            len(result.content), result.completion_tokens, remaining,
        )

        # 续写轮
        for round_num in range(2, _MAX_CONTINUATION_ROUNDS + 1):
            if result.completion_tokens < _TRUNCATION_THRESHOLD:
                break
            if remaining < 500:
                break

            messages.append({"role": "assistant", "content": result.content})
            messages.append({"role": "user", "content": "请继续，从上面中断的地方接着写，不要重复已有内容。"})

            result = await self._single_chat(messages, remaining, temperature)
            all_content.append(result.content)
            total_prompt_tokens += result.prompt_tokens
            total_completion_tokens += result.completion_tokens
            total_all_tokens += result.total_tokens
            remaining -= result.completion_tokens

            logger.info(
                "LLM round %d: %d chars, completion_tokens=%d, remaining=%d",
                round_num, len(result.content), result.completion_tokens, remaining,
            )

        final_content = "\n".join(all_content)
        logger.info(
            "LLM total: %d rounds, %d chars, tokens(prompt=%d, completion=%d, total=%d)",
            len(all_content), len(final_content),
            total_prompt_tokens, total_completion_tokens, total_all_tokens,
        )
        return ChatResult(
            content=final_content,
            prompt_tokens=total_prompt_tokens,
            completion_tokens=total_completion_tokens,
            total_tokens=total_all_tokens,
        )
