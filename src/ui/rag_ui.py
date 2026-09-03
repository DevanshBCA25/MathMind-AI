import shutil
from pathlib import Path

import streamlit as st

from src.rag.config import (
    DOCUMENTS_DIR,
    VECTOR_DB_DIR,
    TOP_K,
)

from src.rag.document_loader import (
    DocumentLoader,
)

from src.rag.chunking import (
    Chunker,
)

from src.rag.vector_store import (
    VectorDatabase,
)

from src.rag.pipeline import (
    RAGPipeline,
)

from src.rag.memory import (
    ConversationMemory,
)

from src.rag.evaluation_runner import (
    RAGEvaluationRunner,
)

from src.rag.evaluation_dataset import (
    TEST_DATASET,
)


# ============================================================
# DIRECTORY SETUP
# ============================================================

def initialize_directories():

    Path(DOCUMENTS_DIR).mkdir(
        parents=True,
        exist_ok=True,
    )

    Path(VECTOR_DB_DIR).mkdir(
        parents=True,
        exist_ok=True,
    )


# ============================================================
# SESSION STATE
# ============================================================

def initialize_session_state():

    if "rag_pipeline" not in st.session_state:
        st.session_state.rag_pipeline = None

    if "rag_chat_history" not in st.session_state:
        st.session_state.rag_chat_history = []

    if "db_ready" not in st.session_state:
        st.session_state.db_ready = False

    if "uploaded_files" not in st.session_state:
        st.session_state.uploaded_files = []

    if "rag_evaluation_report" not in st.session_state:
        st.session_state.rag_evaluation_report = None


# ============================================================
# SAVE UPLOADED FILES
# ============================================================

def save_uploaded_files(uploaded_files):

    saved_files = []

    for uploaded_file in uploaded_files:

        file_path = (
            Path(DOCUMENTS_DIR)
            / uploaded_file.name
        )

        with open(file_path, "wb") as file:

            file.write(
                uploaded_file.getbuffer()
            )

        saved_files.append(
            str(file_path)
        )

    return saved_files


# ============================================================
# BUILD VECTOR DATABASE
# ============================================================

def build_vector_database():

    pdf_files = sorted(
        Path(DOCUMENTS_DIR).glob("*.pdf")
    )

    if not pdf_files:

        st.warning(
            "No PDF documents found. "
            "Please upload and save a PDF first."
        )

        return None

    loader = DocumentLoader()
    chunker = Chunker()

    all_chunks = []

    progress = st.progress(0)

    for index, pdf_file in enumerate(pdf_files):

        try:

            documents = loader.load(
                str(pdf_file)
            )

            if not documents:

                st.warning(
                    f"{pdf_file.name}: "
                    "No text could be extracted."
                )

                progress.progress(
                    (index + 1) / len(pdf_files)
                )

                continue

            valid_documents = [
                doc
                for doc in documents
                if doc.page_content
                and doc.page_content.strip()
            ]

            if not valid_documents:

                st.warning(
                    f"{pdf_file.name}: "
                    "No readable text found."
                )

                progress.progress(
                    (index + 1) / len(pdf_files)
                )

                continue

            # ------------------------------------------------
            # Document metadata
            # ------------------------------------------------

            for doc in valid_documents:

                metadata = dict(
                    doc.metadata or {}
                )

                metadata["source"] = (
                    pdf_file.name
                )

                metadata["file_name"] = (
                    pdf_file.name
                )

                if "page" in metadata:

                    try:

                        metadata["page_number"] = (
                            int(
                                metadata["page"]
                            ) + 1
                        )

                    except (
                        TypeError,
                        ValueError,
                    ):

                        pass

                doc.metadata = metadata

            # ------------------------------------------------
            # Chunk documents
            # ------------------------------------------------

            chunks = chunker.split(
                valid_documents
            )

            # ------------------------------------------------
            # Chunk metadata
            # ------------------------------------------------

            for chunk in chunks:

                metadata = dict(
                    chunk.metadata or {}
                )

                metadata["source"] = (
                    pdf_file.name
                )

                metadata["file_name"] = (
                    pdf_file.name
                )

                if "page" in metadata:

                    try:

                        metadata["page_number"] = (
                            int(
                                metadata["page"]
                            ) + 1
                        )

                    except (
                        TypeError,
                        ValueError,
                    ):

                        pass

                chunk.metadata = metadata

            all_chunks.extend(
                chunks
            )

        except Exception as error:

            st.error(
                f"Failed to process "
                f"{pdf_file.name}: {error}"
            )

        progress.progress(
            (index + 1) / len(pdf_files)
        )

    progress.empty()

    # ========================================================
    # VALIDATE CHUNKS
    # ========================================================

    if not all_chunks:

        st.error(
            "No document chunks were created."
        )

        return None

    # ========================================================
    # CREATE FAISS DATABASE
    # ========================================================

    try:

        vector_db_manager = (
            VectorDatabase()
        )

        vector_db = (
            vector_db_manager.create(
                all_chunks
            )
        )

        vector_db_manager.save(
            vector_db,
            str(VECTOR_DB_DIR),
        )

        st.success(
            "✅ Vector database created successfully!"
        )

        st.info(
            f"📄 PDFs: {len(pdf_files)} | "
            f"🧩 Chunks: {len(all_chunks)}"
        )

        return vector_db

    except Exception as error:

        st.error(
            f"❌ Vector database creation failed: "
            f"{error}"
        )

        return None


