from dataclasses import dataclass
from pathlib import Path

from project_chatbot.config import DOCUMENTS_DIR


SUPPORTED_EXTENSIONS = {
    ".txt",
    ".md",
    ".py",
    ".js",
    ".ts",
    ".html",
    ".css",
    ".json",
    ".yaml",
    ".yml",
}


@dataclass
class Document:
    content: str
    source: str


def load_documents() -> list[Document]:
    """
    Load all supported documents from the documents directory.
    """

    documents: list[Document] = []

    if not DOCUMENTS_DIR.exists():
        raise FileNotFoundError(
            f"Documents directory does not exist: {DOCUMENTS_DIR}"
        )

    for file_path in DOCUMENTS_DIR.rglob("*"):
        if not file_path.is_file():
            continue

        if file_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue

        try:
            content = file_path.read_text(
                encoding="utf-8"
            )
        except UnicodeDecodeError:
            print(
                f"Skipping non-UTF-8 file: {file_path}"
            )
            continue

        content = content.strip()

        if not content:
            continue

        relative_path = file_path.relative_to(
            DOCUMENTS_DIR
        )

        documents.append(
            Document(
                content=content,
                source=str(relative_path),
            )
        )

    return documents
