from langgraph.graph import StateGraph, END
from app.agents.summary import summarize_node
from app.agents.query_rewriter import rewrite_question
from app.graph.state import GraphState
from app.agents.answer import generate_answer, direct_answer
from app.agents.router import route_question
from app.agents.retriver import retrieve
from app.tools.web_tool import web_tool
from app.tools.calculator import calculator_tool
from langgraph.checkpoint.memory import InMemorySaver

def decide_route(state):
    route = route_question(state)
    return {'route': route['route']}

def decide_next(state):
    return state["route"]

def finalize_node(state):
    return state


def should_summarize(state):

    messages = state.get("messages", [])

    if len(messages) > 10:
        return "summarize"

    return "end"

graph = StateGraph(GraphState)

graph.add_node("rewrite", rewrite_question)
graph.add_node("router", decide_route)
graph.add_node("retrieve_node", retrieve)
graph.add_node("calculator", calculator_tool)
graph.add_node("web", web_tool)
graph.add_node("finalize", finalize_node)
graph.add_node("generate", generate_answer)
graph.add_node("direct_node", direct_answer)
graph.add_node("summarize_node", summarize_node)

graph.set_entry_point("rewrite")

graph.add_edge("rewrite", "router")

graph.add_conditional_edges("router", decide_next, {
    "rag": "retrieve_node",
    "direct": "direct_node",
    "web": "web",
    "calculator": "calculator",
    "clarify": END
})

graph.add_edge("retrieve_node", "generate")
graph.add_edge("generate", "finalize")
graph.add_edge("direct_node", "finalize")
graph.add_edge("web", "finalize")
graph.add_edge("calculator", "finalize")
graph.add_conditional_edges(
    "finalize",
    should_summarize,
    {
        "summarize_node": "summarize_node",
        "end": END
    }
)

graph.add_edge("summarize_node", END)
checkpointer = InMemorySaver()

app_graph = graph.compile(
    checkpointer=checkpointer
)
