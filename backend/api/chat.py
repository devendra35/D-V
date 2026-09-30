from fastapi import APIRouter
from pydantic import BaseModel, Field


from backend.llm.groq import GroqProvider
from backend.llm.prompts import DEV_SYSTEM_PROMPT


router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


class ChatRequest(BaseModel):
    """Request body for the chat endpoint."""

    message: str = Field(
        min_length=1,
        max_length=4000,
    )

    session_id: str | None = Field(
        default=None,
        max_length=100,
    )


class ChatSource(BaseModel):
    """Source attached to an AI response."""

    title: str
    type: str
    url: str | None = None


class ChatResponse(BaseModel):
    """Response returned by DΞV."""

    response: str
    provider: str
    model: str
    session_id: str | None = None
    sources: list[ChatSource] = Field(default_factory=list)


@router.post("", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    """Generate an AI response using DΞV."""

    provider = GroqProvider()

    result = provider.generate(
        prompt=request.message,
        system_prompt=DEV_SYSTEM_PROMPT,
    )

    return ChatResponse(
        response=result.content,
        provider=result.provider,
        model=result.model,
        session_id=request.session_id,
        sources=[],
    )