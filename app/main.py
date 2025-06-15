from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
import redis.asyncio as redis

from app.api import auth, contacts
from app.core.config import settings
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
    redis_client = redis.from_url(
        f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
        password=settings.REDIS_PASSWORD,
        encoding="utf-8",
        decode_responses=True,
    )
    await FastAPILimiter.init(redis_client)


@app.get("/")
async def root():
    return {"message": "Welcome to Contacts API"} 