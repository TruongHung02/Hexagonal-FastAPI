import json
from typing import Any, Optional

from redis.asyncio import Redis
from src.domain.ports.repositories import CacheRepository

class RedisCacheRepository(CacheRepository):
    def __init__(self, redis_client: Redis):
        self.redis = redis_client
    
    async def get(self, key: str) -> Optional[Any]:
        data = await self.redis.get(key)
        if data:
            try:
                return json.loads(data)
            except json.JSONDecodeError:
                return data
        return None
    
    async def set(self, key: str, value: Any, expire: Optional[int] = None) -> bool:
        try:
            if not isinstance(value, (str, bytes)):
                value = json.dumps(value)
            
            if expire:
                return await self.redis.setex(key, expire, value)
            else:
                return await self.redis.set(key, value)
        except Exception:
            return False
    
    async def delete(self, key: str) -> bool:
        return bool(await self.redis.delete(key))
    
    async def exists(self, key: str) -> bool:
        return bool(await self.redis.exists(key))