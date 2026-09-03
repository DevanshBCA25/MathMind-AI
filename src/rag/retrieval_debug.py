from typing import Any, Dict, List

from src.rag.config import TOP_K


class RetrievalDebugger:
    """
    Debug utility for inspecting actual FAISS retrieval scores.

    IMPORTANT:
    This module does NOT modify the existing RAG pipeline.
    It only reads retrieval results and analyzes them.
    """

    def __init__(self, retriever):
        self.retriever = retriever

    def analyze_query(
        self,
        query: str,
        k: int = TOP_K,
    ) -> Dict[str, Any]:

        if not query or not query.strip():
            return {
                "query": query,
                "results": [],
                "overall_confidence": "low",
            }

        # Get actual FAISS distance scores.
        results = (
            self.retriever.similarity_search_with_score(
                query=query,
                k=k,
            )
        )

        analyzed_results: List[Dict[str, Any]] = []

        for index, (
            document,
            score,
        ) in enumerate(results):

            score = float(score)

            confidence = self._classify_score(
                score
            )

            metadata = document.metadata or {}

            analyzed_results.append(
                {
                    "rank": index + 1,
                    "score": score,
                    "confidence": confidence,
                    "source": metadata.get(
                        "source",
                        "Unknown",
                    ),
                    "page": metadata.get(
                        "page",
                        None,
                    ),
                    "content": document.page_content,
                }
            )

        overall_confidence = (
            self._overall_confidence(
                analyzed_results
            )
        )

        return {
            "query": query,
            "results": analyzed_results,
            "overall_confidence": overall_confidence,
        }

    @staticmethod
    def _classify_score(
        score: float,
    ) -> str:

        # These are ONLY initial observation bands.
        # They are NOT final production thresholds.

        if score <= 0.6:
            return "high"

        if score <= 1.2:
            return "medium"

        return "low"

    @staticmethod
    def _overall_confidence(
        results: List[Dict[str, Any]],
    ) -> str:

        if not results:
            return "low"

        confidences = [
            result["confidence"]
            for result in results
        ]

        if "high" in confidences:
            return "high"

        if "medium" in confidences:
            return "medium"

        return "low"

    @staticmethod
    def print_report(
        report: Dict[str, Any],
    ):

        print()
        print("=" * 60)
        print("MathMind-AI Retrieval Debug Report")
        print("=" * 60)

        print(
            f"\nQuestion: {report['query']}"
        )

        print(
            f"Overall Confidence: "
            f"{report['overall_confidence'].upper()}"
        )

        results = report["results"]

        if not results:

            print(
                "\nNo documents were retrieved."
            )

            print("=" * 60)

            return

        print(
            f"\nRetrieved Documents: {len(results)}"
        )

        for result in results:

            print()
            print(
                f"Rank: {result['rank']}"
            )

            print(
                f"Score: {result['score']:.4f}"
            )

            print(
                f"Confidence: "
                f"{result['confidence'].upper()}"
            )

            print(
                f"Source: {result['source']}"
            )

            print(
                f"Page: {result['page']}"
            )

            content = (
                result["content"]
                .replace("\n", " ")
                .strip()
            )

            if len(content) > 200:
                content = content[:200] + "..."

            print(
                f"Content: {content}"
            )

        print()
        print("=" * 60)


def main():

    print(
        "Retrieval debugger module loaded successfully."
    )

    print(
        "Use RetrievalDebugger with your existing "
        "RetrieverEngine instance."
    )


if __name__ == "__main__":
    main()