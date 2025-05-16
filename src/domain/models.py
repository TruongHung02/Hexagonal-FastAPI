from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Product:
    id: Optional[int] = None
    name: str = ""
    description: str = ""
    price: float = 0.0
    stock: int = 0
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def is_in_stock(self) -> bool:
        return self.stock > 0
    
    def is_valid(self) -> bool:
        return (
            self.name and
            self.price > 0 and
            self.stock >= 0
        )


@dataclass
class User:
    id: Optional[int] = None
    username: str = ""
    email: str = ""
    hashed_password: str = ""
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None