# core/dependencies.py

from fastapi import Depends


from app.services.chunking_service import ChunkingService
from app.services.embedding_service import EmbeddingService
from app.services.sparse_embedding_service import SparseEmbeddingService
from app.services.vector_service import VectorService
from app.services.ingestion_service import IngestionService
from app.services.search_service import SearchService
from app.guardrails.pii_masking_service import PromptInjectionService
from app.guardrails.prompt_injection_service import PIIMaskingService

chunking_service = ChunkingService()
embedding_service = EmbeddingService()
sparse_service = SparseEmbeddingService()
vector_service = VectorService()

prompt_injection_service = PromptInjectionService()
pii_masking_service = PIIMaskingService()


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