# ============================================================
# LOAD VECTOR DATABASE
# ============================================================

def load_vector_database():

    vector_db_manager = (
        VectorDatabase()
    )

    if not vector_db_manager.exists(
        VECTOR_DB_DIR
    ):

        return None

    try:

        vector_db = (
            vector_db_manager.load(
                str(VECTOR_DB_DIR)
            )
        )

        return vector_db

    except Exception as error:

        st.error(
            f"Failed to load vector database: "
            f"{error}"
        )

        return None


# ============================================================
# CREATE RAG PIPELINE
# ============================================================

def create_pipeline(
    vector_db,
    provider,
    retrieval_method,
    top_k,
):

    memory = ConversationMemory(
        max_messages=10
    )

    pipeline = RAGPipeline(

        vector_db=vector_db,

        provider=provider,

        retrieval_method=retrieval_method,

        top_k=top_k,

        memory=memory,
    )

    return pipeline


# ============================================================
# SIDEBAR
# ============================================================

def render_sidebar():

    st.sidebar.title(
        "⚙️ RAG Settings"
    )

    # --------------------------------------------------------
    # DOCUMENTS
    # --------------------------------------------------------

    st.sidebar.markdown(
        "### 📚 Documents"
    )

    uploaded_files = (
        st.sidebar.file_uploader(
            "Upload PDF documents",
            type=["pdf"],
            accept_multiple_files=True,
        )
    )

    if uploaded_files:

        if st.sidebar.button(
            "💾 Save Documents",
            use_container_width=True,
        ):

            saved = (
                save_uploaded_files(
                    uploaded_files
                )
            )

            st.session_state.uploaded_files = (
                saved
            )

            st.sidebar.success(
                f"{len(saved)} document(s) saved."
            )

    st.sidebar.divider()

    # --------------------------------------------------------
    # PROVIDER
    # --------------------------------------------------------

    st.sidebar.markdown(
        "### 🤖 LLM Provider"
    )

    provider = st.sidebar.selectbox(

        "Choose Provider",

        [
            "Gemini",
            "OpenAI",
            "Groq",
            "Ollama",
        ],

        key="rag_provider",
    )

    st.sidebar.divider()

    # --------------------------------------------------------
    # RETRIEVAL
    # --------------------------------------------------------

    st.sidebar.markdown(
        "### 🔎 Retrieval"
    )

    retrieval_method = (
        st.sidebar.selectbox(

            "Search Method",

            [
                "similarity",
                "mmr",
            ],

            key="rag_retrieval_method",
        )
    )

    top_k = st.sidebar.slider(

        "Top-K Documents",

        min_value=1,

        max_value=10,

        value=TOP_K,

        key="rag_top_k",
    )

    st.sidebar.divider()

    # --------------------------------------------------------
    # VECTOR DATABASE
    # --------------------------------------------------------

    st.sidebar.markdown(
        "### 🗄️ Vector Database"
    )

    if st.sidebar.button(
        "🔨 Build / Rebuild Database",
        use_container_width=True,
    ):

        with st.spinner(
            "Building vector database..."
        ):

            vector_db = (
                build_vector_database()
            )

        if vector_db is not None:

            st.session_state.rag_pipeline = (
                create_pipeline(
                    vector_db,
                    provider,
                    retrieval_method,
                    top_k,
                )
            )

            st.session_state.db_ready = True

            st.sidebar.success(
                "Database ready!"
            )

    if st.sidebar.button(
        "📂 Load Existing Database",
        use_container_width=True,
    ):

        with st.spinner(
            "Loading vector database..."
        ):

            vector_db = (
                load_vector_database()
            )

        if vector_db is not None:

            st.session_state.rag_pipeline = (
                create_pipeline(
                    vector_db,
                    provider,
                    retrieval_method,
                    top_k,
                )
            )

            st.session_state.db_ready = True

            st.sidebar.success(
                "Vector database loaded."
            )

    # --------------------------------------------------------
    # DELETE DATABASE
    # --------------------------------------------------------

    if st.sidebar.button(
        "🗑️ Delete Vector Database",
        use_container_width=True,
    ):

        vector_path = Path(
            VECTOR_DB_DIR
        )

        if vector_path.exists():

            shutil.rmtree(
                vector_path
            )

        vector_path.mkdir(
            parents=True,
            exist_ok=True,
        )

        st.session_state.rag_pipeline = None

        st.session_state.db_ready = False

        st.session_state.rag_evaluation_report = None

        st.sidebar.success(
            "Vector database deleted."
        )

    st.sidebar.divider()

    # --------------------------------------------------------
    # CLEAR CHAT
    # --------------------------------------------------------

    if st.sidebar.button(
        "🧹 Clear RAG Chat",
        use_container_width=True,
    ):

        st.session_state.rag_chat_history = []

        st.session_state.rag_evaluation_report = None

        if st.session_state.rag_pipeline:

            st.session_state.rag_pipeline.clear_memory()

        st.rerun()

    return (
        provider,
        retrieval_method,
        top_k,
    )


