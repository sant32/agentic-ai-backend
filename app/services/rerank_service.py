
from cohere import AsyncClient
from app.config.setting import COHERE_API_KEY



class RerankService:
    
    def __init__(self):
        self.cohere_client = AsyncClient(COHERE_API_KEY)

    async def rerank(self, query, docs, top_k=3):
        documents = [doc.content for doc in docs]

        response = await self.cohere_client.rerank(
            model="rerank-v4.0-pro",
            query=query,
            documents=documents,
            top_n=top_k
        )

        # Return documents in reranked order
        return [docs[result.index] for result in response.results]