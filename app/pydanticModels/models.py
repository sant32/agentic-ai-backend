from pydantic import BaseModel, Field

class RewrittenQuery(BaseModel):
    rewritten_query: str = Field(
        description=
        
       
        """
        You are a query rewriting assistant for Retrieval-Augmented Generation (RAG).

Rewrite the user's question into a concise, retrieval-optimized search query.

Rules:
- Preserve the original intent.
- Expand abbreviations when helpful (e.g. JWT → JSON Web Token).
- Do not answer the question.
- Do not add new information.
- Keep it short (one sentence).
- Return only the rewritten query.
"""
    )



class RetrievedChunk(BaseModel):
    chunk_id: str
    document_id: str
    file_name: str
    page: int
    score: float
    content: str


class GeneratedAnswer(BaseModel):
    answer: str = Field(
        description="Answer to the user's question using only the provided context."
    )