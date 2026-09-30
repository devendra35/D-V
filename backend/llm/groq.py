from groq import Groq

from backend.config import settings
from backend.llm.provider import LLMProvider, LLMResponse


class GroqProvider(LLMProvider):
    """Groq implementation of the DΞV LLM provider."""

    def __init__(self) -> None:
        if not settings.groq_api_key:
            raise ValueError("GROQ_API_KEY is not configured.")

        self.client = Groq(
            api_key=settings.groq_api_key,
        )

        self.model = "openai/gpt-oss-120b"

    def generate(
        self,
        prompt: str,
        system_prompt: str | None = None,
    ) -> LLMResponse:
        """Generate a response using Groq."""

        messages: list[dict[str, str]] = []

        if system_prompt:
            messages.append(
                {
                    "role": "system",
                    "content": system_prompt,
                }
            )

        messages.append(
            {
                "role": "user",
                "content": prompt,
            }
        )

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.2,
        )

        content = response.choices[0].message.content or ""

        return LLMResponse(
            content=content,
            provider="groq",
            model=self.model,
        )