import sys
from pathlib import Path

import ollama
import streamlit as st


# ---------------------------------------------------------
# Add src/ to Python path
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"

sys.path.insert(0, str(SRC_DIR))


from project_chatbot.config import (
    EMBEDDING_MODEL,
    LLM_MODEL,
    OLLAMA_HOST,
)
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
# Translations
# ---------------------------------------------------------

TRANSLATIONS = {
    "en": {
        "title": "⚡ Voltix ChatBot",
        "subtitle": "Ask questions about Voltix facilities.",
        "language": "Language",
        "switch": "فارسی",

        "sidebar_title": "Voltix Chatbot",
        "sidebar_description": (
            "Local RAG assistant powered by Ollama and ChromaDB."
        ),

        "models": "Models",
        "llm_model": "LLM Model",
        "embedding_model": "Embedding Model",
        "model_help": "Select the Ollama model used to generate answers.",
        "no_models": "No Ollama LLM models were found.",

        "clear_chat": "Clear Chat",

        "chat_placeholder": "Ask something about Voltix...",
        "welcome": (
            "Hello! Ask me anything about the Voltix project."
        ),

        "searching": "Searching project knowledge...",
        "generating": "Generating answer with",

        "sources": "Sources",

        "retrieval_error": "Retrieval error",
        "llm_error": "LLM error",

        "empty_context": (
            "No relevant project context was found."
        ),

        "footer": "Voltix Project Chatbot",
    },

    "fa": {
        "title": "⚡ چت‌بات Voltix",
        "subtitle": "درباره پروژه Voltix سؤال بپرسید.",
        "language": "زبان",
        "switch": "English",

        "sidebar_title": "چت‌بات Voltix",
        "sidebar_description": (
            "دستیار RAG محلی با استفاده از Ollama و ChromaDB."
        ),

        "models": "مدل‌ها",
        "llm_model": "مدل زبانی",
        "embedding_model": "مدل Embedding",
        "model_help": "مدل Ollama مورد استفاده برای تولید پاسخ را انتخاب کنید.",
        "no_models": "هیچ مدل زبانی Ollama پیدا نشد.",

        "clear_chat": "پاک کردن گفتگو",

        "chat_placeholder": "سؤالی درباره Voltix بپرسید...",
        "welcome": (
            "سلام! هر سؤالی درباره پروژه Voltix دارید بپرسید."
        ),

        "searching": "در حال جستجو در اطلاعات پروژه...",
        "generating": "در حال تولید پاسخ با",

        "sources": "منابع",

        "retrieval_error": "خطا در جستجوی اطلاعات",
        "llm_error": "خطا در اجرای مدل زبانی",

        "empty_context": (
            "اطلاعات مرتبطی درباره پروژه پیدا نشد."
        ),

        "footer": "چت‌بات پروژه Voltix",
    },
}


# ---------------------------------------------------------
# Session state
# ---------------------------------------------------------

if "language" not in st.session_state:
    st.session_state.language = "en"

if "messages" not in st.session_state:
    st.session_state.messages = []

if "selected_llm" not in st.session_state:
    st.session_state.selected_llm = LLM_MODEL


# ---------------------------------------------------------
# Current UI language
# ---------------------------------------------------------

language = st.session_state.language
text = TRANSLATIONS[language]

is_rtl = language == "fa"

direction = "rtl" if is_rtl else "ltr"
alignment = "right" if is_rtl else "left"


# ---------------------------------------------------------
# Language toggle
# ---------------------------------------------------------

def toggle_language():
    if st.session_state.language == "en":
        st.session_state.language = "fa"
    else:
        st.session_state.language = "en"


# ---------------------------------------------------------
# Custom styling
# ---------------------------------------------------------

