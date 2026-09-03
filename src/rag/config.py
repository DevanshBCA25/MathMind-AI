from pathlib import Path


BASE_DIR = Path.cwd()


DOCUMENTS_DIR = (
    BASE_DIR
    / "data"
    / "documents"
)


VECTOR_DB_DIR = (
    BASE_DIR
    / "data"
    / "vector_store"
)


HISTORY_DIR = (
    BASE_DIR
    / "data"
    / "history"
)


CHUNK_SIZE = 1000


CHUNK_OVERLAP = 200


EMBEDDING_MODEL = (
    "sentence-transformers/"
    "all-MiniLM-L6-v2"
)


TOP_K = 4


RETRIEVAL_METHOD = "similarity"


MMR_FETCH_K = 20


MMR_LAMBDA = 0.5


MAX_CHAT_MESSAGES = 10


SUPPORTED_DOCUMENT_TYPES = [
    ".pdf",
]