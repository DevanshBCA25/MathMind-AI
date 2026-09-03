from typing import Any, Dict, List, Tuple

from langchain_core.documents import Document


class RelevanceAnalyzer:
    """
    Analyzes retrieved documents and assigns
    a simple retrieval confidence level.

    Lower FAISS distance generally indicates
    a better semantic match.
    """

    def __init__(
        self,
        high_threshold: float = 0.6,
        medium_threshold: float = 1.2,
    ):
        self.high_threshold = high_threshold
        self.medium_threshold = medium_threshold

    def classify_score(
        self,
        score: float,
    ) -> str:
        """
        Classify a FAISS distance score.

        Lower score = better match.
        """

        if score <= self.high_threshold:
            return "high"

        if score <= self.medium_threshold:
            return "medium"

        return "low"

    def analyze(
        self,
        results: List[
            Tuple[Document, float]
        ],
    ) -> List[Dict[str, Any]]:
        """
        Analyze scored retrieval results.
        """

        analyzed = []

        for document, score in results:

            confidence = self.classify_score(
                float(score)
            )

            analyzed.append(
                {
                    "document": document,
                    "score": float(score),
                    "confidence": confidence,
                }
            )

        return analyzed

    def filter_relevant(
        self,
        results: List[
            Tuple[Document, float]
        ],
        minimum_confidence: str = "medium",
    ) -> List[Document]:
        """
        Return documents that meet the requested
        confidence level.

        high:
            only high-confidence documents

        medium:
            high + medium documents

        low:
            all documents
        """

        confidence_order = {
            "high": 3,
            "medium": 2,
            "low": 1,
        }

        minimum_value = confidence_order.get(
            minimum_confidence,
            2,
        )

        analyzed = self.analyze(
            results
        )

        relevant_documents = []

        for item in analyzed:

            current_value = confidence_order[
                item["confidence"]
            ]

            if current_value >= minimum_value:

                relevant_documents.append(
                    item["document"]
                )

        return relevant_documents

    def overall_confidence(
        self,
        results: List[
            Tuple[Document, float]
        ],
    ) -> str:
        """
        Determine overall retrieval confidence.
        """

        if not results:
            return "low"

        analyzed = self.analyze(
            results
        )

        levels = [
            item["confidence"]
            for item in analyzed
        ]

        if "high" in levels:
            return "high"

        if "medium" in levels:
            return "medium"

        return "low"