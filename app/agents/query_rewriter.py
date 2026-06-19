from app.config.llm import llm
from langsmith import traceable

@traceable
def rewrite_question(state):

    question = state["question"]
    history = state.get("messages", [])
    history_text = "\n".join(
        msg.content
        for msg in history[-10:]
    )
    prompt = f"""
You are a query rewriting assistant.

Convert the user message into a standalone search query.

Rules:
- Use chat history if needed
- Resolve references
- Keep it short and meaningful for retrieval
- DO NOT answer

Chat History:
{history_text}

Question:
{question}

Return only the rewritten query:
"""

    response = llm.invoke(prompt)

    retrieval_query = response.content.strip()
    
    return {
        **state,
        "retrieval_query": retrieval_query
    }