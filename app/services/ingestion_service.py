from pathlib import Path
from tempfile import NamedTemporaryFile
from fastapi import UploadFile

class IngestionService:

    def __init__(
        self,
        chunking_service,
        embedding_service,
        sparse_service,
        vector_service,
    ):
        self.chunking = chunking_service
        self.dense = embedding_service
        self.sparse = sparse_service
        self.vector = vector_service

    async def ingest(self, pdf_path: str, user_id:int):
        # file: UploadFile,
        # with NamedTemporaryFile(delete=False, suffix="pdf") as temp_file:
        #     temp_file.write(await file.read())
        #     pdf_path = temp_file.name
        try:
            print("1 - chunking")

            chunks = self.chunking.chunk_pdf(pdf_path)

            for chunk in chunks:
                chunk.metadata["user_id"] = user_id
            # print(chunks[0])

            texts = [chunk.page_content for chunk in chunks]
            
            print("Dense")
            dense_embeddings = await self.dense.embed_documents(texts)
            
            print("sparse")
            sparse_embeddings = await self.sparse.embed_documents(texts)

            await self.vector.create_collection()

            await self.vector.upsert(chunks, dense_embeddings, sparse_embeddings)
           
            print("Done vectore store")
            return {"status": "success"}
        except Exception:
            import traceback
            traceback.print_exc()
        finally:
            Path(pdf_path).unlink(missing_ok=True)