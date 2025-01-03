from fastapi import APIRouter

router = APIRouter()

@router.get("/products")
async def get_products():
    pass
