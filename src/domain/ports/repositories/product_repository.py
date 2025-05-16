from abc import ABC, abstractmethod
from typing import List, Optional

from src.domain.models import Product, User

class ProductRepository(ABC):
    @abstractmethod
    async def get_all(self) -> List[Product]:
        pass

    @abstractmethod
    async def get_by_id(self, product_id: int) -> Optional[Product]:
        pass

    @abstractmethod
    async def create(self, product: Product) -> Product:
        pass

    @abstractmethod
    async def update(self, product: Product) -> Product:
        pass

    @abstractmethod
    async def delete(self, product_id: int) -> bool:
        pass