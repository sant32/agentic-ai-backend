from langgraph.graph import StateGraph, START, END

from app.graph.state import GraphState

from app.graph.nodes.pii import pii_node
from app.graph.nodes.prompt_guard import prompt_guard_node
from app.graph.nodes.query_rewrite import rewrite_node
from app.graph.nodes.retrieve_node import retrieve_node
from app.graph.nodes.rerank_node import rerank_node
from app.graph.nodes.context_builder import context_builder_node
from app.graph.nodes.generate import generate_node

from app.graph.routers import prompt_router


def build_graph():

    builder = StateGraph(GraphState)

    # Nodes
    builder.add_node("pii", pii_node)
    builder.add_node("prompt_guard", prompt_guard_node)
    builder.add_node("rewrite", rewrite_node)
    builder.add_node("retrieve", retrieve_node)
    builder.add_node("rerank", rerank_node)
    builder.add_node("context_builder", context_builder_node)
    builder.add_node("generate", generate_node)

    # Start
    builder.add_edge(START, "pii")

    # Linear flow
    builder.add_edge("pii", "prompt_guard")

    # Router
    builder.add_conditional_edges(
        "prompt_guard",
        prompt_router,
        {
            "rewrite": "rewrite",
            "end": END,
        },
    )

    builder.add_edge("rewrite", "retrieve")
    builder.add_edge("retrieve", "rerank")
    builder.add_edge("rerank", "context_builder")
    builder.add_edge("context_builder", "generate")

    # Finish
    builder.add_edge("generate", END)

    return builder.compile()