from dataclasses import dataclass

from backend.services.portfolio_service import PortfolioKnowledgeService


@dataclass(frozen=True)
class RAGDocument:
    """A logical knowledge document for RAG."""

    document_id: str
    text: str
    metadata: dict[str, str]


class PortfolioDocumentBuilder:
    """Build logical RAG documents from portfolio knowledge."""

    def __init__(
        self,
        knowledge_service: PortfolioKnowledgeService | None = None,
    ) -> None:
        self.knowledge_service = (
            knowledge_service
            or PortfolioKnowledgeService()
        )

    def build_documents(self) -> list[RAGDocument]:
        """Build structured documents from the portfolio."""

        profile = self.knowledge_service.get_profile()

        documents: list[RAGDocument] = []

        documents.append(
            RAGDocument(
                document_id="profile",
                text=(
                    f"Name: {profile.name}\n"
                    f"Headline: {profile.headline}\n"
                    f"Location: {profile.location}\n"
                    f"Bio: {profile.bio}\n"
                    f"Interests: {', '.join(profile.interests)}"
                ),
                metadata={
                    "source": "portfolio",
                    "type": "profile",
                },
            )
        )

        for category in profile.skill_categories:
            skills = "\n".join(
                f"- {skill.name}: {skill.description or 'No description'}"
                for skill in category.skills
            )

            documents.append(
                RAGDocument(
                    document_id=(
                        "skill-"
                        + category.name.lower()
                        .replace(" ", "-")
                        .replace("&", "and")
                    ),
                    text=(
                        f"Skill Category: {category.name}\n"
                        f"Description: "
                        f"{category.description or 'No description'}\n"
                        f"Skills:\n{skills}"
                    ),
                    metadata={
                        "source": "portfolio",
                        "type": "skills",
                        "category": category.name,
                    },
                )
            )

        for project in profile.projects:
            technologies = ", ".join(
                project.technologies
            )

            highlights = "\n".join(
                f"- {highlight}"
                for highlight in project.highlights
            )

            project_text = (
                f"Project: {project.name}\n"
                f"Project ID: {project.id}\n"
                f"Description: {project.description}\n"
                f"Category: {project.category or 'Not specified'}\n"
                f"Technologies: {technologies}\n"
                f"Highlights:\n{highlights}"
            )

            if project.github_url:
                project_text += (
                    f"\nGitHub: {project.github_url}"
                )

            if project.live_url:
                project_text += (
                    f"\nLive Demo: {project.live_url}"
                )

            project_metadata = {
                "source": "portfolio",
                "type": "project",
                "project_id": project.id,
                "project_name": project.name,
                "category": (
                    project.category
                    or "Not specified"
                ),
            }

            if project.live_url:
                project_metadata["live_url"] = project.live_url

            if project.github_url:
                project_metadata["github_url"] = project.github_url

            documents.append(
                RAGDocument(
                    document_id=f"project-{project.id}",
                    text=project_text,
                    metadata=project_metadata,
                )
            )

        for index, education in enumerate(
            profile.education
        ):
            documents.append(
                RAGDocument(
                    document_id=f"education-{index}",
                    text=(
                        f"Degree: {education.degree}\n"
                        f"Institution: {education.institution}\n"
                        f"Field: "
                        f"{education.field or 'Not specified'}\n"
                        f"University: "
                        f"{education.university or 'Not specified'}\n"
                        f"Period: "
                        f"{education.period or 'Not specified'}\n"
                        f"Status: "
                        f"{education.status or 'Not specified'}"
                    ),
                    metadata={
                        "source": "portfolio",
                        "type": "education",
                        "institution": education.institution,
                    },
                )
            )

        for index, certificate in enumerate(
            profile.certificates
        ):
            documents.append(
                RAGDocument(
                    document_id=f"certificate-{index}",
                    text=(
                        f"Certificate: {certificate.name}\n"
                        f"Issuer: "
                        f"{certificate.issuer or 'Not specified'}\n"
                        f"Description: "
                        f"{certificate.description or 'Not specified'}"
                    ),
                    metadata={
                        "source": "portfolio",
                        "type": "certificate",
                        "certificate_name": certificate.name,
                    },
                )
            )

        if profile.contact:
            documents.append(
                RAGDocument(
                    document_id="contact",
                    text=(
                        f"Email: "
                        f"{profile.contact.email or 'Not available'}\n"
                        f"Phone: "
                        f"{profile.contact.phone or 'Not available'}\n"
                        f"Location: "
                        f"{profile.contact.location or 'Not available'}"
                    ),
                    metadata={
                        "source": "portfolio",
                        "type": "contact",
                    },
                )
            )

        return documents
