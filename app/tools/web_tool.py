import os
from app.config.llm import llm
from tavily import TavilyClient
from dotenv import load_dotenv

load_dotenv()
client = TavilyClient(
    api_key=os.getenv("TAVILY_API_KEY")
)

def web_tool(state):

    question = state.get("retrieval_query", state['question'])
    history = state.get("chat_history", [])

    response = client.search(
        query=question,
        search_depth="basic",
        max_results=3
    )

    results = response["results"]

    context = "\n\n".join(
        [r["content"] for r in results]
    )
    history_text = "\n".join(history[-5:])

    prompt = f"""
    You are a helpful AI assistant.

    Use conversation history if needed.
    Answer the user's question using the web search context below.
    CHAT HISTORY:
    {history_text}

    WEB CONTEXT:
    {context}

    QUESTION:
    {question}

    Rules:
    - Give concise accurate answer
    - Do not dump raw context
    - Summarize intelligently
    """

    response = llm.invoke(prompt)

    answer = response.content

    return {
        **state,
        "answer": answer,
        "new_messages": [
            f"User: {question}",
            f"Assistant: {answer}"
        ]
    }