from backend.rag.chunking import TextChunker


def test_chunker_creates_chunks():
    text = " ".join(
        f"word{i}"
        for i in range(250)
    )

    chunker = TextChunker(
        chunk_size=100,
        chunk_overlap=20,
    )

    chunks = chunker.split(
        text,
        metadata={"source": "portfolio"},
    )

    assert len(chunks) == 3

    assert chunks[0].chunk_id == "chunk-0"
    assert chunks[1].chunk_id == "chunk-1"
    assert chunks[2].chunk_id == "chunk-2"

    assert chunks[0].metadata["source"] == "portfolio"
    assert chunks[0].metadata["chunk_index"] == "0"


def test_chunker_preserves_overlap():
    text = " ".join(
        f"word{i}"
        for i in range(150)
    )

    chunker = TextChunker(
        chunk_size=100,
        chunk_overlap=20,
    )

    chunks = chunker.split(text)

    first_words = chunks[0].text.split()
    second_words = chunks[1].text.split()

    assert first_words[-20:] == second_words[:20]


def test_chunker_handles_empty_text():
    chunker = TextChunker()

    assert chunker.split("") == []


def test_chunker_rejects_invalid_configuration():
    try:
        TextChunker(
            chunk_size=20,
            chunk_overlap=20,
        )
        assert False
    except ValueError:
        pass
