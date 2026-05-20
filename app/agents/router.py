from app.config.llm import llm
from app.graph.state import GraphState


def route_question(state: GraphState) -> str:
    question = state["question"]
    history = state.get("chat_history", [])

    prompt = f"""
    You are an intent router.

    Decide ONE route:

    OPTIONS:
    - rag → document/company/policy questions/answer depends on document content/private organization data/personal data
    - direct → general knowledge / conversational/public data of any field
    - web → real-time/latest information
    - calculator → math

    Use chat history if needed.

    CHAT HISTORY:
    {chr(10).join(history[-5:])}

    QUESTION:
    {question}

    Return only one word:
    rag / direct / web / calculator / clarify
    """

    response = llm.invoke(prompt)

    route = response.content.strip().lower()
    return {
        **state,
        "route": route
    }