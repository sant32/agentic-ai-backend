from langsmith import traceable
from app.graph.state import GraphState
from app.guardrails.prompt_injection_service import PromptInjectionService

prompt_injection_service = PromptInjectionService()


@traceable
async def prompt_guard_node(state: GraphState) -> GraphState:
    is_attack = prompt_injection_service.detect(state.get("masked_query"))

    return {
        **state,
        "is_prompt_attack": is_attack,
        "attack_reason": (
            "Matched blocked prompt injection pattern"
            if is_attack
            else None
            ),
    }