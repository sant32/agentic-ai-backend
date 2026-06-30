from __future__ import annotations

from uuid import uuid4
from pathlib import Path
import hashlib
from langchain_community.document_loaders import PyPDFLoader

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


class ChunkingService:
    """
    Handles recursive chunking of documents for RAG pipelines.
    """

    def __init__(
        self,
        chunk_size: int = 800,
        chunk_overlap: int = 150,
    ) -> None:

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=[
                "\n\n",
                "\n",
                ". ",
                "? ",
                "! ",
                "; ",
                ", ",
                " ",
                "",
            ],
            keep_separator=True,
            is_separator_regex=False,
        )



    @staticmethod
    def _generate_document_id(source: str) -> str:
        """
        Generate a deterministic document id based on filename and file path.
        """

        document_name = Path(source).stem

        file_hash = hashlib.sha256(
            source.encode("utf-8")
        ).hexdigest()

        return f"{document_name}_{file_hash[:8]}"

    def chunk_text(
        self,
        text: str,
        metadata: dict | None = None,
    ) -> list[Document]:
        """
        Chunk a raw text string.
        """

        metadata = metadata or {}

        documents = self.splitter.create_documents(
            texts=[text],
            metadatas=[metadata],
        )

        return self._enrich_metadata(documents)

    def chunk_pdf(
        self,
        pdf_path: str
    ):
        loader = PyPDFLoader(pdf_path)

        documents = loader.load()

        chunks = self.splitter.split_documents(documents)

        return self._enrich_metadata(chunks)

    def _enrich_metadata(
        self,
        chunks: list[Document],
    ) -> list[Document]:
        """
        Add useful metadata to every chunk.
        """

        total_chunks = len(chunks)
        source = chunks[0].metadata.get("source", "")
        file_name = Path(source).name if source else ""

        document_id = self._generate_document_id(source)

        for index, chunk in enumerate(chunks):

            metadata = dict(chunk.metadata)

            metadata.pop("producer", None)
            metadata.pop("creator", None)
            metadata.pop("keywords", None)
            metadata.pop("trapped", None)

            metadata["document_id"] = document_id
            metadata["file_name"] = file_name
            
            metadata["chunk_id"] = f"{document_id}_chunk{index}"
            metadata["chunk_index"] = index
            metadata["total_chunks"] = total_chunks
            metadata["chunk_size"] = len(chunk.page_content)

            chunk.metadata = metadata
        # print("Metaa -:",chunks)

        return chunks