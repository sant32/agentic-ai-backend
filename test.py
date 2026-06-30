# import asyncio
# from app.nodes.query_rewrite_node import rewrite_query_node

# async def main():
#     state = {
#         "question": "How can I cache responses in FastAPI?"
#     }

#     result = await rewrite_query_node(state)
#     print(type(result))
#     print("Result :",result)

# if __name__ == "__main__":
#     asyncio.run(main())

import asyncio
# test_chunking_service.py
from app.services.chunking_service import ChunkingService  # Update import path
from app.services.embedding_service import EmbeddingService
from app.services.sparse_embedding_service import SparseEmbeddingService
from app.services.vector_service import VectorService
from app.services.search_service import SearchService
from langchain_core.documents import Document
from pathlib import Path
from app.core.dependencies import get_search_service


from qdrant_client.models import Filter, FieldCondition, MatchValue

# def test_chunk_text():
#     """Test basic text chunking."""
#     service = ChunkingService()
    
#     text = "This is first sentence. This is second sentence. This is third sentence."
    
#     result = service.chunk_text(text)
    
#     print("Type:", type(result))
#     print("Number of chunks:", len(result))
#     print("First chunk:", result[0].page_content if result else "No chunks")
#     print("Metadata:", result[0].metadata if result else "No metadata")
#     print("-" * 50)


# def test_chunk_text_with_metadata():
#     """Test text chunking with custom metadata."""
#     service = ChunkingService()
    
#     text = "This is first sentence. This is second sentence."
#     metadata = {"source": "test.txt", "author": "John"}
    
#     result = service.chunk_text(text, metadata=metadata)
    
#     print("Type:", type(result))
#     print("Number of chunks:", len(result))
#     print("Custom metadata preserved:", result[0].metadata["source"] == "test.txt")
#     print("Chunk ID:", result[0].metadata.get("chunk_id"))
#     print("-" * 50)


# def test_chunk_documents():
#     """Test chunking existing documents."""
#     service = ChunkingService()
#     project_dir = Path(__file__).resolve().parent
#     pdf_path = project_dir / "AI-Agent-Observability-Checklist.pdf"
    
#     result = service.chunk_pdf(pdf_path)
    
#     print("Type:", type(result[0]))
#     print("Number of chunks:", len(result))
        
#     # print("First chunk content:", result[0].page_content if result else "No chunks")
#     # print("Original metadata preserved:", result[0].metadata.get("source") if result else "No chunks")
#     # print("-" * 50)


# def test_empty_text():
#     """Test chunking empty text."""
#     service = ChunkingService()
    
#     result = service.chunk_text("")
    
#     print("Type:", type(result))
#     print("Number of chunks:", len(result))
#     print("Content:", repr(result[0].page_content) if result else "No chunks")
#     print("-" * 50)


# def test_custom_chunk_size():
#     """Test with custom chunk size."""
#     service = ChunkingService(chunk_size=50, chunk_overlap=10)
    
#     text = "word " * 30  # ~150 characters
    
#     result = service.chunk_text(text)
    
#     print("Type:", type(result))
#     print("Number of chunks:", len(result))
#     for i, chunk in enumerate(result):
#         print(f"Chunk {i} size: {len(chunk.page_content)} characters")
#     print("-" * 50)



# async def test_embeddings():
#     service = EmbeddingService()

#     texts = [
#         "First document text",
#         "Second document text",
#         "Third document text"
#     ]
#     embeddings = await service.embed_documents(texts)
#     print(type(embeddings))           # <class 'list'>
#     print(len(embeddings))            # 3 (one per text)
#     print(len(embeddings[0]))         # 768 (vector size)
#     print(type(embeddings[0]))        # <class 'list'>
#     # for e in embeddings:
#     #     print(e)

# async def test_sparse_embeddings():
#     service = SparseEmbeddingService()
#     texts = [
#         "First document text",
#         "Second document text",
#         "Third document text"
#     ]

#     result = await service.embed_documents(texts)

async def test_chunking_embeddings():

    project_dir = Path(__file__).resolve().parent
    pdf_path = project_dir / "Santosh-Sakre.pdf"
    # text = "This is first sentence. This is second sentence. This is third sentence."
    
    chunking_service = ChunkingService()
    embedding_service = EmbeddingService()
    sparse_service = SparseEmbeddingService()
    vectore_db = VectorService()
    
    
    # await vectore_db.create_collection()

    info = await vectore_db.get_collection("documents")
    print(info)

    chunks = chunking_service.chunk_pdf(pdf_path)
    print(len(chunks))
    print(chunks[0])
    ids = [chunk.metadata.get("chunk_id") for chunk in chunks]
    # print(ids)
    texts = [chunk.page_content for chunk in chunks]
    embeddings = await embedding_service.embed_documents(texts)
    # return embeddings
    sparse_embeddings = await sparse_service.embed_documents(texts)
    ids = await vectore_db.upsert(chunks, embeddings, sparse_embeddings)

    # print(ids)
    return ids
    


async def hybrid_search_semantic():

    query = "What to trace in any agent run"
    query1 = 'AI Eng' \
    'ineer'
    user_id = 11
    # embedding_service = EmbeddingService()
    # sparse_service = SparseEmbeddingService()
    # vector_service = VectorService()

    # search_service = SearchService(
    #     embedding_service=embedding_service,
    #     sparse_service=sparse_service,
    #     vectore_service=vector_service,
    # )
    search_service = get_search_service()
    results = await search_service.search(query1, user_id)
    docs = []
    # print(results)
    for result in results:
        docs.append({
            "id": result.id,
            "user_id": result.payload.get("user_id"),
            "score": result.score,
            "chunk_id": result.payload.get("chunk_id"),
            "document_id": result.payload.get("document_id"),
            # "content": result.payload.get("content"),
            "page": result.payload.get("page"),
            "source": result.payload.get("source"),

        })

    print(docs)
    print("Count :", len(docs))
    return docs

async def main():
    """Run all tests."""
    # print("=" * 50)
    # print("TESTING CHUNKING SERVICE")
    # print("=" * 50)
    # print()
    # result = await test_chunking_embeddings()
    # print(result)
    await hybrid_search_semantic()
    
    # print("1. Testing basic text chunking:")
    # test_chunk_text()
    
    # print("2. Testing text chunking with metadata:")
    # test_chunk_text_with_metadata()
    
    # print("3. Testing document chunking:")
    # test_chunk_documents()
    
    # print("4. Testing empty text:")
    # test_empty_text()
    
    # print("5. Testing custom chunk size:")
    # test_custom_chunk_size()
    
    # print("=" * 50)
    # print("ALL TESTS COMPLETE")
    # print("=" * 50)
    # await test_embeddings()
    # await test_sparse_embeddings()
if __name__ == "__main__":
    asyncio.run(main())