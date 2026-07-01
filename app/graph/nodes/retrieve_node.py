from langsmith import traceable
from app.graph.state import GraphState
from app.services.embedding_service import EmbeddingService
from app.services.sparse_embedding_service import SparseEmbeddingService
from app.services.vector_service import VectorService
from app.pydanticModels.models import RetrievedChunk

embedding_service = EmbeddingService()
sparse_service = SparseEmbeddingService()
vector_service = VectorService()

@traceable
async def retrieve_node(state: GraphState):
    embedding = await embedding_service.embed_text(state["rewritten_query"])
    sparse_embedding = await sparse_service.embed_text(state["rewritten_query"])
    results = await vector_service.search(embedding, sparse_embedding, state["user_id"])
    
    chunks = []

    for point in results:
        payload = point.payload
        chunks.append(
            RetrievedChunk(
                chunk_id=payload.get("chunk_id"),
                document_id=payload.get("document_id"),
                file_name=payload.get("file_name"),
                page=payload.get("page"),
                score=point.score,
                content=payload.get("content"),
            )
        )

    print(f"Retrieved {len(chunks)} chunks ")

    return {
        **state,

        "retrieved_chunks": chunks,
    }
