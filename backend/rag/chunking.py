from dataclasses import dataclass


@dataclass(frozen=True)
class DocumentChunk:
    """A searchable piece of portfolio knowledge."""

    chunk_id: str
    text: str
    metadata: dict[str, str]


class TextChunker:
    """Split text into overlapping word-based chunks."""

    def __init__(
        self,
        chunk_size: int = 120,
        chunk_overlap: int = 20,
    ) -> None:
        if chunk_size <= 0:
            raise ValueError("chunk_size must be greater than 0.")

        if chunk_overlap < 0:
            raise ValueError("chunk_overlap cannot be negative.")

        if chunk_overlap >= chunk_size:
            raise ValueError(
                "chunk_overlap must be smaller than chunk_size."
            )

        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def split(
        self,
        text: str,
        metadata: dict[str, str] | None = None,
    ) -> list[DocumentChunk]:
        """Split text into deterministic overlapping chunks."""

        cleaned_text = " ".join(text.split())

        if not cleaned_text:
            return []

        words = cleaned_text.split()

        chunks: list[DocumentChunk] = []

        step = self.chunk_size - self.chunk_overlap

        for start in range(0, len(words), step):
            chunk_words = words[
                start : start + self.chunk_size
            ]

            if not chunk_words:
                break

            chunk_text = " ".join(chunk_words)

            chunk_metadata = dict(metadata or {})
            chunk_metadata["chunk_index"] = str(
                len(chunks)
            )

            chunks.append(
                DocumentChunk(
                    chunk_id=f"chunk-{len(chunks)}",
                    text=chunk_text,
                    metadata=chunk_metadata,
                )
            )

            if start + self.chunk_size >= len(words):
                break

        return chunks
