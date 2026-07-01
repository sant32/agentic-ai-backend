

class ContextBuilderService:

    def build(
        self,
        chunks: list
    ) -> str:

        if not chunks:
            return ""

        sections = []

        for chunk in chunks:

            sections.append(
                f"""Source: {chunk.file_name}
Page: {chunk.page}

{chunk.content}
"""
            )

        return "\n\n------------------------------\n\n".join(
            sections
        )