# ============================================================
# DOCUMENT INFORMATION
# ============================================================

def render_document_info():

    documents = list(
        Path(DOCUMENTS_DIR).glob("*.pdf")
    )

    with st.expander(
        "📚 Uploaded Documents",
        expanded=False,
    ):

        if not documents:

            st.info(
                "No PDF documents uploaded."
            )

            return

        for document in documents:

            st.write(
                f"📄 {document.name}"
            )


# ============================================================
# SOURCES
# ============================================================

def render_sources(
    sources,
):

    if not sources:
        return

    st.markdown("### 📚 Sources")

    for source in sources:

        citation_id = source.get(
            "citation_id",
            0,
        )

        source_name = source.get(
            "source",
            "Unknown",
        )

        page = source.get(
            "page",
            None,
        )

        content = source.get(
            "content",
            "",
        )

        if page is not None:

            title = (
                f"📄 [{citation_id}] "
                f"{source_name} — Page {page}"
            )

        else:

            title = (
                f"📄 [{citation_id}] "
                f"{source_name}"
            )

        with st.expander(title):

            if page is not None:

                st.caption(
                    f"Source: {source_name} | "
                    f"Page: {page}"
                )

            st.write(content)

# ============================================================
# CHAT DISPLAY
# ============================================================

def render_chat():

    for message in (
        st.session_state.rag_chat_history
    ):

        role = message["role"]

        content = message["content"]

        with st.chat_message(role):

            st.markdown(content)


