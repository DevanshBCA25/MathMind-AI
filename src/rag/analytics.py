from datetime import datetime
from typing import Any, Dict, List, Optional


class RAGAnalytics:
    """
    Analytics and monitoring layer for MathMind-AI RAG.

    Tracks:
    - User queries
    - Retrieval information
    - Answer generation
    - Confidence
    - Evaluation metrics
    - Provider and retrieval method
    - Execution timestamps
    """

    def __init__(self):
        self.records: List[Dict[str, Any]] = []

    # ============================================================
    # RECORD QUERY
    # ============================================================

    def record(
        self,
        question: str,
        answer: str = "",
        documents: Optional[List[Any]] = None,
        sources: Optional[List[Dict[str, Any]]] = None,
        evaluation: Optional[Dict[str, Any]] = None,
        confidence: Optional[Dict[str, Any]] = None,
        provider: str = "",
        retrieval_method: str = "",
        retrieval_time: Optional[float] = None,
        generation_time: Optional[float] = None,
    ) -> Dict[str, Any]:

        documents = documents or []
        sources = sources or []
        evaluation = evaluation or {}
        confidence = confidence or {}

        record = {
            "timestamp": datetime.now().isoformat(),

            "question": question,

            "answer": answer,

            "provider": provider,

            "retrieval_method": retrieval_method,

            "retrieval_time": retrieval_time,

            "generation_time": generation_time,

            "retrieved_documents": len(documents),

            "sources": sources,

            "evaluation": evaluation,

            "confidence": confidence,
        }

        self.records.append(record)

        return record

    # ============================================================
    # GET ALL RECORDS
    # ============================================================

    def get_records(self) -> List[Dict[str, Any]]:
        return list(self.records)

    # ============================================================
    # CLEAR RECORDS
    # ============================================================

    def clear(self):
        self.records.clear()

    # ============================================================
    # TOTAL QUERIES
    # ============================================================

    def total_queries(self) -> int:
        return len(self.records)

    # ============================================================
    # AVERAGE RETRIEVAL TIME
    # ============================================================

    def average_retrieval_time(self) -> float:

        values = [
            record["retrieval_time"]
            for record in self.records
            if record.get("retrieval_time") is not None
        ]

        if not values:
            return 0.0

        return round(
            sum(values) / len(values),
            4,
        )

    # ============================================================
    # AVERAGE GENERATION TIME
    # ============================================================

    def average_generation_time(self) -> float:

        values = [
            record["generation_time"]
            for record in self.records
            if record.get("generation_time") is not None
        ]

        if not values:
            return 0.0

        return round(
            sum(values) / len(values),
            4,
        )

    # ============================================================
    # AVERAGE CONFIDENCE
    # ============================================================

    def average_confidence(self) -> float:

        values = [
            record["confidence"].get("score")
            for record in self.records
            if record.get("confidence")
            and record["confidence"].get("score")
            is not None
        ]

        if not values:
            return 0.0

        return round(
            sum(values) / len(values),
            3,
        )

    # ============================================================
    # CONFIDENCE DISTRIBUTION
    # ============================================================

    def confidence_distribution(self) -> Dict[str, int]:

        distribution = {
            "HIGH": 0,
            "MEDIUM": 0,
            "LOW": 0,
        }

        for record in self.records:

            confidence = record.get(
                "confidence",
                {},
            )

            level = confidence.get(
                "level"
            )

            if level in distribution:
                distribution[level] += 1

        return distribution

    # ============================================================
    # PROVIDER STATISTICS
    # ============================================================

    def provider_statistics(self) -> Dict[str, int]:

        statistics: Dict[str, int] = {}

        for record in self.records:

            provider = record.get(
                "provider",
                "Unknown",
            )

            statistics[provider] = (
                statistics.get(provider, 0) + 1
            )

        return statistics

    # ============================================================
    # RETRIEVAL METHOD STATISTICS
    # ============================================================

    def retrieval_statistics(self) -> Dict[str, int]:

        statistics: Dict[str, int] = {}

        for record in self.records:

            method = record.get(
                "retrieval_method",
                "Unknown",
            )

            statistics[method] = (
                statistics.get(method, 0) + 1
            )

        return statistics

    # ============================================================
    # SUMMARY
    # ============================================================

    def summary(self) -> Dict[str, Any]:

        confidence_distribution = (
            self.confidence_distribution()
        )

        return {
            "total_queries": self.total_queries(),

            "average_retrieval_time": (
                self.average_retrieval_time()
            ),

            "average_generation_time": (
                self.average_generation_time()
            ),

            "average_confidence": (
                self.average_confidence()
            ),

            "confidence_distribution": (
                confidence_distribution
            ),

            "provider_statistics": (
                self.provider_statistics()
            ),

            "retrieval_statistics": (
                self.retrieval_statistics()
            ),
        }