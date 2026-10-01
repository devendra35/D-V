from pathlib import Path

import chromadb

from backend.rag.chunking import DocumentChunk


class VectorStore:
    """Persistent ChromaDB vector store for DΞV knowledge."""

    def __init__(
        self,
        persist_directory: str = "data/vectorstore",
        collection_name: str = "dev_knowledge",
    ) -> None:
        self.persist_directory = Path(
            persist_directory
        )

        self.persist_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.client = chromadb.PersistentClient(
            path=str(self.persist_directory)
        )

        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={
                "description": "DΞV portfolio knowledge"
            },
        )

    def add_documents(
        self,
        chunks: list[DocumentChunk],
        embeddings: list[list[float]],
    ) -> None:
        """Add document chunks and embeddings."""

        if len(chunks) != len(embeddings):
            raise ValueError(
                "Chunks and embeddings must have the same length."
            )

        if not chunks:
            return

        self.collection.upsert(
            ids=[
                chunk.chunk_id
                for chunk in chunks
            ],
            documents=[
                chunk.text
                for chunk in chunks
            ],
            embeddings=embeddings,
            metadatas=[
                chunk.metadata
                for chunk in chunks
            ],
        )

    def count(self) -> int:
        """Return the number of stored documents."""

        return self.collection.count()

    def search(
        self,
        embedding: list[float],
        top_k: int = 5,
        metadata_filter: dict | None = None,
    ) -> dict:
        """Search for the most similar documents."""

        if top_k <= 0:
            raise ValueError(
                "top_k must be greater than 0."
            )

        query_kwargs = {
            "query_embeddings": [embedding],
            "n_results": top_k,
        }

        if metadata_filter:
            if len(metadata_filter) == 1:
                key, value = next(
                    iter(metadata_filter.items())
                )

                query_kwargs["where"] = {
                    key: {
                        "$eq": value
                    }
                }

            else:
                query_kwargs["where"] = {
                    "$and": [
                        {
                            key: {
                                "$eq": value
                            }
                        }
                        for key, value in metadata_filter.items()
                    ]
                }

        return self.collection.query(
            **query_kwargs,
        )
