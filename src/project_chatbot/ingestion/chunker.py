from dataclasses import dataclass

from project_chatbot.config import CHUNK_OVERLAP, CHUNK_SIZE
from project_chatbot.ingestion.document_loader import Document


@dataclass
class Chunk:
    content: str
    source: str
    chunk_id: int


def split_document(document: Document) -> list[Chunk]:
    """
    Split a document into overlapping chunks.
    """

    text = document.content

    if not text:
        return []

    chunks: list[Chunk] = []

    start = 0
    chunk_id = 0

    while start < len(text):
        end = start + CHUNK_SIZE

        chunk_text = text[start:end].strip()

        if chunk_text:
            chunks.append(
                Chunk(
                    content=chunk_text,
                    source=document.source,
                    chunk_id=chunk_id,
                )
            )

            chunk_id += 1

        if end >= len(text):
            break

        start = end - CHUNK_OVERLAP

    return chunks


def chunk_documents(
    documents: list[Document],
) -> list[Chunk]:
    """
    Split all documents into chunks.
    """

    chunks: list[Chunk] = []

    for document in documents:
        chunks.extend(
            split_document(document)
        )

    return chunks