from fastapi import FastAPI
from app.api.routes import route

start = FastAPI(title="Knowledge Agent")

start.include_router(route)