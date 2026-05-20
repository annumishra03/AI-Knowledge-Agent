from typing import TypedDict, List


class GraphState(TypedDict):

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

    # memory
    chat_history: List[str]
    new_messages: List[str]