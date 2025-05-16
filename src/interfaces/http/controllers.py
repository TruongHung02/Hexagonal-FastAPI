from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from src.interfaces.api.router import router as api_router


controller_router = APIRouter()

# Mount API routes
controller_router.include_router(api_router, prefix="/api")


@controller_router.get("/health")
async def health_check():
    """Health check endpoint"""
    return JSONResponse(content={"status": "ok"})