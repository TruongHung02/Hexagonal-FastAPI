# src/application/services/cache_service.py
from abc import ABC, abstractmethod
from typing import Any, Optional

class CacheService(ABC):
    @abstractmethod
    async def get_cached_data(self, key: str) -> Optional[Any]:
        pass
    
    @abstractmethod
    async def cache_data(self, key: str, data: Any, expire_seconds: Optional[int] = None) -> bool:
        pass
    
    @abstractmethod
    async def invalidate_cache(self, key: str) -> bool:
        pass
    
    @abstractmethod
    async def has_cached_data(self, key: str) -> bool:
        pass