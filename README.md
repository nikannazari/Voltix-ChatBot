# Project Chatbot

A local RAG-based chatbot for answering questions about a specific software project.

The application uses project documentation as its knowledge base and retrieves relevant information from ChromaDB before sending the context to a local LLM running through Ollama.

## Technologies

* Python
* Ollama
* Qwen2.5-Coder 7B
* ChromaDB
* nomic-embed-text

## Architecture

```text
Project Documents
       |
       v
Document Loader
       |
       v
Chunking
       |
       v
Embedding Model
       |
       v
ChromaDB
       |
       v
Retriever
       |
       v
Relevant Context
       |
       v
Qwen2.5-Coder
       |
       v
Answer
```

## Setup

### 1. Clone the repository

```bash
git clone <repository-url>
cd project-chatbot
```

### 2. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

```bash
cp .env.example .env
```

### 5. Download Ollama models

```bash
ollama pull qwen2.5-coder:7b
ollama pull nomic-embed-text
```

### 6. Add project documents

Place supported project files inside:

```text
data/documents/
```

Supported formats currently include:

```text
.txt
.md
.py
.js
.ts
.html
.css
.json
.yaml
.yml
```

### 7. Index the documents

```bash
python scripts/ingest.py
```

### 8. Start the chatbot

```bash
PYTHONPATH=src python -m project_chatbot.main
```

## Example

```text
You: How does authentication work?

Searching project knowledge...

Generating answer...

Assistant: ...
```

The chatbot also displays the source files used for the retrieved context.

## Project Status

This project is being developed incrementally.

Current components:

* [x] Project structure
* [x] Document loading
* [x] Text chunking
* [x] Ollama embeddings
* [x] ChromaDB storage
* [x] Similarity retrieval
* [x] Ollama LLM integration
* [x] CLI chatbot

Planned improvements:

* [ ] Better code-aware chunking
* [ ] PDF support
* [ ] Improved metadata
* [ ] Conversation memory
* [ ] Retrieval evaluation
* [ ] Streamlit web interface
* [ ] Better source citations
* [ ] Incremental document indexing
