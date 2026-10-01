from dataclasses import dataclass

from backend.rag.embeddings import EmbeddingService
from backend.rag.query_classifier import (
    QueryType,
    classify_query,
    detect_project_category,
)
from backend.rag.vectorstore import VectorStore


@dataclass(frozen=True)
class RetrievedDocument:
    """A document retrieved from the portfolio knowledge base."""

    text: str
    metadata: dict
    distance: float | None = None


class PortfolioRetriever:
    """Retrieve relevant portfolio knowledge."""

    def __init__(
        self,
        embedding_service: EmbeddingService | None = None,
        vector_store: VectorStore | None = None,
    ) -> None:
        self.embedding_service = (
            embedding_service or EmbeddingService()
        )

        self.vector_store = (
            vector_store or VectorStore()
        )

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
        metadata_filter: dict | None = None,
    ) -> list[RetrievedDocument]:
        """Retrieve relevant portfolio documents."""

        if not query.strip():
            raise ValueError("Query cannot be empty.")

        if top_k <= 0:
            raise ValueError(
                "top_k must be greater than 0."
            )

        effective_filter = metadata_filter

        if effective_filter is None:
            query_type = classify_query(query)

            if query_type == QueryType.PROJECT_LIST:
                category = detect_project_category(query)

                if category:
                    effective_filter = {
                        "type": "project",
                        "category": category,
                    }
                else:
                    effective_filter = {
                        "type": "project",
                    }

        query_embedding = (
            self.embedding_service.embed_text(query)
        )

        results = self.vector_store.search(
            query_embedding,
            top_k=top_k,
            metadata_filter=effective_filter,
        )

        documents = results.get(
            "documents",
            [[]],
        )[0]

        metadatas = results.get(
            "metadatas",
            [[]],
        )[0]

        distances = results.get(
            "distances",
            [[]],
        )[0]

        retrieved: list[RetrievedDocument] = []

        for index, document in enumerate(documents):
            metadata = (
                metadatas[index]
                if index < len(metadatas)
                else {}
            )

            distance = (
                distances[index]
                if index < len(distances)
                else None
            )

            retrieved.append(
                RetrievedDocument(
                    text=document,
                    metadata=metadata,
                    distance=distance,
                )
            )

        return retrieved
