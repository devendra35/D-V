from fastapi import APIRouter

from backend.services.portfolio_service import PortfolioKnowledgeService


router = APIRouter(
    prefix="/skills",
    tags=["Skills"],
)


knowledge_service = PortfolioKnowledgeService()


@router.get("")
async def get_skills():
    """Return all portfolio skills."""

    return knowledge_service.get_skills()
