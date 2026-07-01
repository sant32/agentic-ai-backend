from langsmith import traceable
from app.graph.state import GraphState
from app.services.llm_service import LLMService

from app.prompts.generate_prompt import generate_prompt
from app.pydanticModels.models import GeneratedAnswer

llm_service = LLMService()

@traceable
async def generate_node(
    state: GraphState,
):

    messages = generate_prompt.format_messages(
        context=state["context"],
        question=state["rewritten_query"],
    )

    response = await llm_service.generate(
        messages=messages,
        schema=GeneratedAnswer,
    )

    return {
        **state,
        "answer": response.answer,
    }