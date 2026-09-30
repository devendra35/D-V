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

    def build_context(self) -> str:
        """Build grounded portfolio context for the LLM."""

        profile = self.profile

        lines: list[str] = [
            "DΞV PORTFOLIO KNOWLEDGE",
            "",
            f"Name: {profile.name}",
            f"Headline: {profile.headline}",
            f"Location: {profile.location or 'Not available'}",
            f"Bio: {profile.bio}",
            "",
            "SKILLS:",
        ]

        for category in profile.skill_categories:
            lines.append(f"- {category.name}:")

            for skill in category.skills:
                description = (
                    f" — {skill.description}"
                    if skill.description
                    else ""
                )

                lines.append(
                    f"  - {skill.name}{description}"
                )

        lines.append("")
        lines.append("PROJECTS:")

        for project in profile.projects:
            lines.extend(
                [
                    f"- {project.name}",
                    f"  ID: {project.id}",
                    f"  Description: {project.description}",
                    (
                        "  Technologies: "
                        + ", ".join(project.technologies)
                    ),
                    (
                        "  Category: "
                        + (project.category or "Not specified")
                    ),
                ]
            )

            if project.highlights:
                lines.append("  Highlights:")

                for highlight in project.highlights:
                    lines.append(f"  - {highlight}")

            if project.github_url:
                lines.append(
                    f"  GitHub: {project.github_url}"
                )

            if project.live_url:
                lines.append(
                    f"  Live Demo: {project.live_url}"
                )

        lines.append("")
        lines.append("EDUCATION:")

        for education in profile.education:
            education_line = (
                f"- {education.degree}"
                f" at {education.institution}"
            )

            if education.field:
                education_line += f" ({education.field})"

            if education.university:
                education_line += (
                    f" — {education.university}"
                )

            if education.period:
                education_line += (
                    f" [{education.period}]"
                )

            lines.append(education_line)

        lines.append("")
        lines.append("CERTIFICATES:")

        for certificate in profile.certificates:
            certificate_line = f"- {certificate.name}"

            if certificate.issuer:
                certificate_line += (
                    f" — {certificate.issuer}"
                )

            if certificate.description:
                certificate_line += (
                    f": {certificate.description}"
                )

            lines.append(certificate_line)

        return "\n".join(lines)