st.markdown(
    f"""
    <style>

        .stApp {{
            direction: {direction};
        }}

        .block-container {{
            max-width: 1100px;
            padding-top: 2rem;
        }}

        .chat-title {{
            font-size: 2.2rem;
            font-weight: 700;
            margin-bottom: 0.2rem;
            direction: {direction};
            text-align: {alignment};
        }}

        .chat-subtitle {{
            color: #888;
            margin-bottom: 2rem;
            direction: {direction};
            text-align: {alignment};
        }}

        .stMarkdown {{
            direction: {direction};
        }}

        .stCaption {{
            direction: {direction};
        }}

        .stAlert {{
            direction: {direction};
        }}

        [data-testid="stSidebar"] {{
            direction: {direction};
        }}

        [data-testid="stSidebar"] .stMarkdown {{
            text-align: {alignment};
        }}

        [data-testid="stChatMessage"] {{
            direction: {direction};
        }}

        [data-testid="stChatMessage"] .stMarkdown {{
            text-align: {alignment};
        }}

        [data-testid="stChatInput"] textarea {{
            direction: {direction};
            text-align: {alignment};
        }}

        [data-testid="stExpander"] {{
            direction: {direction};
        }}

        code,
        pre {{
            direction: ltr !important;
            text-align: left !important;
        }}

        .voltix-footer {{
            margin-top: 3rem;
            padding-top: 1rem;
            border-top: 1px solid rgba(128, 128, 128, 0.2);
            color: #888;
            font-size: 0.85rem;
            text-align: center;
        }}

    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# Ollama model discovery
# ---------------------------------------------------------

@st.cache_data(ttl=30)
def get_ollama_models() -> list[str]:
    """
    Get all models currently installed in Ollama.
    """

    try:
        client = ollama.Client(
            host=OLLAMA_HOST
        )

        response = client.list()

        models = []

        for model in response["models"]:

            model_name = model["model"]

            if model_name == EMBEDDING_MODEL:
                continue

            if model_name == f"{EMBEDDING_MODEL}:latest":
                continue

            models.append(model_name)

        return sorted(set(models))

    except Exception:
        return []


# ---------------------------------------------------------
# Initialize retriever
# ---------------------------------------------------------

@st.cache_resource
def get_retriever() -> Retriever:
    return Retriever()


retriever = get_retriever()


# ---------------------------------------------------------
# Helper functions
# ---------------------------------------------------------

def build_context(retrieved_documents) -> str:
    """
    Build the context that will be sent to the LLM.
    """

    if not retrieved_documents:
        return text["empty_context"]

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

language_col, title_col = st.columns([1, 5])

with language_col:

    st.caption(text["language"])

    st.button(
        text["switch"],
        on_click=toggle_language,
        use_container_width=True,
    )


with title_col:

    st.markdown(
        f"""
        <div
            class="chat-title"
            dir="{direction}"
        >
            {text["title"]}
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div
            class="chat-subtitle"
            dir="{direction}"
        >
            {text["subtitle"]}
        </div>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------
# Sidebar
# ---------------------------------------------------------

with st.sidebar:

    st.header(text["sidebar_title"])

    st.write(
        text["sidebar_description"]
    )

    st.divider()

    st.subheader(text["models"])

    # -----------------------------------------------------
    # LLM model selection
    # -----------------------------------------------------

    available_models = get_ollama_models()

    if available_models:

        if (
            st.session_state.selected_llm
            not in available_models
        ):
            st.session_state.selected_llm = (
                available_models[0]
            )

        selected_llm = st.selectbox(
            text["llm_model"],
            options=available_models,
            index=available_models.index(
                st.session_state.selected_llm
            ),
            help=text["model_help"],
        )

        st.session_state.selected_llm = selected_llm

    else:

        st.warning(
            text["no_models"]
        )

        selected_llm = LLM_MODEL

    # -----------------------------------------------------
    # Embedding model
    # -----------------------------------------------------

    st.caption(
        f"{text['embedding_model']}: {EMBEDDING_MODEL}"
    )

    st.divider()

    # -----------------------------------------------------
    # Clear chat
    # -----------------------------------------------------

    if st.button(
        text["clear_chat"],
        use_container_width=True,
    ):

        st.session_state.messages = []

        st.rerun()


# ---------------------------------------------------------
# Initialize LLM
# ---------------------------------------------------------

llm = OllamaClient(
    model=selected_llm
)


# ---------------------------------------------------------
# Welcome message
# ---------------------------------------------------------

if not st.session_state.messages:

    st.info(
        text["welcome"]
    )


# ---------------------------------------------------------
# Display previous messages
# ---------------------------------------------------------

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )

        if (
            message["role"] == "assistant"
            and message.get("sources")
        ):

            with st.expander(
                text["sources"]
            ):

                for source in message["sources"]:

                    st.markdown(
                        f"- `{source}`"
                    )


# ---------------------------------------------------------
# Chat input
# ---------------------------------------------------------

question = st.chat_input(
    text["chat_placeholder"]
)


# ---------------------------------------------------------
# Process question
# ---------------------------------------------------------

if question:

    # -----------------------------------------------------
    # Display user message
    # -----------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
        }
    )

    with st.chat_message("user"):

        st.markdown(question)

    # -----------------------------------------------------
    # Generate assistant response
    # -----------------------------------------------------

    with st.chat_message("assistant"):

        # -------------------------------------------------
        # Retrieval
        # -------------------------------------------------

        with st.spinner(
            text["searching"]
        ):

            try:

                retrieved_documents = (
                    retriever.retrieve(
                        question
                    )
                )

                context = build_context(
                    retrieved_documents
                )

            except Exception as error:

                st.error(
                    f"{text['retrieval_error']}: {error}"
                )

                st.stop()

        # -------------------------------------------------
        # LLM generation
        # -------------------------------------------------

        with st.spinner(
            f"{text['generating']} {selected_llm}..."
        ):

            try:

                answer = llm.generate(
                    question=question,
                    context=context,
                )

            except Exception as error:

                st.error(
                    f"{text['llm_error']}: {error}"
                )

                st.stop()

        # -------------------------------------------------
        # Display answer
        # -------------------------------------------------

        st.markdown(answer)

        # -------------------------------------------------
        # Sources
        # -------------------------------------------------

        sources = get_sources(
            retrieved_documents
        )

        if sources:

            with st.expander(
                text["sources"]
            ):

                for source in sources:

                    st.markdown(
                        f"- `{source}`"
                    )

        # -------------------------------------------------
        # Save assistant response
        # -------------------------------------------------

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer,
                "sources": sources,
            }
        )


# ---------------------------------------------------------
# Footer
# ---------------------------------------------------------

st.markdown(
    f"""
    <div class="voltix-footer">
        {text["footer"]}
    </div>
    """,
    unsafe_allow_html=True,
)