from backend.services.portfolio_service import PortfolioKnowledgeService


def test_portfolio_knowledge_loads():
    service = PortfolioKnowledgeService()

    profile = service.get_profile()

    assert profile.name == "Devendra Khanal"
    assert len(profile.projects) == 5
    assert len(profile.skill_categories) == 4
    assert len(profile.education) == 3
    assert len(profile.certificates) == 3


def test_project_lookup_from_knowledge():
    service = PortfolioKnowledgeService()

    projects = service.get_projects()

    project_ids = [project.id for project in projects]

    assert "brain-tumor-analyzer" in project_ids
    assert "rag-hallucination-detector" in project_ids


def test_skills_from_knowledge():
    service = PortfolioKnowledgeService()

    skills = service.get_skills()

    assert len(skills) == 29
    assert "Python" in skills
    assert "TensorFlow" in skills
    assert "React" in skills
