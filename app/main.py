from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from motor.motor_asyncio import AsyncIOMotorClient
import redis.asyncio as redis
import sentry_sdk
from contextlib import asynccontextmanager
from datetime import datetime
from app.core.config import settings
from app.core.database import get_db
from app.api.v1.api import api_router
from app.services.store_integrations import StoreIntegrationManager
from app.services.scraper_service import ScraperService
from app.migrations.registry import run_migrations

# Initialize Sentry for error tracking
if settings.SENTRY_DSN:
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        environment=settings.ENVIRONMENT,
        traces_sample_rate=1.0,
    )

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    app.mongodb_client = AsyncIOMotorClient(settings.MONGODB_URL)
    app.mongodb = app.mongodb_client[settings.DATABASE_NAME]
    
    # Run database migrations
    print("Running database migrations...")
    await run_migrations(app.mongodb)
    print("Migrations completed")
    
    app.redis = redis.from_url(settings.REDIS_URL, encoding="utf-8", decode_responses=True)

    # Initialize services
    app.store_manager = StoreIntegrationManager()
    app.scraper_service = ScraperService()

    # Start scheduled tasks
    if not settings.TESTING:
        app.scraper_service.start_scheduled_scraping()

    yield

    # Shutdown
    await app.mongodb_client.close()
    await app.redis.close()
    await app.store_manager.cleanup()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    docs_url=f"{settings.API_V1_STR}/docs" if settings.SHOW_DOCS else None,
    redoc_url=f"{settings.API_V1_STR}/redoc" if settings.SHOW_DOCS else None,
    openapi_url=f"{settings.API_V1_STR}/openapi.json" if settings.SHOW_DOCS else None,
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Error handler
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
            "timestamp": datetime.utcnow().isoformat()
        }
    )

# Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "version": settings.VERSION,
        "timestamp": datetime.utcnow().isoformat()
    }

# Add API router
app.include_router(api_router, prefix=settings.API_V1_STR)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        workers=settings.WORKERS_COUNT
    )