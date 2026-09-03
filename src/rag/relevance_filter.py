from typing import List, Tuple

from langchain_core.documents import Document


class RelevanceFilter:
    """
    Safe relevance filtering layer for RAG retrieval.

    Lower FAISS distance generally means a better match.

    This filter is intentionally conservative:
    it removes only clearly weak results and keeps
    a fallback to the original retrieval results.
    """

    def __init__(
        self,
        max_distance: float = 1.20,
    ):
        self.max_distance = max_distance

    def filter_results(
        self,
        results: List[
            Tuple[Document, float]
        ],
    ) -> List[Document]:

        if not results:
            return []

        relevant_documents = []

        for document, score in results:

            score = float(score)

            if score <= self.max_distance:

                relevant_documents.append(
                    document
                )

        return self.remove_duplicates(
            relevant_documents
        )

    @staticmethod
    def remove_duplicates(
        documents: List[Document],
    ) -> List[Document]:

        unique_documents = []

        seen = set()

        for document in documents:

            content = (
                document.page_content
                or ""
            ).strip()

            source = document.metadata.get(
                "source",
                "Unknown",
            )

            page = document.metadata.get(
                "page",
                None,
            )

            key = (
                str(source),
                str(page),
                content,
            )

            if key in seen:
                continue

            seen.add(key)

            unique_documents.append(
                document
            )

        return unique_documents