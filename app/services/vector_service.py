from __future__ import annotations
from qdrant_client.models import PayloadSchemaType
from typing import List
import uuid

from langchain_core.documents import Document

from qdrant_client import AsyncQdrantClient
from qdrant_client.models import (
    Distance,
    PointStruct,
    SparseVector,
    SparseVectorParams,
    VectorParams,
    Filter,
    NamedVector,
    NamedSparseVector,
    Prefetch,
    Fusion,
    FusionQuery
)

from app.config.setting import QDRANT_API_KEY, QDRANT_URL

class VectorService:

    def __init__(
        self,
        url: str = QDRANT_URL,
        api_key: str = QDRANT_API_KEY,
        collection_name: str = "my_docs",
        vector_size: int = 1024,
        batch_size: int = 5
    ):

        self.collection_name = collection_name
        self.vector_size = vector_size
        self.batch_size = batch_size

        self.client = AsyncQdrantClient(
            url=url,
            api_key=api_key,
        )
    
    async def collection_exists(self) -> bool:

        collections = await self.client.get_collections()

        return any(
            collection.name == self.collection_name
            for collection in collections.collections
        )
    

    async def create_collection(self):

        if await self.collection_exists():
            return self.collection_name
        print("Creating collection")
        await self.client.create_collection(
            collection_name=self.collection_name,
            vectors_config={
                "dense": VectorParams(
                    size=self.vector_size,
                    distance=Distance.COSINE
                )
            },

            sparse_vectors_config={
                "sparse": SparseVectorParams()
            }
        )
        print("Creating indexing")
        await self.client.create_payload_index(
                collection_name=self.collection_name,
                field_name="user_id",
                field_schema=PayloadSchemaType.INTEGER,
        )
        print("Indexing done")
        return self.collection_name
    

    
    async def upsert(

        self,

        chunks: List[Document],

        dense_vectors: List[List[float]],

        sparse_vectors: List[dict],

    ):

        points = []
        point_ids = []

        for chunk, dense, sparse in zip(
            chunks,
            dense_vectors,
            sparse_vectors
        ):  
            
            original_chunk_id = chunk.metadata.get("chunk_id")

            point_id = str(
                uuid.uuid5(
                    uuid.NAMESPACE_DNS,
                    original_chunk_id,
                )
            )

            point_ids.append(point_id)

            payload = chunk.metadata.copy()
            payload["content"] = chunk.page_content

            payload.pop("embedding", None)
            payload.pop("sparse_embedding", None)


            point = PointStruct(

                id=point_id,

                vector={

                    "dense": dense,

                    "sparse": SparseVector(
                        indices=sparse["indices"],
                        values=sparse["values"]
                    )

                },

                payload=payload

            )

            points.append(point)

        await self._upload_batches(points)
        return point_ids

    async def _upload_batches(

        self,

        points: List[PointStruct]

    ):

        total = len(points)

        for i in range(
            0,
            total,
            self.batch_size
        ):

            batch = points[
                i:i+self.batch_size
            ]

            await self.client.upsert(

                collection_name=self.collection_name,

                points=batch,

                wait=True

            )

    async def search(
        self,
        dense_vector: List[float],
        sparse_vector: dict | None = None,
        top_k : int = 6,
        search_type: str = "hybrid",
        filters: Filter | None = None,
    ):
        
        print("Searching")
        if search_type == "dense":
            return await self._dense_search(
                dense_vector=dense_vector,
                top_k=top_k,
                filters=filters,
            )

        return await self._hybrid_search(
            dense_vector=dense_vector,
            sparse_vector=sparse_vector,
            top_k=top_k,
            filters=filters,
        )
        
    
    async def _dense_search(
        self,
        dense_vector: list[float], 
        top_k: int,
        filters: Filter | None = None,
    ):

        response = await self.client.query_points(

            collection_name=self.collection_name,
            query=dense_vector,
            using="dense",
            query_filter=filters,
            limit=top_k,
            with_payload=True,
        )

        return response.points

    async def _hybrid_search(
        self,
        dense_vector: list[float],
        sparse_vector: dict,
        top_k: int,
        filters: Filter | None = None,
    ):

        response = await self.client.query_points(
            collection_name=self.collection_name,

            prefetch=[
                Prefetch(
                    query=dense_vector,
                    using="dense",
                    limit=top_k * 2,
                ),
                Prefetch(
                    query=SparseVector(
                        indices=sparse_vector["indices"],
                        values=sparse_vector["values"],
                    ),
                    using="sparse",
                    limit=top_k * 2,
                ),
            ],

            query=FusionQuery(fusion=Fusion.RRF),

            query_filter=filters,

            limit=top_k,

            with_payload=True,
        )

        return response.points