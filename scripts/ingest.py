import sys
from pathlib import Path
from uuid import uuid5, NAMESPACE_URL


# Add src/ to Python path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"

sys.path.insert(0, str(SRC_DIR))


from project_chatbot.embeddings.embedding_model import (
    EmbeddingModel,
)
from project_chatbot.ingestion.chunker import (
    chunk_documents,
)
from project_chatbot.ingestion.document_loader import (
    load_documents,
)
from project_chatbot.vector_store.chroma_store import (
    ChromaStore,
)


def create_chunk_id(
    source: str,
    chunk_id: int,
) -> str:
    """
    Create a deterministic ID for a document chunk.
    """

    value = f"{source}:{chunk_id}"

    return str(
        uuid5(
            NAMESPACE_URL,
            value,
        )
    )


def main() -> None:
    print("Loading documents...")

    documents = load_documents()

    print(
        f"Loaded {len(documents)} documents."
    )

    if not documents:
        print(
            "No supported documents found."
        )
        return

    print("Splitting documents into chunks...")

    chunks = chunk_documents(documents)

    print(
        f"Created {len(chunks)} chunks."
    )

    if not chunks:
        print("No chunks were created.")
        return

    print("Generating embeddings...")

    embedding_model = EmbeddingModel()

    texts = [
        chunk.content
        for chunk in chunks
    ]

    embeddings = embedding_model.embed_many(
        texts
    )

    ids = [
        create_chunk_id(
            chunk.source,
            chunk.chunk_id,
        )
        for chunk in chunks
    ]

    metadatas = [
        {
            "source": chunk.source,
            "chunk_id": chunk.chunk_id,
        }
        for chunk in chunks
    ]

    print("Storing data in ChromaDB...")

    vector_store = ChromaStore()

    vector_store.add_documents(
        ids=ids,
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas,
    )

    print(
        "Ingestion completed successfully."
    )

    print(
        f"ChromaDB contains "
        f"{vector_store.count()} chunks."
    )


if __name__ == "__main__":
    main()
