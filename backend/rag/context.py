from dataclasses import dataclass

from backend.rag.retrieval import RetrievedDocument


@dataclass(frozen=True)
class RAGContext:
    """Context assembled from retrieved portfolio knowledge."""

    text: str
    sources: list[dict]


class RAGContextBuilder:
    """Build grounded LLM context from retrieved documents."""

    def build(
        self,
        documents: list[RetrievedDocument],
    ) -> RAGContext:
        """Build context and rich source metadata."""

        if not documents:
            return RAGContext(
                text="No relevant portfolio knowledge was found.",
                sources=[],
            )

        context_parts: list[str] = []
        sources: list[dict] = []

        for index, document in enumerate(
            documents,
            start=1,
        ):
            context_parts.append(
                f"[SOURCE {index}]\n"
                f"{document.text}"
            )

            source = document.metadata.get(
                "source",
                "portfolio",
            )

            source_type = document.metadata.get(
                "type",
                "portfolio",
            )

            source_title = (
                document.metadata.get("project_name")
                or document.metadata.get("category")
                or source
            )

            source_url = document.metadata.get(
                "live_url"
            ) or document.metadata.get(
                "github_url"
            )

            sources.append(
                {
                    "source": source,
                    "title": source_title,
                    "type": source_type,
                    "url": source_url,
                }
            )

        return RAGContext(
            text="\n\n".join(context_parts),
            sources=sources,
        )
