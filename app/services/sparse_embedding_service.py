from __future__ import annotations

from typing import List, Dict, Any, Optional
from fastembed import SparseTextEmbedding
import asyncio
import time


class SparseEmbeddingService:

    def __init__(self, model_name: str = "Qdrant/bm25",batch_size: int = 50,max_concurrent: int = 5,):

        self.batch_size = batch_size
        self.max_concurrent = max_concurrent

        self.model = SparseTextEmbedding(
            model_name=model_name
        )

        self.semaphore = asyncio.Semaphore(max_concurrent)

    @staticmethod
    def _format_embedding(embedding):

        return{
            "indices": embedding.indices.tolist(),
            "values": embedding.values.tolist()
        }


    async def embed_text(
        self,
        text: str
    ):

        result = await asyncio.to_thread(
            lambda: next(self.model.embed([text]))
        )

        return self._format_embedding(result)
    
    async def embed_documents(
        self,
        texts: list[str]
    ):

        vectors = []

        for start in range(0, len(texts), self.batch_size):
            batch = texts[start:start + self.batch_size]

            embeddings = await asyncio.to_thread(
                list,
                self.model.embed(batch)
            )

            vectors.extend(
                self._format_embedding(e)
                for e in embeddings
            )

        
        return vectors
    
