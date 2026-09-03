from pathlib import Path
from typing import Any, Dict

from src.rag.config import DOCUMENTS_DIR, VECTOR_DB_DIR


class SystemHealth:

    def __init__(self):
        pass

    @staticmethod
    def check_directory(path) -> Dict[str, Any]:

        directory = Path(path)

        return {
            "exists": directory.exists(),
            "path": str(directory),
            "is_directory": directory.is_dir(),
        }

    def check_documents(self) -> Dict[str, Any]:

        directory = Path(DOCUMENTS_DIR)

        pdf_files = (
            list(directory.glob("*.pdf"))
            if directory.exists()
            else []
        )

        return {
            "status": "READY"
            if pdf_files
            else "EMPTY",
            "count": len(pdf_files),
            "files": [
                file.name
                for file in pdf_files
            ],
        }

    def check_vector_database(self) -> Dict[str, Any]:

        directory = Path(VECTOR_DB_DIR)

        index_file = (
            directory / "index.faiss"
        )

        metadata_file = (
            directory / "index.pkl"
        )

        ready = (
            directory.exists()
            and index_file.exists()
            and metadata_file.exists()
        )

        return {
            "status": "READY"
            if ready
            else "NOT_READY",
            "directory_exists": directory.exists(),
            "index_exists": index_file.exists(),
            "metadata_exists": metadata_file.exists(),
        }

    def check_environment(self) -> Dict[str, Any]:

        import os

        providers = {
            "OpenAI": bool(
                os.getenv("OPENAI_API_KEY")
            ),
            "Gemini": bool(
                os.getenv("GOOGLE_API_KEY")
                or os.getenv("GEMINI_API_KEY")
            ),
            "Groq": bool(
                os.getenv("GROQ_API_KEY")
            ),
        }

        return {
            "providers": providers,
        }

    def run(self) -> Dict[str, Any]:

        documents = self.check_documents()

        vector_database = (
            self.check_vector_database()
        )

        environment = (
            self.check_environment()
        )

        return {
            "documents": documents,
            "vector_database": vector_database,
            "environment": environment,
        }


__all__ = [
    "SystemHealth",
]