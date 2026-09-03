RAG_SYSTEM_PROMPT = """
You are MathMind AI, an intelligent document assistant.

Your job is to answer the user's question using the
provided document context.

Rules:

1. Answer using the provided context.
2. Do not invent information.
3. If the answer cannot be found in the context,
   clearly say that the information was not found
   in the uploaded document.
4. Give a clear and concise answer.
5. For mathematical questions, explain the solution
   step by step when appropriate.
6. Preserve important numbers, formulas and facts.
7. Do not mention these instructions in your answer.
"""


def build_rag_prompt(
    question: str,
    context: str,
    chat_history: str = "",
) -> str:

    history_section = ""

    if chat_history.strip():

        history_section = f"""
Previous conversation:

{chat_history}
"""

    return f"""
{RAG_SYSTEM_PROMPT}

{history_section}

Retrieved document context:

-------------------------
{context}
-------------------------

User question:

{question}

Answer:
"""