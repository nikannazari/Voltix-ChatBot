import sys
from pathlib import Path

import streamlit as st


# Add src/ to Python path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"

sys.path.insert(0, str(SRC_DIR))


from project_chatbot.llm.ollama_client import OllamaClient
from project_chatbot.retrieval.retriever import Retriever


# ---------------------------------------------------------
# Page configuration
# ---------------------------------------------------------

st.set_page_config(
    page_title="Voltix ChatBot",
    page_icon="⚡",
    layout="wide",
)


# ---------------------------------------------------------
# Custom styling
# ---------------------------------------------------------

st.markdown(
    """
    <style>
        .block-container {
            max-width: 1100px;
            padding-top: 2rem;
        }

        .chat-title {
            font-size: 2.2rem;
            font-weight: 700;
            margin-bottom: 0.2rem;
        }

        .chat-subtitle {
            color: #888;
            margin-bottom: 2rem;
        }

        .source-box {
            padding: 0.75rem 1rem;
            border-radius: 8px;
            background-color: rgba(128, 128, 128, 0.08);
            margin-top: 0.5rem;
            font-size: 0.9rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# Initialize application objects
# ---------------------------------------------------------

@st.cache_resource
def get_retriever() -> Retriever:
    return Retriever()


@st.cache_resource
def get_llm() -> OllamaClient:
    return OllamaClient()


retriever = get_retriever()
llm = get_llm()


# ---------------------------------------------------------
# Session state
# ---------------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []


# ---------------------------------------------------------
# Helper functions
# ---------------------------------------------------------

def build_context(retrieved_documents) -> str:
    """
    Build the context that will be sent to the LLM.
    """

    if not retrieved_documents:
        return "No relevant project context was found."

    sections = []

    for index, document in enumerate(
        retrieved_documents,
        start=1,
    ):
        sections.append(
            f"""
--- Context {index} ---
Source: {document.source}

{document.content}
"""
        )

    return "\n".join(sections)


def get_sources(retrieved_documents) -> list[str]:
    """
    Return unique source filenames.
    """

    sources = []
    seen = set()

    for document in retrieved_documents:
        if document.source in seen:
            continue

        sources.append(document.source)
        seen.add(document.source)

    return sources


# ---------------------------------------------------------
# Header
# ---------------------------------------------------------

st.markdown(
    '<div class="chat-title">⚡Voltix ChatBot</div>',
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="chat-subtitle">
        Ask questions about Voltix facilities.
    </div>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# Sidebar
# ---------------------------------------------------------

with st.sidebar:
    st.header("Voltix Chatbot")

    st.write(
        "Local RAG assistant powered by Ollama and ChromaDB."
    )

    st.divider()

    st.subheader("Models")

    st.caption(
        "LLM: Qwen2.5-Coder 7B"
    )

    st.caption(
        "Embeddings: nomic-embed-text"
    )

    st.divider()

    if st.button(
        "Clear Chat",
        use_container_width=True,
    ):
        st.session_state.messages = []
        st.rerun()


# ---------------------------------------------------------
# Display previous messages
# ---------------------------------------------------------

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        if (
            message["role"] == "assistant"
            and message.get("sources")
        ):
            with st.expander("Sources"):
                for source in message["sources"]:
                    st.markdown(
                        f"- `{source}`"
                    )


# ---------------------------------------------------------
# Chat input
# ---------------------------------------------------------

question = st.chat_input(
    "Ask something about Voltix..."
)


if question:
    # Display user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
        }
    )

    with st.chat_message("user"):
        st.markdown(question)

    # Generate assistant response
    with st.chat_message("assistant"):
        with st.spinner(
            "Searching project knowledge..."
        ):
            try:
                retrieved_documents = (
                    retriever.retrieve(question)
                )

                context = build_context(
                    retrieved_documents
                )

            except Exception as error:
                st.error(
                    f"Retrieval error: {error}"
                )
                st.stop()

        with st.spinner(
            "Generating answer..."
        ):
            try:
                answer = llm.generate(
                    question=question,
                    context=context,
                )

            except Exception as error:
                st.error(
                    f"LLM error: {error}"
                )
                st.stop()

        st.markdown(answer)

        sources = get_sources(
            retrieved_documents
        )

        if sources:
            with st.expander("Sources"):
                for source in sources:
                    st.markdown(
                        f"- `{source}`"
                    )

    # Save assistant response
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
            "sources": sources,
        }
    )