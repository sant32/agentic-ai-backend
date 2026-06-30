
from app.services.llm_service import LLMService
from app.pydanticModels.models import RewrittenQuery
from app.prompts.rewrite_user_prompt import rewrite_user_prompt

llm_service = LLMService()



async def rewrite_query_node(state):

    messages = rewrite_user_prompt.format_messages(
        question=state["question"]
    )

    result = await llm_service.generate(
        messages=messages,
        schema=RewrittenQuery
    )
    print("node :", result)

    return {
        "rewritten_query": result.rewritten_query
    }