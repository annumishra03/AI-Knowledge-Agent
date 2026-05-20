from app.config.embedding import vectorstore

def add_documents(chunks):

    vectorstore.add_documents(chunks)


def retrieve_documents(query: str, k: int = 3):

    results = vectorstore.similarity_search(query, k=k)

    return results