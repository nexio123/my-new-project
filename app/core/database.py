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
        yield client[settings.DATABASE_NAME]
    finally:
        client.close()

async def init_indexes(db):
    """Initialize database indexes"""
    # Users collection
    await db.users.create_index("email", unique=True)
    await db.users.create_index("created_at")

    # Products collection
    await db.products.create_index([
        ("name", "text"),
        ("brand", "text"),
        ("category", "text")
    ])
    await db.products.create_index("store")
    await db.products.create_index("last_updated")

    # Shopping lists collection
    await db.shopping_lists.create_index("owner_id")
    await db.shopping_lists.create_index("shared_with.user_id")
    await db.shopping_lists.create_index("created_at")

    # Price history collection
    await db.price_history.create_index([
        ("product_id", 1),
        ("store", 1),
        ("timestamp", -1)
    ])

    # Store locations collection
    await db.store_locations.create_index([
        ("location", "2dsphere")
    ])

    # Notifications collection
    await db.notifications.create_index([
        ("user_id", 1),
        ("read", 1),
        ("created_at", -1)
    ])

    # Cache collection
    await db.cache.create_index(
        "expires_at",
        expireAfterSeconds=0
    )

async def get_collection(collection_name: str, db=Depends(get_db)):
    """Get a specific collection"""
    return db[collection_name]