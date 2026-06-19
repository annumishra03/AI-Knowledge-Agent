import time
from app.config.llm import llm
from langchain_core.messages import AIMessage
from langsmith import traceable

@traceable
def generate_answer(state):
    question = state.get("retrieval_query", state['question'])
    context = state.get("context", [])
    context_text = "\n\n".join(context)
    history = state.get("messages", [])
    history_text = "\n".join(
        msg.content
        for msg in history[-10:]
    )

    summary = state.get("summary", "")

    prompt = f"""
    You are a helpful AI assistant.

    Answer ONLY using the provided context.
    If answer is not present, say:
    "I don't know based on the given documents."

    RULES:
    - If user question depends on previous messages, you MUST use chat history.
    - If context is missing, ask a clarification question.
    - NEVER answer generically if chat history or summary contains relevant entity (movie, person, topic).

    Use CONTEXT + CHAT HISTORY + Summary.
    Conversation Summary:

    {summary}
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

    answer = ""
    start = time.time()
    for chunk in llm.stream(prompt):
        answer += chunk.content

    return {
        **state,
        "answer": answer,
        "messages": [
                AIMessage(content=answer)
            ],
    }

@traceable
def direct_answer(state):

    question = state.get("retrieval_query", state['question'])
    
    summary = state.get("summary", [])
    history = state.get("messages", [])
    history_text = "\n".join(
        msg.content
        for msg in history[-10:]
    )

    prompt = f"""
    You are a helpful AI assistant.
    Rules
    - If user question depends on previous messages, you MUST use chat history and summary otherwise dont use.
    - Chat History empty then answer according to question
    - Don't describe much in answer just upto mark answer if not ask to explain or describe or detail
    Use CONTEXT + CHAT HISTORY + Summary.
    Conversation Summary:

    {summary}
    Chat History:
    Chat History:
    {history_text}

    Question:
    {question}
    INSTRUCTIONS:
    1. First check chat history.
    2. If still unclear, ask a clarification question.
    3. Only answer directly if fully certain.
    """

    answer = ""
    
    for chunk in llm.stream(prompt):
        answer += chunk.content


    return {
        **state,
        "answer": answer,
        "messages": [
            AIMessage(content=answer)
        ],
    }