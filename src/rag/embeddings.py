import os

from src.rag.config import (
    EMBEDDING_MODEL,
)

# "local" runs sentence-transformers on this machine.
# "gemini" uses Google's embedding API instead, which needs no PyTorch
# and fits small free servers (set GEMINI_API_KEY too).
EMBEDDING_PROVIDER = os.getenv("EMBEDDING_PROVIDER", "local").strip().lower()

GEMINI_EMBEDDING_MODEL = os.getenv("GEMINI_EMBEDDING_MODEL", "models/gemini-embedding-001")


class EmbeddingModel:

    def __init__(self):

        if EMBEDDING_PROVIDER == "gemini":

            from langchain_google_genai import GoogleGenerativeAIEmbeddings

            self.embedding = GoogleGenerativeAIEmbeddings(
                model=GEMINI_EMBEDDING_MODEL,
                google_api_key=os.getenv("GEMINI_API_KEY"),
            )

            return

        from langchain_huggingface import HuggingFaceEmbeddings

        self.embedding = HuggingFaceEmbeddings(

            model_name=EMBEDDING_MODEL,

            model_kwargs={
                "device": "cpu",
            },
        )

    def get(self):

        return self.embedding
