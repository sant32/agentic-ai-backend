from langsmith import traceable
from app.graph.state import GraphState
from app.services.context_builder_service import ContextBuilderService

context_builder_service = ContextBuilderService()

@traceable
async def context_builder_node(state: GraphState):
    context = context_builder_service.build(
        chunks=state["retrieved_chunks"]
    )

    return {
        **state,
        "context": context
    }