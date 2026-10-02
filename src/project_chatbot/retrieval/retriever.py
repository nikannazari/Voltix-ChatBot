from dataclasses import dataclass

from project_chatbot.config import TOP_K
from project_chatbot.embeddings.embedding_model import (
    EmbeddingModel,
)
from project_chatbot.vector_store.chroma_store import (
    ChromaStore,
)


@dataclass
class RetrievedDocument:
    content: str
    source: str
    distance: float


class Retriever:
    def __init__(self) -> None:
        self.embedding_model = EmbeddingModel()
        self.vector_store = ChromaStore()

    def retrieve(
        self,
        query: str,
        top_k: int = TOP_K,
    ) -> list[RetrievedDocument]:
        """
        Retrieve the most relevant chunks for a query.
        """

        query_embedding = self.embedding_model.embed(
            query
        )

        results = self.vector_store.search(
            embedding=query_embedding,
            top_k=top_k,
        )

        documents = results.get(
            "documents",
            [[]],
        )[0]

        metadatas = results.get(
            "metadatas",
            [[]],
        )[0]

        distances = results.get(
            "distances",
            [[]],
        )[0]

        retrieved: list[RetrievedDocument] = []

        for index, content in enumerate(documents):
            metadata = metadatas[index]
            distance = distances[index]

            retrieved.append(
                RetrievedDocument(
                    content=content,
                    source=metadata.get(
                        "source",
                        "unknown",
                    ),
                    distance=distance,
                )
            )

        return retrieved
