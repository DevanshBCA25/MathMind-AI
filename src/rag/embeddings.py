from langchain_huggingface import HuggingFaceEmbeddings

from src.rag.config import (
    EMBEDDING_MODEL,
)


class EmbeddingModel:

    def __init__(self):

        self.embedding = HuggingFaceEmbeddings(

            model_name=EMBEDDING_MODEL,

            model_kwargs={
                "device": "cpu",
            },
        )

    def get(self):

        return self.embedding