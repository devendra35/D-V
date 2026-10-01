from pathlib import Path

from backend.rag.ingestion import PortfolioRAGIndexer
from backend.rag.vectorstore import VectorStore


def test_portfolio_rag_indexer(tmp_path):
    vector_store = VectorStore(
        persist_directory=str(
            Path(tmp_path) / "vectorstore"
        ),
        collection_name="portfolio_test",
    )

    indexer = PortfolioRAGIndexer(
        vector_store=vector_store,
    )

    count = indexer.build()

    assert count > 0
    assert vector_store.count() == count


def test_index_contains_portfolio_information(tmp_path):
    vector_store = VectorStore(
        persist_directory=str(
            Path(tmp_path) / "vectorstore"
        ),
        collection_name="portfolio_test",
    )

    indexer = PortfolioRAGIndexer(
        vector_store=vector_store,
    )

    indexer.build()

    query_embedding = (
        indexer.embedding_service.embed_text(
            "What project uses EfficientNetB3?"
        )
    )

    results = vector_store.search(
        query_embedding,
        top_k=3,
    )

    documents = results["documents"][0]

    combined = " ".join(documents)

    assert "Brain Tumor Analyzer" in combined
    assert "EfficientNetB3" in combined
