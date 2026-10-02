from project_chatbot.llm.ollama_client import (
    OllamaClient,
)
from project_chatbot.retrieval.retriever import (
    Retriever,
)


def build_context(retrieved_documents) -> str:
    """
    Build the context sent to the LLM.
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


def main() -> None:
    print("=" * 60)
    print("Project RAG Chatbot")
    print("=" * 60)
    print("Type 'exit' or 'quit' to leave.")
    print()

    retriever = Retriever()
    llm = OllamaClient()

    while True:
        try:
            question = input("You: ").strip()

        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            break

        if not question:
            continue

        if question.lower() in {
            "exit",
            "quit",
        }:
            print("Goodbye!")
            break

        print("\nSearching project knowledge...")

        retrieved_documents = retriever.retrieve(
            question
        )

        context = build_context(
            retrieved_documents
        )

        print("Generating answer...\n")

        answer = llm.generate(
            question=question,
            context=context,
        )

        print(f"Assistant: {answer}")

        print("\nSources:")

        if retrieved_documents:
            seen_sources = set()

            for document in retrieved_documents:
                if document.source in seen_sources:
                    continue

                print(
                    f"- {document.source}"
                )

                seen_sources.add(
                    document.source
                )

        print()


if __name__ == "__main__":
    main()
