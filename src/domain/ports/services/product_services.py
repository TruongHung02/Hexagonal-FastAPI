from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.models import Product, User

class ProductService(ABC):
    @abstractmethod
    async def get_all_products(self) -> List[Product]:
        pass
    
    @abstractmethod
    async def get_product(self, product_id: int) -> Optional[Product]:
        pass
    
    @abstractmethod
    async def create_product(self, product: Product) -> Product:
        pass
    
    @abstractmethod
    async def update_product(self, product_id: int, product: Product) -> Optional[Product]:
        pass
    
    @abstractmethod
    async def delete_product(self, product_id: int) -> bool:
        pass
