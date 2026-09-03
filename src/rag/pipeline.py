from typing import Any, Dict, List, Optional

from langchain_core.documents import Document

from src.rag.retriever import RetrieverEngine
from src.rag.relevance_filter import RelevanceFilter
from src.rag.memory import ConversationMemory
from src.rag.prompt_template import build_rag_prompt
from src.rag.response_formatter import RAGResponseFormatter
from src.llm.router import LLMRouter


class RAGPipeline:
    """
    Complete RAG Pipeline.

    Workflow:

        Question
            ↓
        Retriever
            ↓
        Relevance Filter
            ↓
        Context Builder
            ↓
        Prompt
            ↓
        LLM Router
            ↓
        Response Formatter
            ↓
        Answer + Sources
            ↓
        Conversation Memory
    """

    SUPPORTED_PROVIDERS = [
        "OpenAI",
        "Gemini",
        "Groq",
        "Ollama",
    ]

    SUPPORTED_RETRIEVAL_METHODS = [
        "similarity",
        "mmr",
    ]

    def __init__(
        self,
        vector_db,
        provider: str = "Gemini",
        retrieval_method: str = "similarity",
        top_k: int = 4,
        memory: Optional[
            ConversationMemory
        ] = None,
    ):

        if vector_db is None:

            raise ValueError(
                "vector_db cannot be None."
            )

        self.vector_db = vector_db

        self.provider = provider

        self.retrieval_method = (
            retrieval_method
        )

        self.top_k = int(top_k)

        if self.top_k < 1:

            raise ValueError(
                "top_k must be at least 1."
            )

        # ======================================================
        # RETRIEVER
        # ======================================================

        self.retriever = RetrieverEngine(
            vector_db
        )

        # ======================================================
        # RELEVANCE FILTER
        # ======================================================

        self.relevance_filter = (
            RelevanceFilter(
                max_distance=1.20
            )
        )

        # ======================================================
        # LLM ROUTER
        # ======================================================

        self.router = LLMRouter()

        # ======================================================
        # RESPONSE FORMATTER
        # ======================================================

        self.response_formatter = (
            RAGResponseFormatter()
        )

        # ======================================================
        # MEMORY
        # ======================================================

        self.memory = (
            memory
            if memory is not None
            else ConversationMemory(
                max_messages=10
            )
        )

        # Validate settings

        self.change_provider(
            provider
        )

        self.change_retrieval_method(
            retrieval_method
        )

    # ==========================================================
    # RETRIEVAL
    # ==========================================================

    def retrieve(
        self,
        question: str,
    ) -> List[Document]:

        if not question or not question.strip():

            return []

        # ------------------------------------------------------
        # SIMILARITY
        # ------------------------------------------------------

        if (
            self.retrieval_method
            == "similarity"
        ):

            scored_results = (
                self.retriever
                .similarity_search_with_score(
                    query=question,
                    k=self.top_k,
                )
            )

            filtered_documents = (
                self.relevance_filter
                .filter_results(
                    scored_results
                )
            )

            # Safe fallback

            if filtered_documents:

                return filtered_documents

            return [
                document
                for document, _ in scored_results
            ]

        # ------------------------------------------------------
        # MMR
        # ------------------------------------------------------

        return self.retriever.search(
            query=question,
            method=self.retrieval_method,
            k=self.top_k,
        )

    # ==========================================================
    # BUILD CONTEXT
    # ==========================================================

    @staticmethod
    def build_context(
        documents: List[Document],
    ) -> str:

        if not documents:

            return ""

        context_parts = []

        for index, document in enumerate(
            documents
        ):

            metadata = (
                document.metadata
                or {}
            )

            source = metadata.get(
                "source",
                metadata.get(
                    "file_name",
                    "Unknown",
                ),
            )

            page_number = metadata.get(
                "page_number"
            )

            if page_number is None:

                page = metadata.get(
                    "page"
                )

                if page is not None:

                    try:

                        page_number = (
                            int(page) + 1
                        )

                    except (
                        TypeError,
                        ValueError,
                    ):

                        page_number = None

            if page_number is not None:

                source_info = (
                    f"Source: {source}, "
                    f"Page: {page_number}"
                )

            else:

                source_info = (
                    f"Source: {source}"
                )

            content = (
                document.page_content
                or ""
            ).strip()

            if not content:

                continue

            context_parts.append(
                (
                    f"[Document Chunk {index + 1}]\n"
                    f"{source_info}\n\n"
                    f"{content}"
                )
            )

        return "\n\n".join(
            context_parts
        )

    # ==========================================================
    # GENERATE ANSWER
    # ==========================================================

    def generate_answer(
        self,
        question: str,
        documents: List[Document],
    ) -> str:

        context = self.build_context(
            documents
        )

        history = (
            self.memory
            .get_formatted_history()
        )

        prompt = build_rag_prompt(
            question=question,
            context=context,
            chat_history=history,
        )

        answer = self.router.ask(
            provider=self.provider,
            prompt=prompt,
        )

        answer = (
            self.response_formatter
            .safe_answer(
                answer,
                documents,
            )
        )

        return answer

    # ==========================================================
    # ASK
    # ==========================================================

    def ask(
        self,
        question: str,
    ) -> Dict[str, Any]:

        if not question or not question.strip():

            return {
                "answer": (
                    "Please enter a question."
                ),
                "documents": [],
                "sources": [],
                "provider": self.provider,
                "retrieval_method": (
                    self.retrieval_method
                ),
                "top_k": self.top_k,
                "status": "INVALID_INPUT",
            }

        question = question.strip()

        # ------------------------------------------------------
        # RETRIEVE
        # ------------------------------------------------------

        try:

            documents = self.retrieve(
                question
            )

        except Exception as error:

            return {
                "answer": "",
                "documents": [],
                "sources": [],
                "provider": self.provider,
                "retrieval_method": (
                    self.retrieval_method
                ),
                "top_k": self.top_k,
                "status": "RETRIEVAL_ERROR",
                "message": str(error),
            }

        # ------------------------------------------------------
        # NO CONTEXT
        # ------------------------------------------------------

        if not documents:

            return {
                "answer": (
                    "I couldn't find relevant "
                    "information in the uploaded "
                    "documents."
                ),
                "documents": [],
                "sources": [],
                "provider": self.provider,
                "retrieval_method": (
                    self.retrieval_method
                ),
                "top_k": self.top_k,
                "status": "NO_CONTEXT",
            }

        # ------------------------------------------------------
        # GENERATE ANSWER
        # ------------------------------------------------------

        try:

            answer = self.generate_answer(
                question=question,
                documents=documents,
            )

        except Exception as error:

            return {
                "answer": "",
                "documents": documents,
                "sources": [],
                "provider": self.provider,
                "retrieval_method": (
                    self.retrieval_method
                ),
                "top_k": self.top_k,
                "status": "API_ERROR",
                "message": str(error),
            }

        # ------------------------------------------------------
        # MEMORY
        # ------------------------------------------------------

        try:

            self.memory.add_user_message(
                question
            )

            self.memory.add_assistant_message(
                answer
            )

        except Exception:
            pass

        # ------------------------------------------------------
        # SOURCES
        # ------------------------------------------------------

        try:

            sources = (
                self.retriever
                .format_sources(
                    documents
                )
            )

        except Exception:

            sources = []

        # ------------------------------------------------------
        # FINAL RESULT
        # ------------------------------------------------------

        return {
            "answer": answer,
            "documents": documents,
            "sources": sources,
            "provider": self.provider,
            "retrieval_method": (
                self.retrieval_method
            ),
            "top_k": self.top_k,
            "status": "SUCCESS",
        }

    # ==========================================================
    # CLEAR MEMORY
    # ==========================================================

    def clear_memory(self):

        self.memory.clear()

    # ==========================================================
    # CHANGE PROVIDER
    # ==========================================================

    def change_provider(
        self,
        provider: str,
    ):

        if provider not in (
            self.SUPPORTED_PROVIDERS
        ):

            raise ValueError(
                f"Unsupported provider: "
                f"{provider}. "
                f"Supported providers: "
                f"{', '.join(self.SUPPORTED_PROVIDERS)}"
            )

        self.provider = provider

    # ==========================================================
    # CHANGE RETRIEVAL METHOD
    # ==========================================================

    def change_retrieval_method(
        self,
        method: str,
    ):

        if method not in (
            self.SUPPORTED_RETRIEVAL_METHODS
        ):

            raise ValueError(
                f"Unsupported retrieval method: "
                f"{method}. "
                f"Supported methods: "
                f"{', '.join(self.SUPPORTED_RETRIEVAL_METHODS)}"
            )

        self.retrieval_method = method

    # ==========================================================
    # CHANGE TOP-K
    # ==========================================================

    def change_top_k(
        self,
        top_k: int,
    ):

        top_k = int(top_k)

        if top_k < 1:

            raise ValueError(
                "top_k must be at least 1."
            )

        self.top_k = top_k