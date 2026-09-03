from typing import Any, Dict, Optional

from src.rag.pipeline import RAGPipeline
from src.agents.agent_graph import MathMindAgentGraph


class RAGAgentGraph:
    """
    Document-Aware Multi-Agent Mathematical Reasoning System.

    Workflow:

        User Question
             ↓
        RAG Retrieval
             ↓
        Relevant Context
             ↓
        Planner
             ↓
        Solver
             ↓
        Reviewer
             ↓
        Teacher
             ↓
        Final Answer
    """

    def __init__(
        self,
        vector_db,
        provider: str = "Gemini",
        retrieval_method: str = "similarity",
        top_k: int = 4,
        rag_pipeline: Optional[RAGPipeline] = None,
    ):

        self.provider = provider
        self.retrieval_method = retrieval_method
        self.top_k = top_k

        # --------------------------------------------------
        # RAG Pipeline
        # --------------------------------------------------

        if rag_pipeline is not None:

            self.rag_pipeline = rag_pipeline

        else:

            self.rag_pipeline = RAGPipeline(
                vector_db=vector_db,
                provider=provider,
                retrieval_method=retrieval_method,
                top_k=top_k,
            )

        # --------------------------------------------------
        # Agent Graph
        # --------------------------------------------------

        self.agent_graph = MathMindAgentGraph(
            provider=provider
        )

    # ======================================================
    # PROVIDER
    # ======================================================

    def set_provider(
        self,
        provider: str,
    ) -> None:

        self.provider = provider

        self.rag_pipeline.change_provider(
            provider
        )

        self.agent_graph.set_provider(
            provider
        )

    # ======================================================
    # RETRIEVAL SETTINGS
    # ======================================================

    def set_retrieval_method(
        self,
        method: str,
    ) -> None:

        if method not in [
            "similarity",
            "mmr",
        ]:

            raise ValueError(
                "Unsupported retrieval method. "
                "Use 'similarity' or 'mmr'."
            )

        self.retrieval_method = method

        self.rag_pipeline.change_retrieval_method(
            method
        )

    def set_top_k(
        self,
        top_k: int,
    ) -> None:

        if top_k < 1:

            raise ValueError(
                "top_k must be greater than zero."
            )

        self.top_k = top_k

        self.rag_pipeline.top_k = top_k

    # ======================================================
    # RETRIEVE CONTEXT
    # ======================================================

    def retrieve_context(
        self,
        question: str,
    ) -> Dict[str, Any]:

        if not question or not question.strip():

            return {
                "status": "ERROR",
                "question": question,
                "documents": [],
                "sources": [],
                "context": "",
                "message": (
                    "Question cannot be empty."
                ),
            }

        try:

            documents = (
                self.rag_pipeline.retrieve(
                    question
                )
            )

            if not documents:

                return {
                    "status": "NO_CONTEXT",
                    "question": question,
                    "documents": [],
                    "sources": [],
                    "context": "",
                    "message": (
                        "No relevant document "
                        "context was found."
                    ),
                }

            context = (
                self.rag_pipeline.build_context(
                    documents
                )
            )

            sources = (
                self.rag_pipeline.retriever
                .format_sources(
                    documents
                )
            )

            return {
                "status": "SUCCESS",
                "question": question,
                "documents": documents,
                "sources": sources,
                "context": context,
            }

        except Exception as error:

            return {
                "status": "ERROR",
                "question": question,
                "documents": [],
                "sources": [],
                "context": "",
                "message": str(error),
            }

    # ======================================================
    # BUILD AGENT QUESTION WITH CONTEXT
    # ======================================================

    @staticmethod
    def build_agent_question(
        question: str,
        context: str,
    ) -> str:

        if not context:

            return question

        return f"""
You are solving a mathematical problem using
information retrieved from the user's documents.

IMPORTANT:
- Use the document context when it is relevant.
- Do not invent information that is not supported
  by the context.
- You may use mathematical reasoning when required.
- Clearly explain the final result.

USER QUESTION:
{question}

RETRIEVED DOCUMENT CONTEXT:
{context}

Now solve the user's question.
"""

    # ======================================================
    # COMPLETE WORKFLOW
    # ======================================================

    def run(
        self,
        question: str,
    ) -> Dict[str, Any]:

        if not question or not question.strip():

            return {
                "status": "ERROR",
                "question": question,
                "message": (
                    "Question cannot be empty."
                ),
            }

        # --------------------------------------------------
        # STEP 1 — RAG RETRIEVAL
        # --------------------------------------------------

        retrieval = self.retrieve_context(
            question
        )

        if retrieval["status"] == "ERROR":

            return {
                "status": "RAG_ERROR",
                "question": question,
                "retrieval": retrieval,
                "context": "",
                "sources": [],
                "agents": {},
                "final_answer": "",
                "message": retrieval.get(
                    "message",
                    "RAG retrieval failed.",
                ),
            }

        context = retrieval.get(
            "context",
            "",
        )

        sources = retrieval.get(
            "sources",
            [],
        )

        # --------------------------------------------------
        # STEP 2 — BUILD CONTEXT-AWARE QUESTION
        # --------------------------------------------------

        agent_question = (
            self.build_agent_question(
                question=question,
                context=context,
            )
        )

        # --------------------------------------------------
        # STEP 3 — MULTI-AGENT WORKFLOW
        # --------------------------------------------------

        try:

            agent_result = (
                self.agent_graph.run(
                    agent_question
                )
            )

        except Exception as error:

            return {
                "status": "AGENT_ERROR",
                "question": question,
                "retrieval": retrieval,
                "context": context,
                "sources": sources,
                "agents": {},
                "final_answer": "",
                "message": str(error),
            }

        # --------------------------------------------------
        # STEP 4 — FINAL RESULT
        # --------------------------------------------------

        status = agent_result.get(
            "status",
            "UNKNOWN",
        )

        final_answer = agent_result.get(
            "explanation",
            "",
        )

        if not final_answer:

            teacher = agent_result.get(
                "teacher",
                {},
            )

            if isinstance(
                teacher,
                dict,
            ):

                final_answer = teacher.get(
                    "explanation",
                    "",
                )

        return {
            "status": status,
            "question": question,
            "retrieval": retrieval,
            "context": context,
            "sources": sources,
            "agents": agent_result,
            "final_answer": final_answer,
        }

    # ======================================================
    # CLEAR MEMORY
    # ======================================================

    def clear_memory(self) -> None:

        try:

            self.rag_pipeline.clear_memory()

        except Exception:

            pass


__all__ = [
    "RAGAgentGraph",
]