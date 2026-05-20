def calculator_tool(state):

    question = state["question"]

    try:
        result = eval(question)

        answer = f"Calculation result: {result}"

    except Exception:
        answer = "Unable to calculate."

    return {
        **state,
        "answer": answer,
        "new_messages": [
            f"User: {question}",
            f"Assistant: {answer}"
        ]
    }