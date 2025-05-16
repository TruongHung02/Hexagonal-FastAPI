# src/application/services/cache_service.py
from typing import Any, Optional
from src.domain.ports.services import CacheService
from src.domain.ports.repositories import CacheRepository

class CacheServiceImpl(CacheService):
    def __init__(self, cache_repository: CacheRepository):
        self.cache_repository = cache_repository
    
    async def get_cached_data(self, key: str) -> Optional[Any]:
        return await self.cache_repository.get(key)
    
    async def cache_data(self, key: str, data: Any, expire_seconds: Optional[int] = None) -> bool:
        return await self.cache_repository.set(key, data, expire_seconds)
    
    async def invalidate_cache(self, key: str) -> bool:
        return await self.cache_repository.delete(key)
    
    async def has_cached_data(self, key: str) -> bool:
        return await self.cache_repository.exists(key)