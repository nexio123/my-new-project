import asyncio
import click
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings
from app.migrations.registry import run_migrations
from app.migrations.base import MigrationManager

async def get_db():
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    return client[settings.DATABASE_NAME]

@click.group()
def cli():
    """Database migration management tool"""
    pass

@cli.command()
def migrate():
    """Run all pending migrations"""
    async def run():
        db = await get_db()
        await run_migrations(db)

    asyncio.run(run())
    click.echo("Migrations completed successfully")

@cli.command()
def rollback():
    """Rollback the last migration"""
    async def run():
        db = await get_db()
        manager = MigrationManager(db)
        await manager.rollback_last()

    asyncio.run(run())
    click.echo("Rollback completed successfully")

@cli.command()
def status():
    """Show migration status"""
    async def run():
        db = await get_db()
        migrations = await db.migrations.find().sort('version', 1).to_list(None)
        
        click.echo("Applied migrations:")
        for migration in migrations:
            click.echo(f"  {migration['version']}: {migration['description']} "
                      f"(applied at {migration['executed_at']})")

    asyncio.run(run())

if __name__ == '__main__':
    cli()