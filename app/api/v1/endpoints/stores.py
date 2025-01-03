from fastapi import APIRouter

router = APIRouter()

@router.get("/stores")
async def get_stores():
    pass
