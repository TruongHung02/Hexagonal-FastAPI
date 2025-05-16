# src/infrastructure/cache.py
from typing import AsyncGenerator
from fastapi import Depends
from redis.asyncio import Redis
from src.infrastructure.config import settings

async def get_redis_client() -> Redis:
    redis = Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=settings.REDIS_DB,
        password=settings.REDIS_PASSWORD,
        decode_responses=True
    )
    return redis

# Dependency để cung cấp Redis client
async def get_redis_dependency() -> AsyncGenerator[Redis, None]:
    redis = await get_redis_client()
    try:
        yield redis
    finally:
        await redis.close()
