from typing import Any, Dict, List, Optional, Tuple

from langchain_core.documents import Document

from src.rag.config import TOP_K


class RetrieverEngine:
    """
    Production-ready retrieval engine for MathMind AI.

    Supports:
        - Similarity search
        - Similarity search with scores
        - MMR search
        - Score filtering
        - Metadata filtering
        - Duplicate removal
        - Source formatting
        - Scored source formatting
    """

    def __init__(self, vector_db):
        self.vector_db = vector_db

    # ========================================================
    # SIMILARITY SEARCH
    # ========================================================

    def similarity_search(
        self,
        query: str,
        k: int = TOP_K,
    ) -> List[Document]:

        if not query or not query.strip():
            return []

        k = max(1, int(k))

        documents = self.vector_db.similarity_search(
            query.strip(),
            k=k,
        )

        return self.remove_duplicates(documents)

    # ========================================================
    # SIMILARITY SEARCH WITH SCORE
    # ========================================================

    def similarity_search_with_score(
        self,
        query: str,
        k: int = TOP_K,
        score_threshold: Optional[float] = None,
    ) -> List[Tuple[Document, float]]:

        if not query or not query.strip():
            return []

        k = max(1, int(k))

        results = (
            self.vector_db.similarity_search_with_score(
                query.strip(),
                k=k,
            )
        )

        cleaned_results = []

        for document, score in results:

            try:
                score = float(score)
            except (TypeError, ValueError):
                continue

            cleaned_results.append(
                (
                    document,
                    score,
                )
            )

        # ----------------------------------------------------
        # FAISS distance:
        #
        # Lower distance = better match
        # ----------------------------------------------------

        if score_threshold is not None:

            cleaned_results = [
                (
                    document,
                    score,
                )
                for document, score in cleaned_results
                if score <= score_threshold
            ]

        return self.remove_duplicate_scored_documents(
            cleaned_results
        )

    # ========================================================
    # MMR SEARCH
    # ========================================================

    def mmr_search(
        self,
        query: str,
        k: int = TOP_K,
        fetch_k: int = 20,
        lambda_mult: float = 0.5,
    ) -> List[Document]:

        if not query or not query.strip():
            return []

        k = max(1, int(k))
        fetch_k = max(k, int(fetch_k))

        lambda_mult = max(
            0.0,
            min(1.0, float(lambda_mult)),
        )

        documents = (
            self.vector_db.max_marginal_relevance_search(
                query.strip(),
                k=k,
                fetch_k=fetch_k,
                lambda_mult=lambda_mult,
            )
        )

        return self.remove_duplicates(
            documents
        )

    # ========================================================
    # GENERAL SEARCH
    # ========================================================

    def search(
        self,
        query: str,
        method: str = "similarity",
        k: int = TOP_K,
    ) -> List[Document]:

        if not query or not query.strip():
            return []

        method = (
            method or "similarity"
        ).lower().strip()

        if method == "mmr":

            return self.mmr_search(
                query=query,
                k=k,
            )

        if method == "similarity":

            return self.similarity_search(
                query=query,
                k=k,
            )

        raise ValueError(
            f"Unsupported retrieval method: {method}. "
            "Supported methods are: similarity, mmr."
        )

    # ========================================================
    # DUPLICATE REMOVAL
    # ========================================================

    @staticmethod
    def remove_duplicates(
        documents: List[Document],
    ) -> List[Document]:
        """
        Remove duplicate chunks.

        Identity:
            source + page + content
        """

        unique_documents = []

        seen = set()

        for document in documents:

            if document is None:
                continue

            metadata = (
                document.metadata
                or {}
            )

            source = metadata.get(
                "source",
                "Unknown",
            )

            page = metadata.get(
                "page",
                metadata.get(
                    "page_number",
                    None,
                ),
            )

            content = (
                document.page_content
                or ""
            ).strip()

            if not content:
                continue

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

    # ========================================================
    # DUPLICATE REMOVAL FOR SCORED RESULTS
    # ========================================================

    @staticmethod
    def remove_duplicate_scored_documents(
        results: List[Tuple[Document, float]],
    ) -> List[Tuple[Document, float]]:
        """
        Remove duplicate documents while
        preserving their FAISS scores.
        """

        unique_results = []

        seen = set()

        for document, score in results:

            if document is None:
                continue

            metadata = (
                document.metadata
                or {}
            )

            source = metadata.get(
                "source",
                "Unknown",
            )

            page = metadata.get(
                "page",
                metadata.get(
                    "page_number",
                    None,
                ),
            )

            content = (
                document.page_content
                or ""
            ).strip()

            if not content:
                continue

            key = (
                str(source),
                str(page),
                content,
            )

            if key in seen:
                continue

            seen.add(key)

            unique_results.append(
                (
                    document,
                    float(score),
                )
            )

        return unique_results

    # ========================================================
    # METADATA FILTERING
    # ========================================================

    def filter_by_metadata(
        self,
        documents: List[Document],
        filters: Optional[
            Dict[str, Any]
        ] = None,
    ) -> List[Document]:

        if not filters:
            return documents

        filtered_documents = []

        for document in documents:

            metadata = (
                document.metadata
                or {}
            )

            matches = all(
                metadata.get(key) == value
                for key, value in filters.items()
            )

            if matches:

                filtered_documents.append(
                    document
                )

        return filtered_documents

    # ========================================================
    # SOURCE FORMATTING
    # ========================================================

    @staticmethod
    def format_sources(
        documents: List[Document],
    ) -> List[Dict[str, Any]]:
        """
        Convert Documents into the
        source structure used by the UI.
        """

        sources = []

        unique_documents = (
            RetrieverEngine.remove_duplicates(
                documents
            )
        )

        for index, document in enumerate(
            unique_documents
        ):

            metadata = (
                document.metadata
                or {}
            )

            page = metadata.get(
                "page",
                None,
            )

            page_number = metadata.get(
                "page_number",
                None,
            )

            if page_number is None and page is not None:

                try:
                    page_number = (
                        int(page) + 1
                    )
                except (
                    TypeError,
                    ValueError,
                ):
                    page_number = None

            sources.append(
                {
                    "index": index + 1,

                    "content": (
                        document.page_content
                    ),

                    "source": metadata.get(
                        "source",
                        "Unknown",
                    ),

                    "page": page,

                    "page_number": page_number,
                }
            )

        return sources

    # ========================================================
    # SCORED SOURCE FORMATTING
    # ========================================================

    @staticmethod
    def format_scored_sources(
        results: List[
            Tuple[Document, float]
        ],
    ) -> List[Dict[str, Any]]:
        """
        Format scored retrieval results.

        Lower FAISS distance generally
        means a better match.
        """

        sources = []

        unique_results = (
            RetrieverEngine.remove_duplicate_scored_documents(
                results
            )
        )

        for index, (
            document,
            score,
        ) in enumerate(
            unique_results
        ):

            metadata = (
                document.metadata
                or {}
            )

            page = metadata.get(
                "page",
                None,
            )

            page_number = metadata.get(
                "page_number",
                None,
            )

            if page_number is None and page is not None:

                try:
                    page_number = (
                        int(page) + 1
                    )
                except (
                    TypeError,
                    ValueError,
                ):
                    page_number = None

            sources.append(
                {
                    "index": index + 1,

                    "content": (
                        document.page_content
                    ),

                    "source": metadata.get(
                        "source",
                        "Unknown",
                    ),

                    "page": page,

                    "page_number": page_number,

                    "score": float(score),
                }
            )

        return sources