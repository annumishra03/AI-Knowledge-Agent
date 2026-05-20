def update_memory(state):

    question = state["question"]
    answer = state["answer"]

    history = state.get("chat_history", [])

    history.append(f"User: {question}")
    history.append(f"Assistant: {answer}")

    return {
        **state,
        "chat_history": history
    }