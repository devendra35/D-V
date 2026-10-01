from backend.models.actions import (
    PortfolioAction,
    PortfolioActionType,
)
from backend.services.portfolio_service import (
    PortfolioKnowledgeService,
)


class PortfolioActionService:
    """Create safe, validated actions for the portfolio frontend."""

    def __init__(
        self,
        knowledge_service: PortfolioKnowledgeService | None = None,
    ) -> None:
        self.knowledge_service = (
            knowledge_service
            or PortfolioKnowledgeService()
        )

    def filter_projects(
        self,
        category: str | None = None,
    ) -> PortfolioAction:
        """Create a project filtering action."""

        return PortfolioAction(
            type=PortfolioActionType.FILTER_PROJECTS,
            category=category,
        )

    def scroll_to_section(
        self,
        section: str,
    ) -> PortfolioAction:
        """Create a section navigation action."""

        if not section.strip():
            raise ValueError(
                "Section cannot be empty."
            )

        return PortfolioAction(
            type=PortfolioActionType.SCROLL_TO_SECTION,
            target=section.strip(),
        )

    def open_project(
        self,
        project_id: str,
    ) -> PortfolioAction:
        """Create an action for an existing portfolio project."""

        if not project_id.strip():
            raise ValueError(
                "Project ID cannot be empty."
            )

        normalized_id = project_id.strip().lower()

        project = next(
            (
                project
                for project in self.knowledge_service.get_projects()
                if project.id.lower() == normalized_id
            ),
            None,
        )

        if project is None:
            raise ValueError(
                f"Unknown portfolio project: {project_id}"
            )

        return PortfolioAction(
            type=PortfolioActionType.OPEN_PROJECT,
            project_id=project.id,
        )

    def open_github(self) -> PortfolioAction:
        """Create a GitHub navigation action."""

        return PortfolioAction(
            type=PortfolioActionType.OPEN_GITHUB,
        )

    def open_contact(self) -> PortfolioAction:
        """Create a contact navigation action."""

        return PortfolioAction(
            type=PortfolioActionType.OPEN_CONTACT,
        )

    def download_resume(self) -> PortfolioAction:
        """Create a resume download action."""

        return PortfolioAction(
            type=PortfolioActionType.DOWNLOAD_RESUME,
        )
