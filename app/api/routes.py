import time
from fastapi import APIRouter, Depends, UploadFile, File
import os

from fastapi.responses import StreamingResponse

from app.ingestion.loader import load_pdf
from app.ingestion.splitter import split_documents
from app.schemas.request import QuestionRequest
from app.vectorStore.store import add_documents
from app.graph.workflow import app_graph
from langchain_core.messages import HumanMessage
from langchain_core.messages import AIMessageChunk

route = APIRouter()

from app.memory.redis_memory import RedisSessionStore
session_store = RedisSessionStore()

from app.auth.dependencies import (
    get_current_user
)

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

@route.post("/ask-stream")
async def ask_stream(req: QuestionRequest, user = Depends(get_current_user)):
    print(user)
    state = {
        "messages": [
            HumanMessage(content=req.question)
        ],
        "question": req.question,
        "retrieval_query": "",
        "context": [],
        "answer": "",
        "route": "",
    }

    async def generate():

        config = {
            "configurable": {
                "thread_id": req.session_id
            }
        }

        full_response = ""

        try:

            for event, metadata in app_graph.stream(
                state,
                config=config,
                stream_mode="messages"
            ):
                if not isinstance(event, AIMessageChunk):
                    continue

                node = metadata.get("langgraph_node")
                if event.content and node in ["direct_node", "retrieve_node", "web"]:
                    yield event.content

        except Exception as e:
            print("STREAM ERROR:", str(e))
            raise

    return StreamingResponse(
        generate(),
        media_type="text/event-stream"
    )
    
@route.get("/check-state")
def getFullState():
    config = {
    "configurable": {
        "thread_id": "bollywood"
    }
    }

    state = app_graph.get_state(config)

    print(state)
    return state