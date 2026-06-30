import asyncio
from typing import List, Optional
from langchain_litellm import LiteLLMEmbeddings

class EmbeddingService:

    """
    Handles embedding generation with LiteLLM and fallback support.
    """

    def __init__(self, batch_size: int = 10, max_concurrent: int = 2):
        self.batch_size = batch_size
        self.max_concurrent = max_concurrent

        self.semaphore = asyncio.Semaphore(max_concurrent)
        
        self.embedding_model = LiteLLMEmbeddings(
            model="mistral/mistral-embed",
        )

    async def embed_text(
            self,
            text: str
    ):
        return await self.embedding_model.aembed_query(
            text
        )
    
    async def _embed_batch_with_limit(self, batch: List[str]):
        """Embed a single batch with semaphore protection."""
        async with self.semaphore:
            return await self.embedding_model.aembed_documents(batch)

    async def embed_documents(
            self,
            texts: List[str]
    ):
        
        if len(texts) <= self.batch_size:
            async with self.semaphore:
                return  await self.embedding_model.aembed_documents(texts)

        batches = []
        for i in range(0, len(texts), self.batch_size):
            batch = texts[i:i + self.batch_size]
            batches.append(batch)

        tasks = []
        for batch in batches:
            task = self._embed_batch_with_limit(batch)
            tasks.append(task)


        batch_results = await asyncio.gather(*tasks)

        all_embeddings = []
        for result in batch_results:
            all_embeddings.extend(result)

        return  all_embeddings