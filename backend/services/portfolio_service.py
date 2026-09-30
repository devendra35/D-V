import json
from pathlib import Path

from backend.models.portfolio import PortfolioProfile


class PortfolioKnowledgeService:
    """Load and provide access to DΞV portfolio knowledge."""

    def __init__(self) -> None:
        self.data_path = (
            Path(__file__).resolve().parent.parent
            / "knowledge"
            / "portfolio.json"
        )

        self.profile = self._load_profile()

    def _load_profile(self) -> PortfolioProfile:
        """Load and validate portfolio knowledge."""

        with self.data_path.open(
            "r",
            encoding="utf-8-sig",
        ) as file:
            data = json.load(file)

        return PortfolioProfile.model_validate(data)

    def get_profile(self) -> PortfolioProfile:
        """Return the complete portfolio profile."""

        return self.profile

    def get_projects(self):
        """Return all portfolio projects."""

        return self.profile.projects

    def get_skills(self) -> list[str]:
        """Return all portfolio skills."""

        return [
            skill.name
            for category in self.profile.skill_categories
            for skill in category.skills
        ]
