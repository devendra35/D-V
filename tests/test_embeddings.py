from backend.rag.embeddings import EmbeddingService


def test_single_embedding():
    service = EmbeddingService()

    embedding = service.embed_text(
        "Brain Tumor Analyzer uses EfficientNetB3."
    )

    assert isinstance(embedding, list)
    assert len(embedding) == 384
    assert all(isinstance(value, float) for value in embedding)


def test_multiple_embeddings():
    service = EmbeddingService()

    embeddings = service.embed_documents(
        [
            "Brain Tumor Analyzer",
            "RAG Hallucination Detector",
        ]
    )

    assert len(embeddings) == 2
    assert len(embeddings[0]) == 384
    assert len(embeddings[1]) == 384


def test_empty_documents():
    service = EmbeddingService()

    assert service.embed_documents([]) == []


def test_empty_text_rejected():
    service = EmbeddingService()

    try:
        service.embed_text("")
        assert False
    except ValueError:
        pass
