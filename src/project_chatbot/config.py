import os
from pathlib import Path

from dotenv import load_dotenv


# Load environment variables from .env
load_dotenv()


# Project root
BASE_DIR = Path(__file__).resolve().parents[2]


# Data paths
DOCUMENTS_DIR = BASE_DIR / "data" / "documents"
CHROMA_PATH = BASE_DIR / "chroma_db"


# Ollama configuration
OLLAMA_HOST = os.getenv(
    "OLLAMA_HOST",
    "http://localhost:11434",
)

LLM_MODEL = os.getenv(
    "LLM_MODEL",
    "qwen2.5-coder:7b",
)

EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL",
    "nomic-embed-text",
)


# ChromaDB
COLLECTION_NAME = os.getenv(
    "COLLECTION_NAME",
    "project_documents",
)


# RAG configuration
TOP_K = int(
    os.getenv("TOP_K", "5")
)

CHUNK_SIZE = int(
    os.getenv("CHUNK_SIZE", "1000")
)

CHUNK_OVERLAP = int(
    os.getenv("CHUNK_OVERLAP", "200")
)
