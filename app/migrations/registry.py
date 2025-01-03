from typing import List
from .base import Migration, MigrationManager
from .versions.001_initial_user_schema import InitialUserSchemaMigration

def get_migrations() -> List[Migration]:
    return [
        InitialUserSchemaMigration(),
        # Add new migrations here
    ]

async def run_migrations(db) -> None:
    manager = MigrationManager(db)
    
    # Register all migrations
    for migration in get_migrations():
        manager.register_migration(migration)
    
    # Run pending migrations
    await manager.run_pending()