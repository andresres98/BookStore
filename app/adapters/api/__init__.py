
from fastapi import FastAPI
from app.adapters.api.author_routes import router as author_router

app = FastAPI()

app.include_router(author_router)