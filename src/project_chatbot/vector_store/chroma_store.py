from pathlib import Path

import chromadb

from project_chatbot.config import (
    CHROMA_PATH,
    COLLECTION_NAME,
)


class ChromaStore:
    def __init__(
        self,
        path: Path = CHROMA_PATH,
    ) -> None:
        self.client = chromadb.PersistentClient(
            path=str(path)
        )

        self.collection = (
            self.client.get_or_create_collection(
                name=COLLECTION_NAME
            )
        )

    def add_documents(
        self,
        ids: list[str],
        documents: list[str],
        embeddings: list[list[float]],
        metadatas: list[dict],
    ) -> None:
        """
        Add documents and their embeddings to ChromaDB.
        """

        self.collection.upsert(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
        )

    def search(
        self,
        embedding: list[float],
        top_k: int,
    ) -> dict:
        """
        Search for the most relevant documents.
        """

        return self.collection.query(
            query_embeddings=[embedding],
            n_results=top_k,
        )

    def count(self) -> int:
        """
        Return the number of stored documents.
        """

        return self.collection.count()
