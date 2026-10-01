import pytest
from pydantic import ValidationError

from backend.models.actions import (
    PortfolioAction,
    PortfolioActionType,
)


def test_filter_projects_action():
    action = PortfolioAction(
        type=PortfolioActionType.FILTER_PROJECTS,
        category="AI/ML",
    )

    assert action.type == PortfolioActionType.FILTER_PROJECTS
    assert action.category == "AI/ML"


def test_open_project_action():
    action = PortfolioAction(
        type=PortfolioActionType.OPEN_PROJECT,
        project_id="brain-tumor-analyzer",
    )

    assert action.type == PortfolioActionType.OPEN_PROJECT
    assert action.project_id == "brain-tumor-analyzer"


def test_action_rejects_unknown_type():
    with pytest.raises(ValidationError):
        PortfolioAction(
            type="RUN_ARBITRARY_JAVASCRIPT",
        )
