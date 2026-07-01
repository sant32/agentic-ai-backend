from app.graph.builder import build_graph
from app.schemas.auth import SourceResponse, SearchResponse

class GraphService:

    def __init__(self):
        self.graph = build_graph()

    async def search(self, state):
        result = await self.graph.ainvoke(state)

        return SearchResponse(
            answer=result.get("answer"),
            sources=[
                SourceResponse(
                    file_name=chunk.file_name,
                    page=chunk.page,
                    score=chunk.score,
                    content=chunk.content,
                )
                for chunk in result.get("retrieved_chunks", [])
            ],
        )

