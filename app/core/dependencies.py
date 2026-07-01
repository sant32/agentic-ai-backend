# core/dependencies.py

from fastapi import Depends


from app.services.chunking_service import ChunkingService
from app.services.embedding_service import EmbeddingService
from app.services.sparse_embedding_service import SparseEmbeddingService
from app.services.vector_service import VectorService
from app.services.ingestion_service import IngestionService
from app.services.search_service import SearchService
from app.services.llm_service import LLMService
from app.services.rerank_service import RerankService
from app.services.context_builder_service import ContextBuilderService
from app.services.graph_service import GraphService


chunking_service = ChunkingService()
embedding_service = EmbeddingService()
sparse_service = SparseEmbeddingService()
vector_service = VectorService()


rerank_service = RerankService()
context_builder_service = ContextBuilderService()


llm_service = LLMService()

graph_service = GraphService()

def create_ingestion_service():
    return IngestionService(
        chunking_service,
        embedding_service,
        sparse_service,
        vector_service,
    )


def get_ingestion_service():
    return create_ingestion_service()

def get_search_service():
    return SearchService(
        embedding_service,
        sparse_service,
        vector_service
    )

