

from typing import TypedDict, Optional


class GraphState(TypedDict):

    user_id: int
    conversation_id: str | None

    query: str
    masked_query: str
    rewritten_query: str

    is_prompt_attack: bool
    attack_reason: str | None

    

    retrieved_chunks: list
    context: str

    answer: str | None
    error: str | None