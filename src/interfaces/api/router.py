from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
import bcrypt
from datetime import timedelta, datetime
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.database import get_db
from src.infrastructure.config import settings
from src.infrastructure.repositories.mysql_product_repository import MySQLProductRepository
from src.infrastructure.repositories.mysql_user_repository import MySQLUserRepository
from src.application.services import ProductServiceImpl, UserServiceImpl
from src.domain.models import Product, User
from src.interfaces.api.schemas import (
    ProductCreate, ProductUpdate, ProductResponse,
    UserCreate, UserUpdate, UserResponse,
    Token, TokenData
)

# OAuth2 scheme
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")


# Dependencies
async def get_product_service(db: AsyncSession = Depends(get_db)):
    repository = MySQLProductRepository(db)
    return ProductServiceImpl(repository)


async def get_user_service(db: AsyncSession = Depends(get_db)):
    repository = MySQLUserRepository(db)
    return UserServiceImpl(repository)

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.JWT_EXPIRATION_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt


def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


def get_password_hash(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    user_service: UserServiceImpl = Depends(get_user_service)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        token_data = TokenData(user_id=user_id)
    except JWTError:
        raise credentials_exception
    
    user = await user_service.get_user(user_id=token_data.user_id)
    if user is None:
        raise credentials_exception
    return user


# Product Endpoints
@router.get("/products", response_model=List[ProductResponse], tags=["Products"])
async def get_products(
    product_service: ProductServiceImpl = Depends(get_product_service)
):
    """Get all products"""
    products = await product_service.get_all_products()
    return products


@router.get("/products/{product_id}", response_model=ProductResponse, tags=["Products"])
async def get_product(
    product_id: int,
    product_service: ProductServiceImpl = Depends(get_product_service)
):
    """Get a product by ID"""
    product = await product_service.get_product(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.post("/products", response_model=ProductResponse, status_code=201, tags=["Products"])
async def create_product(
    product_data: ProductCreate,
    product_service: ProductServiceImpl = Depends(get_product_service),
    current_user: User = Depends(get_current_user)
):
    """Create a new product (requires authentication)"""
    try:
        product = Product(
            name=product_data.name,
            description=product_data.description,
            price=product_data.price,
            stock=product_data.stock
        )
        created_product = await product_service.create_product(product)
        return created_product
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/products/{product_id}", response_model=ProductResponse, tags=["Products"])
async def update_product(
    product_id: int,
    product_data: ProductUpdate,
    product_service: ProductServiceImpl = Depends(get_product_service),
    current_user: User = Depends(get_current_user)
):
    """Update a product (requires authentication)"""
    existing_product = await product_service.get_product(product_id)
    if not existing_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Update only the provided fields
    if product_data.name is not None:
        existing_product.name = product_data.name
    if product_data.description is not None:
        existing_product.description = product_data.description
    if product_data.price is not None:
        existing_product.price = product_data.price
    if product_data.stock is not None:
        existing_product.stock = product_data.stock
    
    try:
        updated_product = await product_service.update_product(product_id, existing_product)
        return updated_product
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/products/{product_id}", status_code=204, tags=["Products"])
async def delete_product(
    product_id: int,
    product_service: ProductServiceImpl = Depends(get_product_service),
    current_user: User = Depends(get_current_user)
):
    """Delete a product (requires authentication)"""
    result = await product_service.delete_product(product_id)
    if not result:
        raise HTTPException(status_code=404, detail="Product not found")


# User Endpoints
@router.post("/users", response_model=UserResponse, status_code=201, tags=["Users"])
async def create_user(
    user_data: UserCreate,
    user_service: UserServiceImpl = Depends(get_user_service)
):
    """Register a new user"""
    try:
        hashed_password = get_password_hash(user_data.password)
        user = User(
            username=user_data.username,
            email=user_data.email,
            hashed_password=hashed_password
        )
        created_user = await user_service.create_user(user)
        return created_user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login", response_model=Token, tags=["Authentication"])
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_service: UserServiceImpl = Depends(get_user_service)
):
    """Login to get access token"""
    user = await user_service.get_user_by_email(form_data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(
        data={"sub": str(user.id)}
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me", response_model=UserResponse, tags=["Users"])
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current user information (requires authentication)"""
    return current_user