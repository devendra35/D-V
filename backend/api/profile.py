from fastapi import APIRouter

from backend.services.portfolio_service import PortfolioKnowledgeService


router = APIRouter(
    prefix="/profile",
    tags=["Profile"],
)


knowledge_service = PortfolioKnowledgeService()


@router.get("")
async def get_profile():
    """Return the complete portfolio profile."""

    return knowledge_service.get_profile()
