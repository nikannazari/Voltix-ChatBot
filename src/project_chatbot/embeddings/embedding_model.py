import ollama

from project_chatbot.config import (
    EMBEDDING_MODEL,
    OLLAMA_HOST,
)


class EmbeddingModel:
    def __init__(self) -> None:
        self.client = ollama.Client(
            host=OLLAMA_HOST
        )

    def embed(self, text: str) -> list[float]:
        """
        Generate an embedding for a single text.
        """

        response = self.client.embed(
            model=EMBEDDING_MODEL,
            input=text,
        )

        return response["embeddings"][0]

    def embed_many(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        """
        Generate embeddings for multiple texts.
        """

        if not texts:
            return []

        response = self.client.embed(
            model=EMBEDDING_MODEL,
            input=texts,
        )

        return response["embeddings"]
