from langchain_core.prompts import ChatPromptTemplate


generate_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are a helpful AI assistant.

Answer ONLY using the provided context.

If the context does not contain enough information, respond exactly:

"I don't have enough information in the provided documents."

Do not make up facts.
Do not use outside knowledge.
Return only the answer.
"""
        ),
        (
            "human",
            """
Context:

{context}

-------------------------

Question:

{question}
"""
        ),
    ]
)