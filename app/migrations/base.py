from datetime import datetime
from typing import List

class Migration:
    def __init__(self, version: str, description: str):
        self.version = version
        self.description = description
        self.executed_at = None

    async def up(self, db) -> None:
        """Execute the migration"""
        raise NotImplementedError

    async def down(self, db) -> None:
        """Rollback the migration"""
        raise NotImplementedError

class MigrationManager:
    def __init__(self, db):
        self.db = db
        self.migrations: List[Migration] = []

    def register_migration(self, migration: Migration):
        self.migrations.append(migration)

    async def init_migrations_collection(self):
        collections = await self.db.list_collection_names()
        if 'migrations' not in collections:
            await self.db.create_collection('migrations')
            await self.db.migrations.create_index('version', unique=True)

    async def run_pending(self):
        await self.init_migrations_collection()

        # Sort migrations by version
        self.migrations.sort(key=lambda m: m.version)

        # Get executed migrations
        executed = await self.db.migrations.find().to_list(None)
        executed_versions = {m['version'] for m in executed}

        # Run pending migrations
        for migration in self.migrations:
            if migration.version not in executed_versions:
                print(f"Running migration {migration.version}: {migration.description}")
                try:
                    await migration.up(self.db)
                    await self.db.migrations.insert_one({
                        'version': migration.version,
                        'description': migration.description,
                        'executed_at': datetime.utcnow()
                    })
                    print(f"Successfully completed migration {migration.version}")
                except Exception as e:
                    print(f"Error running migration {migration.version}: {str(e)}")
                    raise

    async def rollback_last(self):
        # Get last executed migration
        last_migration = await self.db.migrations.find_one(
            sort=[('version', -1)]
        )

        if not last_migration:
            print("No migrations to rollback")
            return

        # Find corresponding migration object
        migration_obj = next(
            (m for m in self.migrations if m.version == last_migration['version']),
            None
        )

        if migration_obj:
            print(f"Rolling back migration {migration_obj.version}: {migration_obj.description}")
            try:
                await migration_obj.down(self.db)
                await self.db.migrations.delete_one({'version': migration_obj.version})
                print(f"Successfully rolled back migration {migration_obj.version}")
            except Exception as e:
                print(f"Error rolling back migration {migration_obj.version}: {str(e)}")
                raise