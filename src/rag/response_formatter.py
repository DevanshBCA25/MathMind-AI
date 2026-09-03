from typing import Any, Dict, List

from langchain_core.documents import Document


class RAGResponseFormatter:
    """
    Formats RAG answers with source citations,
    confidence information, and safe fallback handling.
    """

    @staticmethod
    def format_sources(
        documents: List[Document],
    ) -> List[Dict[str, Any]]:

        sources = []

        seen = set()

        for index, document in enumerate(documents, start=1):

            metadata = document.metadata or {}

            source = metadata.get(
                "source",
                "Unknown",
            )

            page = metadata.get(
                "page_number",
                None,
            )

            if page is None:

                raw_page = metadata.get(
                    "page",
                    None,
                )

                if raw_page is not None:

                    try:
                        page = int(raw_page) + 1

                    except (
                        TypeError,
                        ValueError,
                    ):

                        page = None

            content = (
                document.page_content or ""
            ).strip()

            key = (
                str(source),
                str(page),
                content,
            )

            if key in seen:
                continue

            seen.add(key)

            sources.append(
                {
                    "citation_id": len(sources) + 1,
                    "source": source,
                    "page": page,
                    "content": content,
                }
            )

        return sources

    @staticmethod
    def add_citations(
        answer: str,
        sources: List[Dict[str, Any]],
    ) -> str:

        if not answer:
            return (
                "I could not generate an answer "
                "from the available documents."
            )

        if not sources:
            return answer

        citation_lines = []

        for source in sources:

            source_name = source.get(
                "source",
                "Unknown",
            )

            page = source.get(
                "page",
                None,
            )

            if page is not None:

                citation_lines.append(
                    f"- [{source['citation_id']}] "
                    f"{source_name} — Page {page}"
                )

            else:

                citation_lines.append(
                    f"- [{source['citation_id']}] "
                    f"{source_name}"
                )

        return (
            f"{answer}\n\n"
            "### 📚 Sources\n"
            + "\n".join(citation_lines)
        )

    @staticmethod
    def safe_answer(
        answer: str,
        documents: List[Document],
    ) -> str:

        if not documents:

            return (
                "I couldn't find relevant information "
                "in the uploaded documents."
            )

        if not answer or not answer.strip():

            return (
                "I found relevant information in the "
                "documents, but I couldn't generate "
                "a reliable answer."
            )

        return answer.strip()