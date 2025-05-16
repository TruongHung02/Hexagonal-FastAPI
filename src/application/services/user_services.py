from datetime import datetime
from typing import Optional
from src.domain.models import User
from src.domain.ports.repositories import UserRepository
from src.domain.ports.services import UserService


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