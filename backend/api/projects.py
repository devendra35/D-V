from fastapi import APIRouter, HTTPException

from backend.services.portfolio_service import PortfolioKnowledgeService


router = APIRouter(
    prefix="/projects",
    tags=["Projects"],
)


knowledge_service = PortfolioKnowledgeService()


@router.get("")
async def get_projects():
    """Return all portfolio projects."""

    return knowledge_service.get_projects()


@router.get("/{project_id}")
async def get_project(project_id: str):
    """Return a single portfolio project by ID."""

    projects = knowledge_service.get_projects()

    for project in projects:
        if project.id == project_id:
            return project

    raise HTTPException(
        status_code=404,
        detail=f"Project '{project_id}' not found.",
    )
