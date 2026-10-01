from backend.models.actions import PortfolioAction
from backend.services.action_service import PortfolioActionService
from backend.tools.action_detector import (
    DetectedAction,
    PortfolioActionDetector,
)


class PortfolioActionExecutor:
    """Convert detected intents into validated portfolio actions."""

    def __init__(
        self,
        detector: PortfolioActionDetector | None = None,
        action_service: PortfolioActionService | None = None,
    ) -> None:
        self.detector = (
            detector
            or PortfolioActionDetector()
        )

        self.action_service = (
            action_service
            or PortfolioActionService()
        )

    def execute(
        self,
        query: str,
    ) -> PortfolioAction | None:
        """Detect and validate a portfolio action."""

        detected = self.detector.detect(query)

        if detected is None:
            return None

        return self._build_action(detected)

    def _build_action(
        self,
        detected: DetectedAction,
    ) -> PortfolioAction:
        """Convert a detected action into a validated action."""

        if detected.type.value == "FILTER_PROJECTS":
            return self.action_service.filter_projects(
                detected.value
            )

        if detected.type.value == "OPEN_PROJECT":
            if not detected.value:
                raise ValueError(
                    "OPEN_PROJECT requires a project ID."
                )

            return self.action_service.open_project(
                detected.value
            )

        if detected.type.value == "OPEN_GITHUB":
            return self.action_service.open_github()

        if detected.type.value == "OPEN_CONTACT":
            return self.action_service.open_contact()

        if detected.type.value == "DOWNLOAD_RESUME":
            return self.action_service.download_resume()

        if detected.type.value == "SCROLL_TO_SECTION":
            if not detected.value:
                raise ValueError(
                    "SCROLL_TO_SECTION requires a section."
                )

            return self.action_service.scroll_to_section(
                detected.value
            )

        raise ValueError(
            f"Unsupported action type: {detected.type}"
        )
