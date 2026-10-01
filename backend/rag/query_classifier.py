from enum import Enum


class QueryType(str, Enum):
    """Classify portfolio queries for retrieval strategy."""

    GENERAL = "general"
    PROJECT_LIST = "project_list"
    PROJECT_SPECIFIC = "project_specific"


CATEGORY_ALIASES: dict[str, tuple[str, ...]] = {
    "AI/ML": (
        "ai",
        "artificial intelligence",
        "machine learning",
        "ml",
        "deep learning",
        "computer vision",
    ),
    "Web Development": (
        "web development",
        "web developer",
        "web",
        "frontend",
        "front end",
        "backend",
        "back end",
        "full stack",
        "full-stack",
    ),
    "Data Science": (
        "data science",
        "data scientist",
        "data analysis",
        "data analytics",
    ),
}


def classify_query(query: str) -> QueryType:
    """Classify a portfolio query."""

    normalized = query.lower().strip()

    if not normalized:
        raise ValueError("Query cannot be empty.")

    project_terms = (
        "projects",
        "project",
        "built",
        "developed",
        "created",
        "made",
        "applications",
        "apps",
    )

    has_project_term = any(
        term in normalized
        for term in project_terms
    )

    if has_project_term:
        list_terms = (
            "what",
            "which",
            "list",
            "show",
            "all",
            "built",
            "developed",
            "created",
            "made",
        )

        if any(
            term in normalized
            for term in list_terms
        ):
            return QueryType.PROJECT_LIST

    return QueryType.GENERAL


def detect_project_category(
    query: str,
) -> str | None:
    """Detect a portfolio project category from a query."""

    normalized = query.lower().strip()

    if not normalized:
        raise ValueError("Query cannot be empty.")

    for category, aliases in CATEGORY_ALIASES.items():
        if any(
            alias in normalized
            for alias in aliases
        ):
            return category

    return None
