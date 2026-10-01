from sentence_transformers import SentenceTransformer


class EmbeddingService:
    """Generate vector embeddings for DΞV knowledge."""

    def __init__(
        self,
        model_name: str = "all-MiniLM-L6-v2",
    ) -> None:
        self.model_name = model_name
        self.model = SentenceTransformer(model_name)

    def embed_text(self, text: str) -> list[float]:
        """Generate an embedding for a single text."""

        if not text.strip():
            raise ValueError("Text cannot be empty.")

        embedding = self.model.encode(
            text,
            normalize_embeddings=True,
        )

        return embedding.tolist()

    def embed_documents(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        """Generate embeddings for multiple documents."""

        if not texts:
            return []

        if any(not text.strip() for text in texts):
            raise ValueError(
                "Documents cannot contain empty text."
            )

        embeddings = self.model.encode(
            texts,
            normalize_embeddings=True,
        )

        return embeddings.tolist()
