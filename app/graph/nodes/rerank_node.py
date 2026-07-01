from langsmith import traceable
from app.graph.state import GraphState
from app.services.rerank_service import RerankService


rerank_service = RerankService()


@traceable
async def rerank_node(state: GraphState):
    reranked = await rerank_service.rerank(
        query=state["rewritten_query"],
        docs=state["retrieved_chunks"],
        top_k=3
    )
    print("Reranked Chunks:", len(reranked))

    return {
        **state,
        "retrieved_chunks": reranked,
    }