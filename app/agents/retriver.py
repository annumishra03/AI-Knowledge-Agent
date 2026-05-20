from app.vectorStore.store import retrieve_documents


def retrieve(state):

    query = state.get("retrieval_query") or state["question"]

    docs = retrieve_documents(query)

    context = [doc.page_content for doc in docs]

    return {
        **state,
        "context": context
    }