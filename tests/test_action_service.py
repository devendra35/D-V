import pytest

from backend.models.actions import PortfolioActionType
from backend.services.action_service import PortfolioActionService


@pytest.fixture
def service():
    return PortfolioActionService()


def test_filter_projects(service):
    action = service.filter_projects("AI/ML")

    assert action.type == PortfolioActionType.FILTER_PROJECTS
    assert action.category == "AI/ML"


def test_scroll_to_section(service):
    action = service.scroll_to_section("projects")

    assert action.type == PortfolioActionType.SCROLL_TO_SECTION
    assert action.target == "projects"


def test_open_project(service):
    action = service.open_project(
        "brain-tumor-analyzer"
    )

    assert action.type == PortfolioActionType.OPEN_PROJECT
    assert action.project_id == "brain-tumor-analyzer"


def test_open_github(service):
    action = service.open_github()

    assert action.type == PortfolioActionType.OPEN_GITHUB


def test_open_contact(service):
    action = service.open_contact()

    assert action.type == PortfolioActionType.OPEN_CONTACT


def test_download_resume(service):
    action = service.download_resume()

    assert action.type == PortfolioActionType.DOWNLOAD_RESUME


def test_empty_project_id_is_rejected(service):
    with pytest.raises(ValueError):
        service.open_project("")


def test_empty_section_is_rejected(service):
    with pytest.raises(ValueError):
        service.scroll_to_section("   ")
