from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
import redis.asyncio as redis

from app.api import auth, contacts
from app.core.config import settings
from app.core.cache import cache
from app.db.session import engine
from app.models import Base

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])
app.include_router(contacts.router, prefix=f"{settings.API_V1_STR}/contacts", tags=["contacts"])


@app.on_event("startup")
async def startup():
    """
    Initialize Redis connection, FastAPI Limiter, and cache on application startup.
    
    This function is called when the FastAPI application starts up.
    It establishes a connection to Redis and initializes the rate limiter and cache.
    """
    # Initialize Redis for rate limiting
    redis_client = redis.from_url(
        f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
        password=settings.REDIS_PASSWORD,
        encoding="utf-8",
        decode_responses=True,
    )
    await FastAPILimiter.init(redis_client)
    
    # Initialize cache
    await cache.init_cache()


@app.on_event("shutdown")
async def shutdown():
    """
    Clean up Redis connections on application shutdown.
    """
    await cache.close_cache()


@app.get("/")
async def root():
    """
    Root endpoint that returns a welcome message.
    
    Returns:
        dict: A welcome message for the Contacts API
    """
    return {"message": "Welcome to Contacts API"} 