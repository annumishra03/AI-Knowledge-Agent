from fastapi import APIRouter, UploadFile, File
import os

from app.ingestion.loader import load_pdf
from app.ingestion.splitter import split_documents
from app.schemas.request import QuestionRequest
from app.vectorStore.store import add_documents
from app.graph.workflow import app_graph
route = APIRouter()

from app.memory.redis_memory import session_store

@route.get("/")
def health():
    return {"status": "running"}

@route.post("/upload")
async def upload_documents(file: UploadFile = File(...)):
    upload_dir = "data/docs"
    os.makedirs(upload_dir, exist_ok=True)

    file_path = os.path.join(upload_dir, file.filename)

    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)

    print("\n===== FILE SAVED =====")
    print(file_path)

    # LOAD PDF
    documents = load_pdf(file_path)

    print("\n===== DOCUMENTS LOADED =====")
    print(f"Pages loaded: {len(documents)}")

    # SPLIT INTO CHUNKS
    chunks = split_documents(documents)

    print("\n===== CHUNKS CREATED =====")
    print(f"Chunks count: {len(chunks)}")

    # STORE IN CHROMA
    add_documents(chunks)

    print("\n===== DOCUMENTS STORED IN CHROMADB =====")

    return {
        "message": "File uploaded successfully",
        "filename": file.filename
    }

@route.post("/ask")
def ask(req: QuestionRequest):
    history = session_store.get(req.session_id)
    print(req.session_id, history)
    state = {
        "question": req.question,
        "retrieval_query": "",
        "chat_history": history,
        "context": [],
        "answer": "",
        "route": "",
        "new_messages": []   # 👈 IMPORTANT
    }

    result = app_graph.invoke(state)

    # append only new messages
    session_store.append(
        req.session_id,
        result.get("new_messages", [])
    )
    
    return result

    