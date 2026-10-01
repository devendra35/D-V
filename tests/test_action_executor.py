import pytest

from backend.models.actions import PortfolioActionType
from backend.tools.action_executor import (
    PortfolioActionExecutor,
)


@pytest.fixture
def executor():
    return PortfolioActionExecutor()


@pytest.mark.parametrize(
    ("query", "expected_type"),
    [
        (
            "Show me AI projects",
            PortfolioActionType.FILTER_PROJECTS,
        ),
        (
            "Open Brain Tumor Analyzer",
            PortfolioActionType.OPEN_PROJECT,
        ),
        (
            "Take me to GitHub",
            PortfolioActionType.OPEN_GITHUB,
        ),
        (
            "Contact Devendra",
            PortfolioActionType.OPEN_CONTACT,
        ),
        (
            "Go to the projects section",
            PortfolioActionType.SCROLL_TO_SECTION,
        ),
    ],
)
def test_execute_creates_valid_action(
    executor,
    query,
    expected_type,
):
    action = executor.execute(query)

    assert action is not None
    assert action.type == expected_type


def test_open_project_contains_real_project_id(executor):
    action = executor.execute(
        "Open Brain Tumor Analyzer"
    )

    assert action is not None
    assert action.type == PortfolioActionType.OPEN_PROJECT
    assert action.project_id == "brain-tumor-analyzer"


def test_filter_action_contains_category(executor):
    action = executor.execute(
        "Show me AI projects"
    )

    assert action is not None
    assert action.type == PortfolioActionType.FILTER_PROJECTS
    assert action.category == "AI/ML"


def test_unknown_request_returns_none(executor):
    assert executor.execute(
        "Tell me about Devendra"
    ) is None


def test_unknown_project_does_not_create_action(executor):
    assert executor.execute(
        "Open Unknown Project"
    ) is None
def test_execute_download_resume():
    executor = PortfolioActionExecutor()

    result = executor.execute("Download my resume")

    assert result is not None
    assert result.type == PortfolioActionType.DOWNLOAD_RESUME
