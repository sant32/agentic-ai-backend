from langgraph.graph import END


def prompt_router(state):

    if state["is_prompt_attack"]:
        return END

    return "rewrite"