from langsmith import traceable
from app.graph.state import GraphState
from app.guardrails.pii_masking_service import PIIMaskingService

pii_masking_service = PIIMaskingService()


@traceable
async def pii_node(state: GraphState) -> GraphState:
    masked = pii_masking_service.mask(state.get("query"))

    return {
        **state,
        "masked_query": masked
    }