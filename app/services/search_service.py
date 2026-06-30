from qdrant_client.models import Filter, FieldCondition, MatchValue

class SearchService:

    def __init__(
        self,
        embedding_service,
        sparse_service,
        vectore_service,
    ):
        
        self.dense = embedding_service
        self.sparse = sparse_service
        self.vectore = vectore_service

    async def search(
        self,
        query: str,
        user_id: int
    ):
        
        dense = await self.dense.embed_text(query)
        sparse = await self.sparse.embed_text(query)

        filters = self._build_filter(user_id=user_id)

        return await self.vectore.search(
            dense_vector=dense, 
            sparse_vector=sparse,
            filters=filters
        )
    
    @staticmethod
    def _build_filter(user_id: int):
        
        must = [
            FieldCondition(
                key="user_id",
                match=MatchValue(value=user_id),
            )
        ]

        return Filter(must=must)
        
