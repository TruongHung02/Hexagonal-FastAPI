from datetime import datetime
from typing import List, Optional
import bcrypt

from src.domain.models import Product, User
from src.domain.ports.repositories import ProductRepository, UserRepository
from src.domain.ports.services import ProductService, UserService
from src.application.dtos import ProductDTO, UserDTO


class ProductServiceImpl(ProductService):
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository
    
    async def get_all_products(self) -> List[Product]:
        return await self.product_repository.get_all()
    
    async def get_product(self, product_id: int) -> Optional[Product]:
        return await self.product_repository.get_by_id(product_id)
    
    async def create_product(self, product: Product) -> Product:
        if not product.is_valid():
            raise ValueError("Invalid product data")
        
        product.created_at = datetime.utcnow()
        product.updated_at = product.created_at
        
        return await self.product_repository.create(product)
    
    async def update_product(self, product_id: int, product: Product) -> Optional[Product]:
        existing_product = await self.product_repository.get_by_id(product_id)
        if not existing_product:
            return None
        
        if not product.is_valid():
            raise ValueError("Invalid product data")
        
        product.id = product_id
        product.created_at = existing_product.created_at
        product.updated_at = datetime.utcnow()
        
        return await self.product_repository.update(product)
    
    async def delete_product(self, product_id: int) -> bool:
        return await self.product_repository.delete(product_id)


class UserServiceImpl(UserService):
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
    
    async def get_user(self, user_id: int) -> Optional[User]:
        return await self.user_repository.get_by_id(user_id)
    
    async def get_user_by_email(self, email: str) -> Optional[User]:
        return await self.user_repository.get_by_email(email)
    
    async def create_user(self, user: User) -> User:
        # Check if email or username already exists
        existing_email_user = await self.user_repository.get_by_email(user.email)
        existing_username_user = await self.user_repository.get_by_username(user.username)
        
        if existing_email_user:
            raise ValueError("Email already registered")
        
        if existing_username_user:
            raise ValueError("Username already taken")
        
        user.created_at = datetime.utcnow()
        user.updated_at = user.created_at
        
        return await self.user_repository.create(user)
    
    async def update_user(self, user_id: int, user: User) -> Optional[User]:
        existing_user = await self.user_repository.get_by_id(user_id)
        if not existing_user:
            return None
        
        user.id = user_id
        user.created_at = existing_user.created_at
        user.updated_at = datetime.utcnow()
        
        return await self.user_repository.update(user)
    
    async def delete_user(self, user_id: int) -> bool:
        return await self.user_repository.delete(user_id)