from google import genai

from backend.config import settings
from backend.llm.provider import LLMProvider, LLMResponse


class GeminiProvider(LLMProvider):
    """Gemini implementation of the DΞV LLM provider."""

    def __init__(self) -> None:
        if not settings.gemini_api_key:
            raise ValueError("GEMINI_API_KEY is not configured.")

        self.client = genai.Client(
            api_key=settings.gemini_api_key
        )
        self.model = "gemini-3.7-flash"

    def generate(
        self,
        prompt: str,
        system_prompt: str | None = None,
    ) -> LLMResponse:
        """Generate a response using Gemini."""

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config={
                "system_instruction": system_prompt
            } if system_prompt else None,
        )

        return LLMResponse(
            content=response.text or "",
            provider="gemini",
            model=self.model,
        )