# app/api/v1/__init__.py
"""
API v1 router
Combines all endpoint routers
"""
from fastapi import APIRouter
from app.api.v1 import farmers, fields, insurance

api_router = APIRouter()

# Include all routers
api_router.include_router(farmers.router)
api_router.include_router(fields.router)
api_router.include_router(insurance.router)
