from backend.rag.chunking import DocumentChunk, TextChunker
from backend.rag.documents import PortfolioDocumentBuilder
from backend.rag.embeddings import EmbeddingService
from backend.rag.vectorstore import VectorStore


class PortfolioRAGIndexer:
    """Build the searchable RAG index from structured portfolio documents."""

    def __init__(
        self,
        chunker: TextChunker | None = None,
        embedding_service: EmbeddingService | None = None,
        vector_store: VectorStore | None = None,
        document_builder: PortfolioDocumentBuilder | None = None,
    ) -> None:
        self.document_builder = (
            document_builder
            or PortfolioDocumentBuilder()
        )

        self.chunker = chunker or TextChunker(
            chunk_size=120,
            chunk_overlap=20,
        )

        self.embedding_service = (
            embedding_service or EmbeddingService()
        )

        self.vector_store = (
            vector_store or VectorStore()
        )

    def build(self) -> int:
        """Build the portfolio vector index."""

        documents = (
            self.document_builder.build_documents()
        )

        total_chunks = 0

        for document in documents:
            chunks = self.chunker.split(
                document.text,
                metadata={
                    **document.metadata,
                    "document_id": document.document_id,
                },
            )

            if not chunks:
                continue

            unique_chunks: list[DocumentChunk] = []

            for chunk in chunks:
                unique_chunks.append(
                    DocumentChunk(
                        chunk_id=(
                            f"{document.document_id}"
                            f"-{chunk.chunk_id}"
                        ),
                        text=chunk.text,
                        metadata=chunk.metadata,
                    )
                )

            embeddings = (
                self.embedding_service.embed_documents(
                    [chunk.text for chunk in unique_chunks]
                )
            )

            self.vector_store.add_documents(
                unique_chunks,
                embeddings,
            )

            total_chunks += len(unique_chunks)

        return total_chunks
