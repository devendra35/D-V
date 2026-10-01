from backend.rag.documents import PortfolioDocumentBuilder


def test_document_builder_creates_logical_documents():
    builder = PortfolioDocumentBuilder()

    documents = builder.build_documents()

    assert len(documents) > 0

    project_documents = [
        document
        for document in documents
        if document.metadata.get("type") == "project"
    ]

    assert len(project_documents) == 5


def test_project_document_contains_project_metadata():
    builder = PortfolioDocumentBuilder()

    documents = builder.build_documents()

    brain_tumor = next(
        document
        for document in documents
        if document.document_id
        == "project-brain-tumor-analyzer"
    )

    assert (
        brain_tumor.metadata["type"]
        == "project"
    )

    assert (
        brain_tumor.metadata["project_id"]
        == "brain-tumor-analyzer"
    )

    assert (
        brain_tumor.metadata["project_name"]
        == "Brain Tumor Analyzer"
    )

    assert "EfficientNetB3" in brain_tumor.text
    assert "Lightweight U-Net" in brain_tumor.text


def test_document_builder_contains_profile_and_skills():
    builder = PortfolioDocumentBuilder()

    documents = builder.build_documents()

    types = {
        document.metadata["type"]
        for document in documents
    }

    assert "profile" in types
    assert "skills" in types
    assert "education" in types
    assert "certificate" in types
    assert "contact" in types
