from langchain_core.prompts import ChatPromptTemplate

rewrite_user_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Rewrite the user's question to optimize semantic vector retrieval. "
            "Preserve the original intent and return only the rewritten query."
        ),
        (
            "human",
            "{question}"
        )
    ]
)