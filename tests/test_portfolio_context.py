from backend.services.portfolio_service import PortfolioKnowledgeService


def test_portfolio_context_contains_core_information():
    service = PortfolioKnowledgeService()

    context = service.build_context()

    assert "DΞV PORTFOLIO KNOWLEDGE" in context
    assert "Devendra Khanal" in context
    assert "AI/ML Developer" in context
    assert "Python" in context
    assert "TensorFlow" in context
    assert "Brain Tumor Analyzer" in context
    assert "RAG Hallucination Detector" in context
    assert "BSc.CSIT" in context
    assert "Remote Sensing for Coastal Change Detection" in context


def test_portfolio_context_contains_project_details():
    service = PortfolioKnowledgeService()

    context = service.build_context()

    assert "EfficientNetB3" in context
    assert "Lightweight U-Net" in context
    assert "Streamlit" in context
    assert "brain-tumor-classification-35.streamlit.app" in context