# ============================================================
# CHAT EXPORT
# ============================================================

def generate_chat_text():

    lines = []

    for message in (
        st.session_state.rag_chat_history
    ):

        role = message["role"].upper()

        lines.append(
            f"{role}:\n"
            f"{message['content']}\n"
        )

    return "\n".join(lines)


# ============================================================
# MAIN RAG CHAT
# ============================================================

def render_chat_interface(
    provider,
    retrieval_method,
    top_k,
):

    st.subheader(
        "💬 Ask Your Documents"
    )

    st.caption(
        f"Provider: {provider} | "
        f"Retrieval: {retrieval_method} | "
        f"Top-K: {top_k}"
    )

    # --------------------------------------------------------
    # DATABASE STATUS
    # --------------------------------------------------------

    if st.session_state.db_ready:

        st.success(
            "🟢 RAG database is ready."
        )

    else:

        st.warning(
            "🟡 Build or load a vector database first."
        )

    # --------------------------------------------------------
    # CHAT HISTORY
    # --------------------------------------------------------

    render_chat()

    question = st.chat_input(
        "Ask a question about your documents..."
    )

    if not question:

        return

    pipeline = (
        st.session_state.rag_pipeline
    )

    if pipeline is None:

        st.warning(
            "Please build or load a vector "
            "database first."
        )

        return

    # --------------------------------------------------------
    # USER MESSAGE
    # --------------------------------------------------------

    st.session_state.rag_chat_history.append(
        {
            "role": "user",
            "content": question,
        }
    )

    with st.chat_message("user"):

        st.markdown(question)

    # --------------------------------------------------------
    # RAG RESPONSE
    # --------------------------------------------------------

    with st.chat_message("assistant"):

        with st.spinner(
            "🔎 Searching documents..."
        ):

            try:

                pipeline.change_provider(
                    provider
                )

                pipeline.change_retrieval_method(
                    retrieval_method
                )

                pipeline.top_k = top_k

                result = pipeline.ask(
                    question
                )

                answer = result.get(
                    "answer",
                    "No answer generated.",
                )

                sources = result.get(
                    "sources",
                    [],
                )

                st.markdown(
                    answer
                )

                render_sources(
                    sources
                )

                st.session_state.rag_chat_history.append(
                    {
                        "role": "assistant",
                        "content": answer,
                    }
                )

            except Exception as error:

                st.error(
                    f"RAG Error: {error}"
                )


# ============================================================
# RETRIEVAL-ONLY TEST
# ============================================================

def render_retrieval_test():

    with st.expander(
        "🔎 Retrieval Test",
        expanded=False,
    ):

        st.caption(
            "Test FAISS retrieval without calling an LLM."
        )

        pipeline = (
            st.session_state.rag_pipeline
        )

        if pipeline is None:

            st.info(
                "Build or load the vector database first."
            )

            return

        query = st.text_input(
            "Test retrieval query",
            placeholder="e.g. What is the area of a rectangle?",
            key="retrieval_test_query",
        )

        if st.button(
            "🔍 Search FAISS",
            use_container_width=True,
            key="retrieval_test_button",
        ):

            if not query.strip():

                st.warning(
                    "Enter a query first."
                )

                return

            try:

                documents = pipeline.retrieve(
                    query
                )

                st.success(
                    f"Retrieved {len(documents)} document chunk(s)."
                )

                for index, document in enumerate(
                    documents,
                    start=1,
                ):

                    source = document.metadata.get(
                        "source",
                        "Unknown",
                    )

                    page = document.metadata.get(
                        "page",
                        None,
                    )

                    st.markdown(
                        f"### Result {index}"
                    )

                    st.write(
                        f"**Source:** {source}"
                    )

                    if page is not None:

                        st.write(
                            f"**Page:** {int(page) + 1}"
                        )

                    st.write(
                        document.page_content
                    )

                    st.divider()

            except Exception as error:

                st.error(
                    f"Retrieval test failed: {error}"
                )


