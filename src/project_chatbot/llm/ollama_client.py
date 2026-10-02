import ollama

from project_chatbot.config import (
    LLM_MODEL,
    OLLAMA_HOST,
)


SYSTEM_PROMPT = """
You are a project documentation assistant.

Your job is to answer questions about the user's project.

Use the provided project context as your primary source of truth.

Rules:

1. Answer based on the provided context.
2. Do not invent project-specific information.
3. If the context does not contain enough information,
   clearly say that the available project documentation
   does not provide enough information.
4. You may explain programming concepts when necessary,
   but distinguish general knowledge from information
   explicitly found in the project context.
5. Be clear and technically accurate.
6. When useful, mention the source files that support
   your answer.
"""


class OllamaClient:
    def __init__(
        self,
        model: str = LLM_MODEL,
    ) -> None:
        self.client = ollama.Client(
            host=OLLAMA_HOST
        )

        self.model = model

    def generate(
        self,
        question: str,
        context: str,
    ) -> str:
        """
        Generate an answer using the selected LLM.
        """

        prompt = f"""
Project Context:

{context}

User Question:

{question}

Answer the question using the project context above.
"""

        response = self.client.chat(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT,
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        )

        return response["message"]["content"]