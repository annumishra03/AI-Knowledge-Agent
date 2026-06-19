from langgraph.types import interrupt

def clarification_node(state):

    clarification = interrupt(
        {
            "message": "Please clarify your question."
        }
    )

    return {
        **state,
        "clarification": clarification
    }