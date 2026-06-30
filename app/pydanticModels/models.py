from pydantic import BaseModel, Field

class RewrittenQuery(BaseModel):
    rewritten_query: str = Field(
        description="Optimized query for semantic vector search."
    )