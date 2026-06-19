import os
from app.config.llm import llm
from tavily import TavilyClient
from dotenv import load_dotenv
from langchain_core.messages import AIMessage
from langsmith import traceable
load_dotenv()
client = TavilyClient(
    api_key=os.getenv("TAVILY_API_KEY")
)

@traceable
def web_tool(state):

    question = state.get("retrieval_query", state['question'])
    summary = state.get("summary", [])
    history = state.get("messages", [])

    response = client.search(
        query=question,
        search_depth="basic",
        max_results=3
    )

    results = response["results"]

    context = "\n\n".join(
        [r["content"] for r in results]
    )
    history_text = "\n".join(
        msg.content
        for msg in history[-10:]
    )

    prompt = f"""
    You are a helpful AI assistant.

    Use conversation history and summary if needed.
    Answer the user's question using the web search context below.

    Conversation Summary:

    {summary}

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