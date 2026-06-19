# def update_memory(state):

#     question = state["question"]
#     answer = state["answer"]

#     history = state.get("chat_history", [])

#     history.append(f"User: {question}")
#     history.append(f"Assistant: {answer}")

#     return {
#         **state,
#         "chat_history": history
#     }

from langchain_core.messages import HumanMessage

from app.config import llm

def summarize_node(state):

    messages = state["messages"]

    summary = state.get("summary", "")

    if summary:

        prompt = f"""
        Existing summary:

        {summary}

        Update this summary using new messages.
        Keep important facts and decisions.
        """

    else:

        prompt = """
        Create a concise summary of this conversation.
        Include:
        - Important facts
        - User goals
        - Decisions made
        """

    response = llm.invoke(
        messages + [HumanMessage(content=prompt)]
    )

    return {
        **state,
        "summary": response.content
    }