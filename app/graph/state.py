from typing import Annotated, TypedDict, List
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage

class GraphState(TypedDict):

    messages: Annotated[list[BaseMessage], add_messages]
    # user input
    question: str

    # retrieval optimized query
    retrieval_query: str

    # routing
    route: str

    # RAG
    context: List[str]

    # output
    answer: str
    summary: str


    # # memory
    # chat_history: List[str]
    # new_messages: List[str]