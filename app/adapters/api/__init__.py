
from fastapi import FastAPI

from app.adapters.api.review_routes import router as review_router
from app.adapters.api.customer_routes import router as customer_router
from app.adapters.api.author_routes import router as author_router
from app.adapters.api.bookcategory_routes import router as bookcategory_router
from app.adapters.api.editorial_routes import router as editorial_router
from app.adapters.api.book_routes import router as book_router
from app.adapters.api.purchase_routes import router as purchase_router
from app.adapters.api.purchase_detail_routes import router as purchase_detail_router
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todos los orígenes
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos
    allow_headers=["*"],  # Permitir todos los encabezados
)

app.include_router(author_router)
app.include_router(bookcategory_router)
app.include_router(editorial_router)
app.include_router(book_router)
app.include_router(customer_router)
app.include_router(review_router)
app.include_router(purchase_router)
app.include_router(purchase_detail_router)
