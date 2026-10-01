from pydantic import BaseModel, Field


class SocialLink(BaseModel):
    """A public social or professional profile."""

    platform: str
    url: str


class Skill(BaseModel):
    """A portfolio skill."""

    name: str
    description: str | None = None


class SkillCategory(BaseModel):
    """A categorized group of skills."""

    name: str
    description: str | None = None
    skills: list[Skill] = Field(default_factory=list)


class Project(BaseModel):
    """A portfolio project."""

    id: str
    name: str
    description: str
    technologies: list[str] = Field(default_factory=list)
    github_url: str | None = None
    live_url: str | None = None
    category: str | None = None
    highlights: list[str] = Field(default_factory=list)


class Education(BaseModel):
    """An education record."""

    institution: str
    degree: str
    field: str | None = None
    university: str | None = None
    period: str | None = None
    status: str | None = None


class Certificate(BaseModel):
    """A certificate or participation record."""

    name: str
    issuer: str | None = None
    description: str | None = None


class Contact(BaseModel):
    """Public contact information."""

    email: str | None = None
    phone: str | None = None
    location: str | None = None


class PortfolioProfile(BaseModel):
    """Complete portfolio profile."""

    name: str
    headline: str
    location: str | None = None
    bio: str
    date_of_birth: str | None = None

    interests: list[str] = Field(default_factory=list)

    skill_categories: list[SkillCategory] = Field(default_factory=list)

    education: list[Education] = Field(default_factory=list)

    projects: list[Project] = Field(default_factory=list)

    certificates: list[Certificate] = Field(default_factory=list)

    contact: Contact | None = None

    social_links: list[SocialLink] = Field(default_factory=list)
