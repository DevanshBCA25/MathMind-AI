from typing import Any, Dict, Optional

from src.agents.agent_graph import MathMindAgentGraph


class AgentRAGIntegration:
    """
    Integration layer between the Agent Graph and RAG Pipeline.

    The class keeps both systems independent while providing
    one common interface for the Streamlit application.
    """

    def __init__(
        self,
        rag_pipeline=None,
        agent_graph=None,
    ):
        self.rag_pipeline = rag_pipeline

        self.agent_graph = (
            agent_graph
            if agent_graph is not None
            else MathMindAgentGraph()
        )

    def set_rag_pipeline(
        self,
        rag_pipeline,
    ):
        """Attach or replace the RAG pipeline."""

        self.rag_pipeline = rag_pipeline

    def set_agent_graph(
        self,
        agent_graph,
    ):
        """Attach or replace the Agent Graph."""

        self.agent_graph = agent_graph

    @staticmethod
    def _is_document_question(
        question: str,
    ) -> bool:
        """
        Detect whether the question appears to be asking
        about uploaded documents.

        This is intentionally conservative.
        """

        text = question.lower()

        document_keywords = [
            "according to the document",
            "according to the pdf",
            "according to my document",
            "in the document",
            "in the pdf",
            "uploaded document",
            "uploaded pdf",
            "from the document",
            "from the pdf",
            "what does the document say",
            "what does the pdf say",
        ]

        return any(
            keyword in text
            for keyword in document_keywords
        )

    def run_agent(
        self,
        question: str,
    ) -> Dict[str, Any]:
        """Run the normal Agent Graph."""

        if not question or not question.strip():

            return {
                "status": "ERROR",
                "answer": "Please enter a question.",
                "mode": "agent",
            }

        try:

            result = self.agent_graph.run(
                question.strip()
            )

            if isinstance(result, dict):

                result.setdefault(
                    "mode",
                    "agent",
                )

                result.setdefault(
                    "status",
                    "SUCCESS",
                )

                return result

            return {
                "status": "SUCCESS",
                "mode": "agent",
                "final_answer": str(result),
            }

        except Exception as error:

            return {
                "status": "ERROR",
                "mode": "agent",
                "answer": "",
                "error": str(error),
            }

    def run_rag(
        self,
        question: str,
    ) -> Dict[str, Any]:
        """Run the RAG pipeline."""

        if self.rag_pipeline is None:

            return {
                "status": "UNAVAILABLE",
                "mode": "rag",
                "answer": (
                    "No RAG pipeline is currently loaded."
                ),
                "sources": [],
            }

        try:

            result = self.rag_pipeline.ask(
                question.strip()
            )

            if isinstance(result, dict):

                result.setdefault(
                    "mode",
                    "rag",
                )

                result.setdefault(
                    "status",
                    "SUCCESS",
                )

                return result

            return {
                "status": "SUCCESS",
                "mode": "rag",
                "answer": str(result),
                "sources": [],
            }

        except Exception as error:

            return {
                "status": "ERROR",
                "mode": "rag",
                "answer": "",
                "sources": [],
                "error": str(error),
            }

    def run(
        self,
        question: str,
        mode: str = "auto",
    ) -> Dict[str, Any]:
        """
        Main integration entry point.

        Modes:
        - auto
        - agent
        - rag
        """

        if not question or not question.strip():

            return {
                "status": "ERROR",
                "mode": "unknown",
                "answer": "Please enter a question.",
                "sources": [],
            }

        question = question.strip()

        # --------------------------------------------------
        # AUTO MODE
        # --------------------------------------------------

        if mode == "auto":

            if self.rag_pipeline is not None and (
                self._is_document_question(
                    question
                )
            ):

                result = self.run_rag(
                    question
                )

                if result.get("status") == "SUCCESS":

                    return result

                # Safe fallback to Agent Graph
                return self.run_agent(
                    question
                )

            return self.run_agent(
                question
            )

        # --------------------------------------------------
        # EXPLICIT RAG
        # --------------------------------------------------

        if mode == "rag":

            return self.run_rag(
                question
            )

        # --------------------------------------------------
        # EXPLICIT AGENT
        # --------------------------------------------------

        if mode == "agent":

            return self.run_agent(
                question
            )

        return {
            "status": "ERROR",
            "mode": mode,
            "answer": "",
            "sources": [],
            "error": (
                "Unsupported mode. "
                "Use 'auto', 'agent' or 'rag'."
            ),
        }


__all__ = [
    "AgentRAGIntegration",
]