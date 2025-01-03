from ..base import Migration

class InitialUserSchemaMigration(Migration):
    def __init__(self):
        super().__init__(
            version="001",
            description="Initial user schema setup"
        )

    async def up(self, db):
        # Create users collection if it doesn't exist
        collections = await db.list_collection_names()
        if 'users' not in collections:
            await db.create_collection('users')

        # Create indexes
        await db.users.create_index("email", unique=True)
        await db.users.create_index(["email", "hashed_password"])
        await db.users.create_index("created_at")

    async def down(self, db):
        # Drop users collection
        await db.users.drop()