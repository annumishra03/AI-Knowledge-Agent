from app.config.llm import llm

def generate_answer(state):
    question = state.get("retrieval_query", state['question'])
    context = state.get("context", [])
    context_text = "\n\n".join(context)
    history = state.get("chat_history", [])
    history_text = "\n".join(history[-6:])
    prompt = f"""
    You are a helpful AI assistant.

    Answer ONLY using the provided context.
    If answer is not present, say:
    "I don't know based on the given documents."

    RULES:
    - If user question depends on previous messages, you MUST use chat history.
    - If context is missing, ask a clarification question.
    - NEVER answer generically if chat history contains relevant entity (movie, person, topic).

    Use CONTEXT + CHAT HISTORY.

    Chat History:
    {history_text}

    Context:
    {context_text}

    Question:
    {question}
INSTRUCTIONS:
1. First check chat history.
2. If question refers to "that", "it", "same movie", "he", "she", resolve from history.
3. If still unclear, ask a clarification question.
4. Only answer directly if fully certain.
    """

    response = llm.invoke(prompt)
    answer = response.content
    return {
        **state,
        "answer": answer,

        # ONLY DELTA (IMPORTANT)
        "new_messages": [
            f"User: {question}",
            f"Assistant: {answer}"
        ]
    }

def direct_answer(state):

    question = state.get("retrieval_query", state['question'])
    
    history = state.get("chat_history", [])
    history_text = "\n".join(history[-6:])  # last few turns
    prompt = f"""
    You are a helpful AI assistant.
    Rules
    - If user question depends on previous messages, you MUST use chat history otherwise dont use.
    - Chat History empty then answer according to question
    - Don't describe much in answer just upto mark answer if not ask to explain or describe or detail

    Chat History:
    {history_text}

    Question:
    {question}
    INSTRUCTIONS:
    1. First check chat history.
    2. If still unclear, ask a clarification question.
    3. Only answer directly if fully certain.
    """

    response = llm.invoke(prompt)
    answer = response.content
    return {
        **state,
        "answer": answer,

        # ONLY DELTA (IMPORTANT)
        "new_messages": [
            f"User: {question}",
            f"Assistant: {answer}"
        ]
    }