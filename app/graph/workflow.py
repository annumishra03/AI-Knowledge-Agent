from langgraph.graph import StateGraph, END
from app.agents.memory import update_memory
from app.agents.query_rewriter import rewrite_question
from app.graph.state import GraphState
from app.agents.answer import generate_answer, direct_answer
from app.agents.router import route_question
from app.agents.retriver import retrieve
from app.tools.web_tool import web_tool
from app.tools.calculator import calculator_tool

def decide_route(state):
    route = route_question(state)
    return {'route': route['route']}

def decide_next(state):
    return state["route"]

graph = StateGraph(GraphState)

graph.add_node("rewrite", rewrite_question)
graph.add_node("router", decide_route)
graph.add_node("retrieve_node", retrieve)
graph.add_node("calculator", calculator_tool)
graph.add_node("web", web_tool)
graph.add_node("generate", generate_answer)
graph.add_node("direct_node", direct_answer)
graph.add_node("memory_node", update_memory)
graph.set_entry_point("rewrite")

graph.add_edge("rewrite", "router")
# graph.set_entry_point("router")
graph.add_conditional_edges("router", decide_next,{
    "rag": "retrieve_node",
    "direct": "direct_node",
    "web": "web",
    "calculator": "calculator",
    "clarify": END
})

graph.add_edge("retrieve_node", "generate")
graph.add_edge("generate", "memory_node")
graph.add_edge("direct_node", "memory_node")
graph.add_edge("web", "memory_node")
graph.add_edge("calculator", "memory_node")

graph.add_edge("memory_node", END)

app_graph = graph.compile()