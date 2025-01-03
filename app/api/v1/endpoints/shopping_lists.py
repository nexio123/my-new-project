from fastapi import APIRouter

router = APIRouter()

@router.get("/shopping-lists")
async def get_shopping_lists():
    pass
