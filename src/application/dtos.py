from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class ProductDTO:
    id: Optional[int] = None
    name: str = ""
    description: str = ""
    price: float = 0.0
    stock: int = 0
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass
class UserDTO:
    id: Optional[int] = None
    username: str = ""
    email: str = ""
    password: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None