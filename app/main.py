from fastapi import FastAPI
from app.api.routes import route
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()
start = FastAPI(title="Knowledge Agent")
start.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
start.include_router(route)