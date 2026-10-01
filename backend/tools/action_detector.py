from dataclasses import dataclass

from backend.models.actions import PortfolioActionType
from backend.rag.query_classifier import detect_project_category
from backend.services.portfolio_service import (
    PortfolioKnowledgeService,
)


@dataclass(frozen=True)
class DetectedAction:
    """A detected portfolio action intent."""

    type: PortfolioActionType
    value: str | None = None


class PortfolioActionDetector:
    """Detect safe portfolio actions from natural language."""

    def __init__(
        self,
        knowledge_service: PortfolioKnowledgeService | None = None,
    ) -> None:
        self.knowledge_service = (
            knowledge_service
            or PortfolioKnowledgeService()
        )

    def detect(
        self,
        query: str,
    ) -> DetectedAction | None:
        """Detect a safe portfolio action."""

        normalized = query.lower().strip()

        if not normalized:
            raise ValueError("Query cannot be empty.")

        project_action = self._detect_project(normalized)

        if project_action:
            return project_action

        category = detect_project_category(normalized)

        action_terms = (
            "show",
            "filter",
            "display",
            "view",
            "list",
        )

        project_terms = (
            "projects",
            "project",
        )

        if (
            category
            and any(
                term in normalized
                for term in action_terms
            )
            and any(
                term in normalized
                for term in project_terms
            )
        ):
            return DetectedAction(
                type=PortfolioActionType.FILTER_PROJECTS,
                value=category,
            )

        github_terms = (
            "open github",
            "go to github",
            "take me to github",
            "github profile",
        )

        if any(
            term in normalized
            for term in github_terms
        ):
            return DetectedAction(
                type=PortfolioActionType.OPEN_GITHUB,
            )

        resume_terms = (
            "download resume",
            "download my resume",
            "download cv",
            "download my cv",
            "download cv",
            "get resume",
            "get cv",
            "view resume",
            "view cv",
            "show resume",
            "show cv",
        )

        if any(
            term in normalized
            for term in resume_terms
        ):
            return DetectedAction(
                type=PortfolioActionType.DOWNLOAD_RESUME,
            )

        contact_terms = (
            "contact devendra",
            "contact me",
            "contact",
            "get in touch",
        )

        if any(
            term in normalized
            for term in contact_terms
        ):
            return DetectedAction(
                type=PortfolioActionType.OPEN_CONTACT,
            )

        section_terms = {
            "projects": (
                "projects section",
                "project section",
                "go to projects",
                "show projects section",
            ),
            "skills": (
                "skills section",
                "skill section",
                "go to skills",
            ),
            "about": (
                "about section",
                "go to about",
            ),
            "contact": (
                "contact section",
                "go to contact",
            ),
        }

        for section, terms in section_terms.items():
            if any(
                term in normalized
                for term in terms
            ):
                return DetectedAction(
                    type=PortfolioActionType.SCROLL_TO_SECTION,
                    value=section,
                )

        return None

    def _detect_project(
        self,
        normalized_query: str,
    ) -> DetectedAction | None:
        """Detect a specific project mentioned in a query."""

        project_action_terms = (
            "open",
            "view",
            "show me",
            "tell me about",
            "take me to",
        )

        if not any(
            term in normalized_query
            for term in project_action_terms
        ):
            return None

        projects = self.knowledge_service.get_projects()

        for project in projects:
            project_name = project.name.lower()

            if project_name in normalized_query:
                return DetectedAction(
                    type=PortfolioActionType.OPEN_PROJECT,
                    value=project.id,
                )

        return None


def detect_action(query: str) -> DetectedAction | None:
    """Backward-compatible action detection helper."""

    detector = PortfolioActionDetector()

    return detector.detect(query)

