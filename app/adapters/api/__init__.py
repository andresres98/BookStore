
from fastapi import FastAPI
from app.adapters.api.author_routes import router as author_router
from app.adapters.api.bookcategory_routes import router as bookcategory_router

app = FastAPI()

app.include_router(author_router)
app.include_router(bookcategory_router)