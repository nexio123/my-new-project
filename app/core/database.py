from motor.motor_asyncio import AsyncIOMotorClient
from typing import AsyncGenerator
from fastapi import Depends
from ..core.config import settings

async def get_db() -> AsyncGenerator:
    """
    Get database connection.
    Used as a FastAPI dependency.
    """
    try:
        client = AsyncIOMotorClient(settings.MONGODB_URL)
        database = client[settings.DATABASE_NAME]
        yield database
    finally:
        client.close()

async def init_db(database):
    """Initialize database with required collections and indexes"""
    # Users collection indexes
    await database.users.create_index("email", unique=True)
    await database.users.create_index(["email", "hashed_password"])
    await database.users.create_index("created_at")

    # Add logging for successful initialization
    print(f"Initialized database: {settings.DATABASE_NAME}")
    collections = await database.list_collection_names()
    print(f"Available collections: {collections}")

async def get_collection(collection_name: str, db=Depends(get_db)):
    """Get a specific collection"""
    return db[collection_name]
