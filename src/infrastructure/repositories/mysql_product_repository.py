from typing import List, Optional
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.models import Product
from src.domain.ports.repositories import ProductRepository
from src.infrastructure.models.product_model import ProductModel


class MySQLProductRepository(ProductRepository):
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_all(self) -> List[Product]:
        query = select(ProductModel)
        result = await self.session.execute(query)
        product_models = result.scalars().all()
        
        return [
            Product(
                id=product.id,
                name=product.name,
                description=product.description,
                price=product.price,
                stock=product.stock,
                created_at=product.created_at,
                updated_at=product.updated_at
            )
            for product in product_models
        ]
    
    async def get_by_id(self, product_id: int) -> Optional[Product]:
        query = select(ProductModel).where(ProductModel.id == product_id)
        result = await self.session.execute(query)
        product_model = result.scalars().first()
        
        if not product_model:
            return None
        
        return Product(
            id=product_model.id,
            name=product_model.name,
            description=product_model.description,
            price=product_model.price,
            stock=product_model.stock,
            created_at=product_model.created_at,
            updated_at=product_model.updated_at
        )
    
    async def create(self, product: Product) -> Product:
        product_model = ProductModel(
            name=product.name,
            description=product.description,
            price=product.price,
            stock=product.stock,
            created_at=product.created_at,
            updated_at=product.updated_at
        )
        
        self.session.add(product_model)
        await self.session.flush()
        
        product.id = product_model.id
        return product
    
    async def update(self, product: Product) -> Product:
        query = select(ProductModel).where(ProductModel.id == product.id)
        result = await self.session.execute(query)
        product_model = result.scalars().first()
        
        if product_model:
            product_model.name = product.name
            product_model.description = product.description
            product_model.price = product.price
            product_model.stock = product.stock
            product_model.updated_at = product.updated_at
            
            await self.session.flush()
        
        return product
    
    async def delete(self, product_id: int) -> bool:
        query = delete(ProductModel).where(ProductModel.id == product_id)
        result = await self.session.execute(query)
        return result.rowcount > 0