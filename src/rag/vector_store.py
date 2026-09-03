from pathlib import Path

from langchain_community.vectorstores import FAISS

from src.rag.embeddings import EmbeddingModel


class VectorDatabase:

    def __init__(self):

        self.embeddings = EmbeddingModel().get()

    def create(self, chunks):

        return FAISS.from_documents(

            chunks,

            self.embeddings,

        )

    def save(self, db, path):

        Path(path).mkdir(
            parents=True,
            exist_ok=True,
        )

        db.save_local(path)

    def load(self, path):

        return FAISS.load_local(

            path,

            self.embeddings,

            allow_dangerous_deserialization=True,

        )

    def exists(self, path):

        return Path(path).exists()