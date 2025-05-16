from typing import List, Optional
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.models import User
from src.domain.ports.repositories import UserRepository
from src.infrastructure.models.user_model import UserModel


class MySQLUserRepository(UserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_by_id(self, user_id: int) -> Optional[User]:
        query = select(UserModel).where(UserModel.id == user_id)
        result = await self.session.execute(query)
        user_model = result.scalars().first()
        
        if not user_model:
            return None
        
        return User(
            id=user_model.id,
            username=user_model.username,
            email=user_model.email,
            hashed_password=user_model.hashed_password,
            created_at=user_model.created_at,
            updated_at=user_model.updated_at
        )
    
    async def get_by_email(self, email: str) -> Optional[User]:
        query = select(UserModel).where(UserModel.email == email)
        result = await self.session.execute(query)
        user_model = result.scalars().first()
        
        if not user_model:
            return None
        
        return User(
            id=user_model.id,
            username=user_model.username,
            email=user_model.email,
            hashed_password=user_model.hashed_password,
            created_at=user_model.created_at,
            updated_at=user_model.updated_at
        )
    
    async def get_by_username(self, username: str) -> Optional[User]:
        query = select(UserModel).where(UserModel.username == username)
        result = await self.session.execute(query)
        user_model = result.scalars().first()
        
        if not user_model:
            return None
        
        return User(
            id=user_model.id,
            username=user_model.username,
            email=user_model.email,
            hashed_password=user_model.hashed_password,
            created_at=user_model.created_at,
            updated_at=user_model.updated_at
        )
    
    async def create(self, user: User) -> User:
        user_model = UserModel(
            username=user.username,
            email=user.email,
            hashed_password=user.hashed_password,
            created_at=user.created_at,
            updated_at=user.updated_at
        )
        
        self.session.add(user_model)
        await self.session.flush()
        
        user.id = user_model.id
        return user
    
    async def update(self, user: User) -> User:
        query = select(UserModel).where(UserModel.id == user.id)
        result = await self.session.execute(query)
        user_model = result.scalars().first()
        
        if user_model:
            user_model.username = user.username
            user_model.email = user.email
            if user.hashed_password:
                user_model.hashed_password = user.hashed_password
            user_model.updated_at = user.updated_at
            
            await self.session.flush()
        
        return user
    
    async def delete(self, user_id: int) -> bool:
        query = delete(UserModel).where(UserModel.id == user_id)
        result = await self.session.execute(query)
        return result.rowcount > 0
