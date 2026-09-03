from langchain_text_splitters import (
    RecursiveCharacterTextSplitter,
)

from src.rag.config import (
    CHUNK_SIZE,
    CHUNK_OVERLAP,
)


class Chunker:

    def __init__(self):

        self.splitter = RecursiveCharacterTextSplitter(

            chunk_size=CHUNK_SIZE,

            chunk_overlap=CHUNK_OVERLAP,

        )

    def split(self, documents):

        return self.splitter.split_documents(
            documents
        )