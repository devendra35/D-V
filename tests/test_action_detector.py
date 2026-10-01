import pytest

from backend.models.actions import PortfolioActionType
from backend.tools.action_detector import (
    PortfolioActionDetector,
    detect_action,
)


@pytest.fixture
def detector():
    return PortfolioActionDetector()


@pytest.mark.parametrize(
    ("query", "expected_type", "expected_value"),
    [
        (
            "Show me AI projects",
            PortfolioActionType.FILTER_PROJECTS,
            "AI/ML",
        ),
        (
            "Filter machine learning projects",
            PortfolioActionType.FILTER_PROJECTS,
            "AI/ML",
        ),
        (
            "Open GitHub",
            PortfolioActionType.OPEN_GITHUB,
            None,
        ),
        (
            "Take me to GitHub",
            PortfolioActionType.OPEN_GITHUB,
            None,
        ),
        (
            "Contact Devendra",
            PortfolioActionType.OPEN_CONTACT,
            None,
        ),
        (
            "Go to the projects section",
            PortfolioActionType.SCROLL_TO_SECTION,
            "projects",
        ),
        (
            "Go to skills",
            PortfolioActionType.SCROLL_TO_SECTION,
            "skills",
        ),
    ],
)
def test_detect_action(
    detector,
    query,
    expected_type,
    expected_value,
):
    action = detector.detect(query)

    assert action is not None
    assert action.type == expected_type
    assert action.value == expected_value


@pytest.mark.parametrize(
    ("query", "expected_project"),
    [
        (
            "Open Brain Tumor Analyzer",
            "brain-tumor-analyzer",
        ),
        (
            "Show me the RAG Hallucination Detector",
            "rag-hallucination-detector",
        ),
        (
            "Take me to Dev Store",
            "dev-store",
        ),
    ],
)
def test_detect_specific_project(
    detector,
    query,
    expected_project,
):
    action = detector.detect(query)

    assert action is not None
    assert action.type == PortfolioActionType.OPEN_PROJECT
    assert action.value == expected_project


def test_unknown_request_returns_none(detector):
    assert detector.detect(
        "Tell me about Devendra"
    ) is None


def test_unknown_project_returns_none(detector):
    assert detector.detect(
        "Open Unknown Project"
    ) is None


def test_empty_query_is_rejected(detector):
    with pytest.raises(ValueError):
        detector.detect("")


def test_backward_compatible_helper():
    action = detect_action("Open Brain Tumor Analyzer")

    assert action is not None
    assert action.type == PortfolioActionType.OPEN_PROJECT
    assert action.value == "brain-tumor-analyzer"
from backend.models.actions import PortfolioActionType
from backend.tools.action_detector import PortfolioActionDetector


def test_detect_download_resume():
    detector = PortfolioActionDetector()

    result = detector.detect("Download my resume")

    assert result is not None
    assert result.type == PortfolioActionType.DOWNLOAD_RESUME


def test_detect_download_cv():
    detector = PortfolioActionDetector()

    result = detector.detect("Download my CV")

    assert result is not None
    assert result.type == PortfolioActionType.DOWNLOAD_RESUME
