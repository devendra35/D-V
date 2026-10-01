from backend.rag.chunking import DocumentChunk
from backend.rag.embeddings import EmbeddingService
from backend.rag.vectorstore import VectorStore


def test_vector_store_add_and_search(tmp_path):
    chunks = [
        DocumentChunk(
            chunk_id="test-1",
            text="Brain Tumor Analyzer uses EfficientNetB3.",
            metadata={
                "source": "portfolio",
                "type": "project",
            },
        ),
        DocumentChunk(
            chunk_id="test-2",
            text="RAG Hallucination Detector uses Random Forest.",
            metadata={
                "source": "portfolio",
                "type": "project",
            },
        ),
    ]

    embedding_service = EmbeddingService()

    embeddings = embedding_service.embed_documents(
        [chunk.text for chunk in chunks]
    )

    store = VectorStore(
        persist_directory=str(tmp_path / "vectorstore"),
        collection_name="test_collection",
    )

    store.add_documents(
        chunks,
        embeddings,
    )

    assert store.count() == 2

    query_embedding = embedding_service.embed_text(
        "What project uses EfficientNetB3?"
    )

    results = store.search(
        query_embedding,
        top_k=1,
    )

    assert len(results["documents"]) == 1
    assert len(results["documents"][0]) == 1

    assert (
        "Brain Tumor Analyzer"
        in results["documents"][0][0]
    )


def test_vector_store_rejects_mismatched_data(tmp_path):
    store = VectorStore(
        persist_directory=str(tmp_path / "vectorstore"),
        collection_name="test_collection",
    )

    chunks = [
        DocumentChunk(
            chunk_id="test-1",
            text="Example",
            metadata={},
        )
    ]

    try:
        store.add_documents(
            chunks,
            [],
        )
        assert False
    except ValueError:
        pass


def test_vector_store_empty_insert(tmp_path):
    store = VectorStore(
        persist_directory=str(tmp_path / "vectorstore"),
        collection_name="test_collection",
    )

    store.add_documents([], [])

    assert store.count() == 0
