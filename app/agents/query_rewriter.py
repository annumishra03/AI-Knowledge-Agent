from app.config.llm import llm


def rewrite_question(state):

    question = state["question"]
    history = state.get("chat_history", [])

    prompt = f"""
You are a query rewriting assistant.

Convert the user message into a standalone search query.

Rules:
- Use chat history if needed
- Resolve references
- Keep it short and meaningful for retrieval
- DO NOT answer

Chat History:
{chr(10).join(history[-6:])}

Question:
{question}

Return only the rewritten query:
"""

    response = llm.invoke(prompt)

    retrieval_query = response.content.strip()
    print("REWRITE NODE EXECUTED")
    print("QUESTION:", question)
    print("REWRITTEN:", retrieval_query)
    return {
        **state,
        "retrieval_query": retrieval_query
    }