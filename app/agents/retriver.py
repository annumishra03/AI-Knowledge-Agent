from app.vectorStore.store import retrieve_documents
from langsmith import traceable

@traceable
def retrieve(state):

    query = state.get("retrieval_query") or state["question"]

    docs = retrieve_documents(query)

    context = [doc.page_content for doc in docs]

    return {
        **state,
        "context": context
    }