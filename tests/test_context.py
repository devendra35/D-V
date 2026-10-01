from backend.rag.context import RAGContextBuilder
from backend.rag.retrieval import RetrievedDocument


def test_context_builder_creates_grounded_context():
    documents = [
        RetrievedDocument(
            text="Brain Tumor Analyzer uses EfficientNetB3.",
            metadata={
                "source": "portfolio",
                "type": "project",
            },
        ),
        RetrievedDocument(
            text="The project also uses Lightweight U-Net.",
            metadata={
                "source": "portfolio",
                "type": "project",
            },
        ),
    ]

    builder = RAGContextBuilder()

    context = builder.build(documents)

    assert "Brain Tumor Analyzer" in context.text
    assert "EfficientNetB3" in context.text
    assert "Lightweight U-Net" in context.text

    assert len(context.sources) == 2
    assert context.sources[0]["source"] == "portfolio"
    assert context.sources[0]["type"] == "project"


def test_context_builder_preserves_project_source_url():
    documents = [
        RetrievedDocument(
            text="Brain Tumor Analyzer project.",
            metadata={
                "source": "portfolio",
                "type": "project",
                "project_name": "Brain Tumor Analyzer",
                "live_url": (
                    "https://brain-tumor-classification-35.streamlit.app"
                ),
            },
        ),
    ]

    builder = RAGContextBuilder()

    context = builder.build(documents)

    assert len(context.sources) == 1

    source = context.sources[0]

    assert source["source"] == "portfolio"
    assert source["title"] == "Brain Tumor Analyzer"
    assert source["type"] == "project"
    assert (
        source["url"]
        == "https://brain-tumor-classification-35.streamlit.app"
    )


def test_context_builder_handles_empty_documents():
    builder = RAGContextBuilder()

    context = builder.build([])

    assert context.text == (
        "No relevant portfolio knowledge was found."
    )

    assert context.sources == []
