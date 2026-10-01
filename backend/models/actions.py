from enum import Enum

from pydantic import BaseModel, Field


class PortfolioActionType(str, Enum):
    """Safe actions DΞV can request from the portfolio frontend."""

    FILTER_PROJECTS = "FILTER_PROJECTS"
    SCROLL_TO_SECTION = "SCROLL_TO_SECTION"
    OPEN_PROJECT = "OPEN_PROJECT"
    OPEN_GITHUB = "OPEN_GITHUB"
    OPEN_CONTACT = "OPEN_CONTACT"
    DOWNLOAD_RESUME = "DOWNLOAD_RESUME"


class PortfolioAction(BaseModel):
    """A validated action that the frontend may execute."""

    type: PortfolioActionType
    target: str | None = Field(
        default=None,
        max_length=200,
    )
    project_id: str | None = Field(
        default=None,
        max_length=100,
    )
    category: str | None = Field(
        default=None,
        max_length=100,
    )


class ActionResponse(BaseModel):
    """Structured action response returned by DΞV."""

    action: PortfolioAction | None = None
