from fastapi import APIRouter, Depends
from app.core.dependencies import graph_service 

from app.schemas.auth import SearchRequest, SearchResponse

router = APIRouter()

@router.post("/search", response_model=SearchResponse)
async def search(
    request: SearchRequest
):
    state = {
        "user_id": 11,          # later from JWT
        "conversation_id": None,

        "query": request.query,

        "masked_query": "",
        "rewritten_query": "",

        "is_prompt_attack": False,
        "attack_reason": None,

        "retrieved_chunks": [],
        "context": "",
        "answer": "",
        "error": None,
    }
    
    result = await graph_service.search(state)
    return result