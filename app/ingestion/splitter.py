from langchain_text_splitters import RecursiveCharacterTextSplitter

def split_documents(documents):

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=700,
        chunk_overlap=120,
        separators=["\n\n", "\n", ".", " ", ""]
    )
    
    chunks = text_splitter.split_documents(documents)

    return chunks