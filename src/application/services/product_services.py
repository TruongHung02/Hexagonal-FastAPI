from dataclasses import asdict
from datetime import datetime
import json
from typing import List, Optional
from src.domain.models import Product
from src.domain.ports.repositories import ProductRepository, CacheRepository
from src.domain.ports.services import ProductService

class ProductServiceImpl(ProductService):
    def __init__(self, product_repository: ProductRepository, cache: CacheRepository):
        self.product_repository = product_repository
        self.cache = cache
        self.cache_prefix = 'product'
        self.cache_ttl = 3600  # 1 hour

    
    async def get_all_products(self) -> List[Product]:
        return await self.product_repository.get_all()
    
    async def get_product(self, product_id: int) -> Optional[Product]:
        cache_key = f"{self.cache_prefix}:{product_id}"
        cached_product = await self.cache.get(cache_key)
        if cached_product:
            product_data = json.loads(cached_product)
            return Product(**product_data)
        

        product = await self.product_repository.get_by_id(product_id)
        
        # Lưu vào cache nếu tìm thấy
        if product:
            product_dict = asdict(product)
            await self.cache.set(cache_key, json.dumps(product_dict, default=str), self.cache_ttl)
        return product
    
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


