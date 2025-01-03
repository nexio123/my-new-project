from fastapi import FastAPI
from api.v1.endpoints import auth, products, stores, shopping_lists

app = FastAPI()

app.include_router(auth.router, prefix="/api/v1")
app.include_router(products.router, prefix="/api/v1")
app.include_router(stores.router, prefix="/api/v1")
app.include_router(shopping_lists.router, prefix="/api/v1")
