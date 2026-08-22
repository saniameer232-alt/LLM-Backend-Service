import time
from collections.abc import AsyncGenerator

from groq import AsyncGroq

from app.core.config import settings


class LLMService:
    def __init__(self):
        self.api_key = settings.groq_api_key
        self.default_model = settings.default_model
        self.timeout = settings.llm_timeout

        self.client = AsyncGroq(
            api_key=self.api_key,
        )

    def get_available_models(self) -> list[str]:
        return [
            "openai/gpt-oss-20b",
        ]

    def _build_messages(
        self,
        message: str,
        system_prompt: str | None = None,
        history: list[dict] | None = None,
    ) -> list[dict]:

        messages = []

        if system_prompt:
            messages.append(
                {
                    "role": "system",
                    "content": system_prompt,
                }
            )

        if history:
            messages.extend(history)

        messages.append(
            {
                "role": "user",
                "content": message,
            }
        )

        return messages

    async def generate_response(
        self,
        message: str,
        system_prompt: str | None = None,
        model: str | None = None,
        temperature: float = 0.7,
        max_tokens: int = 300,
        history: list[dict] | None = None,
    ) -> dict:

        start_time = time.perf_counter()

        if model is None:
            model = self.default_model

        messages = self._build_messages(
            message=message,
            system_prompt=system_prompt,
            history=history,
        )

        response = await self.client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            timeout=self.timeout,
        )

        content = response.choices[0].message.content or ""

        tokens_used = 0

        if response.usage:
            tokens_used = response.usage.total_tokens

        latency_ms = (
            time.perf_counter() - start_time
        ) * 1000

        return {
            "response": content,
            "model": model,
            "tokens_used": tokens_used,
            "latency_ms": round(latency_ms, 2),
        }

    async def stream_response(
        self,
        message: str,
        system_prompt: str | None = None,
        model: str | None = None,
        temperature: float = 0.7,
        max_tokens: int = 300,
        history: list[dict] | None = None,
    ) -> AsyncGenerator[str, None]:

        if model is None:
            model = self.default_model

        messages = self._build_messages(
            message=message,
            system_prompt=system_prompt,
            history=history,
        )

        stream = await self.client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            timeout=self.timeout,
            stream=True,
        )

        async for chunk in stream:

            if not chunk.choices:
                continue

            delta = chunk.choices[0].delta

            if delta and delta.content:
                yield delta.content