# ============================================================
# RAG EVALUATION
# ============================================================

def run_rag_evaluation(pipeline):

    runner = RAGEvaluationRunner(
        pipeline
    )

    progress = st.progress(0)

    results = []

    total = len(
        TEST_DATASET
    )

    if total == 0:

        progress.empty()

        return {
            "summary": {},
            "results": [],
        }

    for index, test_case in enumerate(
        TEST_DATASET
    ):

        result = runner.run_case(
            test_case
        )

        results.append(
            result
        )

        progress.progress(
            (index + 1) / total
        )

    progress.empty()

    summary = runner.summarize(
        results
    )

    return {
        "summary": summary,
        "results": results,
    }


# ============================================================
# EVALUATION DASHBOARD
# ============================================================

def render_evaluation_dashboard(
    provider,
    retrieval_method,
    top_k,
):

    with st.expander(
        "📊 RAG Evaluation",
        expanded=False,
    ):

        pipeline = (
            st.session_state.rag_pipeline
        )

        if pipeline is None:

            st.info(
                "Build or load a vector database "
                "before running evaluation."
            )

            return

        if st.button(
            "▶ Run RAG Evaluation",
            use_container_width=True,
            key="run_rag_evaluation",
        ):

            try:

                pipeline.change_provider(
                    provider
                )

                pipeline.change_retrieval_method(
                    retrieval_method
                )

                pipeline.top_k = top_k

                with st.spinner(
                    "Running RAG evaluation..."
                ):

                    report = (
                        run_rag_evaluation(
                            pipeline
                        )
                    )

                st.session_state[
                    "rag_evaluation_report"
                ] = report

                st.success(
                    "Evaluation completed."
                )

            except Exception as error:

                st.error(
                    f"RAG Evaluation Error: {error}"
                )

        report = (
            st.session_state.get(
                "rag_evaluation_report"
            )
        )

        if not report:

            return

        summary = report.get(
            "summary",
            {},
        )

        results = report.get(
            "results",
            [],
        )

        st.markdown(
            "### 📈 Evaluation Summary"
        )

        total_cases = summary.get(
            "total_cases",
            0,
        )

        retrieval_accuracy = (
            summary.get(
                "retrieval_accuracy"
            )
        )

        context_relevance = (
            summary.get(
                "average_context_relevance",
                0.0,
            )
        )

        answer_grounding = (
            summary.get(
                "average_answer_grounding",
                0.0,
            )
        )

        average_confidence = (
            summary.get(
                "average_confidence",
                0.0,
            )
        )

        col1, col2, col3, col4, col5 = (
            st.columns(5)
        )

        with col1:

            st.metric(
                "Test Cases",
                total_cases,
            )

        with col2:

            st.metric(
                "Retrieval Accuracy",
                (
                    f"{retrieval_accuracy * 100:.1f}%"
                    if retrieval_accuracy is not None
                    else "N/A"
                ),
            )

        with col3:

            st.metric(
                "Context Relevance",
                f"{context_relevance * 100:.1f}%",
            )

        with col4:

            st.metric(
                "Answer Grounding",
                f"{answer_grounding * 100:.1f}%",
            )

        with col5:

            st.metric(
                "Avg Confidence",
                f"{average_confidence * 100:.1f}%",
            )

        # ----------------------------------------------------
        # CONFIDENCE
        # ----------------------------------------------------

        st.markdown(
            "### 🎯 Confidence Distribution"
        )

        high_cases = summary.get(
            "high_confidence_cases",
            0,
        )

        medium_cases = summary.get(
            "medium_confidence_cases",
            0,
        )

        low_cases = summary.get(
            "low_confidence_cases",
            0,
        )

        col1, col2, col3 = (
            st.columns(3)
        )

        with col1:

            st.metric(
                "🟢 High",
                high_cases,
            )

        with col2:

            st.metric(
                "🟡 Medium",
                medium_cases,
            )

        with col3:

            st.metric(
                "🔴 Low",
                low_cases,
            )

        # ----------------------------------------------------
        # INDIVIDUAL RESULTS
        # ----------------------------------------------------

        st.markdown(
            "### 🧪 Individual Results"
        )

        for index, result in enumerate(
            results,
            start=1,
        ):

            question = result.get(
                "question",
                "",
            )

            answer = result.get(
                "answer",
                "",
            )

            expected_answer = result.get(
                "expected_answer",
                "",
            )

            evaluation = result.get(
                "evaluation",
                {},
            )

            confidence = result.get(
                "confidence",
                {},
            )

            retrieval_hit = (
                evaluation.get(
                    "retrieval_hit"
                )
            )

            relevance = (
                evaluation.get(
                    "context_relevance",
                    0.0,
                )
            )

            grounding = (
                evaluation.get(
                    "answer_grounding",
                    0.0,
                )
            )

            confidence_score = (
                confidence.get(
                    "score",
                    0.0,
                )
            )

            confidence_level = (
                confidence.get(
                    "level",
                    "LOW",
                )
            )

            if confidence_level == "HIGH":

                icon = "🟢"

            elif confidence_level == "MEDIUM":

                icon = "🟡"

            else:

                icon = "🔴"

            with st.expander(
                f"{icon} {confidence_level} — "
                f"Question {index}: {question}"
            ):

                col1, col2, col3 = (
                    st.columns(3)
                )

                with col1:

                    st.metric(
                        "Confidence",
                        confidence_level,
                    )

                with col2:

                    st.metric(
                        "Score",
                        f"{confidence_score * 100:.1f}%",
                    )

                with col3:

                    st.metric(
                        "Retrieval",
                        (
                            "PASS"
                            if retrieval_hit is True
                            else "FAIL"
                            if retrieval_hit is False
                            else "N/A"
                        ),
                    )

                st.write(
                    "**Question:**",
                    question,
                )

                if expected_answer:

                    st.write(
                        "**Expected Answer:**",
                        expected_answer,
                    )

                st.write(
                    "**Generated Answer:**",
                    answer,
                )

                st.write(
                    "**Context Relevance:**",
                    f"{relevance * 100:.1f}%",
                )

                st.write(
                    "**Answer Grounding:**",
                    f"{grounding * 100:.1f}%",
                )


# ============================================================
# MAIN
# ============================================================

def show():

    initialize_directories()

    initialize_session_state()

    st.title(
        "📚 MathMind AI — RAG Assistant"
    )

    st.markdown(
        """
        ### Ask questions from your documents

        Upload PDFs → Build FAISS → Retrieve relevant
        chunks → Generate answers with an LLM.
        """
    )

    (
        provider,
        retrieval_method,
        top_k,
    ) = render_sidebar()

    render_document_info()

    st.divider()

    render_retrieval_test()

    st.divider()

    render_evaluation_dashboard(
        provider=provider,
        retrieval_method=retrieval_method,
        top_k=top_k,
    )

    st.divider()

    render_chat_interface(
        provider=provider,
        retrieval_method=retrieval_method,
        top_k=top_k,
    )

    st.divider()

    chat_text = generate_chat_text()

    if chat_text.strip():

        st.download_button(

            "⬇️ Download Conversation",

            data=chat_text,

            file_name="rag_conversation.txt",

            mime="text/plain",

            use_container_width=True,
        )