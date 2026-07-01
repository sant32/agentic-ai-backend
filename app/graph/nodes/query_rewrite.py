
from langsmith import traceable
from app.graph.state import GraphState
from app.services.llm_service import LLMService

from app.prompts import rewrite_user_prompt
from app.pydanticModels.models import RewrittenQuery
from app.prompts.rewrite_user_prompt import rewrite_user_prompt

llm_service = LLMService()

@traceable
async def rewrite_node(state: GraphState):

    messages = rewrite_user_prompt.format_messages(
        question=state["masked_query"]
    )

    response = await llm_service.generate(
        messages=messages,
        schema=RewrittenQuery,
    )
    print(response)

    return {
        **state,
        "rewritten_query": response.rewritten_query
    }


