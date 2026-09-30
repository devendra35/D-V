from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class LLMResponse:
    """Standard response returned by any LLM provider."""

    content: str
    provider: str
    model: str


class LLMProvider(ABC):
    """Base interface for all DΞV LLM providers."""

    @abstractmethod
    def generate(
        self,
        prompt: str,
        system_prompt: str | None = None,
    ) -> LLMResponse:
        """Generate a response from the language model."""
        raise NotImplementedError