from pathlib import Path

from backend.rag.ingestion import PortfolioRAGIndexer
from backend.rag.retrieval import PortfolioRetriever
from backend.rag.vectorstore import VectorStore


def build_test_retriever(tmp_path):
    vector_store = VectorStore(
        persist_directory=str(
            Path(tmp_path) / "vectorstore"
        ),
        collection_name="retrieval_test",
    )

    indexer = PortfolioRAGIndexer(
        vector_store=vector_store,
    )

    indexer.build()

    return PortfolioRetriever(
        embedding_service=indexer.embedding_service,
        vector_store=vector_store,
    )


def test_retriever_finds_brain_tumor_project(tmp_path):
    retriever = build_test_retriever(tmp_path)

    results = retriever.retrieve(
        "Which project uses EfficientNetB3?",
        top_k=3,
    )

    assert len(results) > 0

    combined = " ".join(
        result.text
        for result in results
    )

    assert "Brain Tumor Analyzer" in combined
    assert "EfficientNetB3" in combined


def test_retriever_finds_rag_project(tmp_path):
    retriever = build_test_retriever(tmp_path)

    results = retriever.retrieve(
        "Which project uses Random Forest?",
        top_k=3,
    )

    assert len(results) > 0

    combined = " ".join(
        result.text
        for result in results
    )

    assert "RAG Hallucination Detector" in combined
    assert "Random Forest" in combined


def test_retriever_rejects_empty_query(tmp_path):
    retriever = build_test_retriever(tmp_path)

    try:
        retriever.retrieve("")
        assert False
    except ValueError:
        pass


def test_retriever_rejects_invalid_top_k(tmp_path):
    retriever = build_test_retriever(tmp_path)

    try:
        retriever.retrieve(
            "Python",
            top_k=0,
        )
        assert False
    except ValueError:
        pass

def test_retriever_supports_project_metadata_filter():
    retriever = PortfolioRetriever()

    results = retriever.retrieve(
        "What technologies are used in this project?",
        top_k=3,
        metadata_filter={
            "type": "project",
            "project_id": "brain-tumor-analyzer",
        },
    )

    assert len(results) >= 1

    for result in results:
        assert result.metadata["type"] == "project"
        assert (
            result.metadata["project_id"]
            == "brain-tumor-analyzer"
        )


def test_retriever_supports_single_metadata_filter():
    retriever = PortfolioRetriever()

    results = retriever.retrieve(
        "What AI projects has Devendra built?",
        top_k=5,
        metadata_filter={
            "type": "project",
        },
    )

    assert len(results) >= 1

    for result in results:
        assert result.metadata["type"] == "project"
