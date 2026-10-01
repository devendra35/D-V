import pytest

from backend.rag.query_classifier import (
    QueryType,
    classify_query,
    detect_project_category,
)


@pytest.mark.parametrize(
    ("query", "expected"),
    [
        (
            "What AI and machine learning projects has Devendra built?",
            QueryType.PROJECT_LIST,
        ),
        (
            "What projects has Devendra created?",
            QueryType.PROJECT_LIST,
        ),
        (
            "Show me all projects",
            QueryType.PROJECT_LIST,
        ),
        (
            "Which projects has Devendra developed?",
            QueryType.PROJECT_LIST,
        ),
        (
            "Tell me about Brain Tumor Analyzer",
            QueryType.GENERAL,
        ),
        (
            "What skills does Devendra have?",
            QueryType.GENERAL,
        ),
        (
            "Tell me about Devendra",
            QueryType.GENERAL,
        ),
    ],
)
def test_classify_query(
    query: str,
    expected: QueryType,
):
    assert classify_query(query) == expected


@pytest.mark.parametrize(
    ("query", "expected"),
    [
        (
            "AI and machine learning projects",
            "AI/ML",
        ),
        (
            "What artificial intelligence projects has Devendra built?",
            "AI/ML",
        ),
        (
            "Show me his deep learning projects",
            "AI/ML",
        ),
        (
            "web development projects",
            "Web Development",
        ),
        (
            "Show me his full stack projects",
            "Web Development",
        ),
        (
            "data science projects",
            "Data Science",
        ),
        (
            "What projects has Devendra built?",
            None,
        ),
    ],
)
def test_detect_project_category(
    query: str,
    expected: str | None,
):
    assert detect_project_category(query) == expected


def test_empty_query_is_rejected():
    with pytest.raises(ValueError):
        classify_query("")


def test_empty_category_query_is_rejected():
    with pytest.raises(ValueError):
        detect_project_category("")
