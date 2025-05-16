import uvicorn
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException

from src.infrastructure.database import init_db
from src.interfaces.http.controllers import controller_router
from src.interfaces.http.error_handlers import (
    validation_exception_handler,
    http_exception_handler_wrapper,
    generic_exception_handler
)

# Create FastAPI application
app = FastAPI(
    title="FastAPI Hexagonal Architecture Demo",
    description="A demo application using FastAPI with Hexagonal Architecture and MySQL",
    version="0.1.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this to specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register exception handlers
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(StarletteHTTPException, http_exception_handler_wrapper)
app.add_exception_handler(Exception, generic_exception_handler)

# Add controller router
app.include_router(controller_router)


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    await init_db()


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to FastAPI Hexagonal Architecture Demo",
        "documentation": "/docs"
    }


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)