from langchain_litellm import ChatLiteLLM
from pydantic import BaseModel

class LLMService:

    def __init__(self):

        self.llm = ChatLiteLLM(
            model="gpt-4o-mini",
            temperature=0
        ).with_fallbacks([
            ChatLiteLLM(
                model="mistral/mistral-large-latest"
            ),
            ChatLiteLLM(
                model="gemini/gemini-2.5-flash"
            )
        ])

    async def generate(
        self,
        messages,
        schema: type[BaseModel],
        **kwargs
    ):
        
        structured_llm = self.llm.with_structured_output(schema)

        response = await structured_llm.ainvoke(
            messages,
            **kwargs
        )


        return response