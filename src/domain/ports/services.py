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


class UserService(ABC):
    @abstractmethod
    async def get_user(self, user_id: int) -> Optional[User]:
        pass
    
    @abstractmethod
    async def get_user_by_email(self, email: str) -> Optional[User]:
        pass
    
    @abstractmethod
    async def create_user(self, user: User) -> User:
        pass
    
    @abstractmethod
    async def update_user(self, user_id: int, user: User) -> Optional[User]:
        pass
    
    @abstractmethod
    async def delete_user(self, user_id: int) -> bool:
        pass