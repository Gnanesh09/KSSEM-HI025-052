# app/api/v1/__init__.py
from fastapi import APIRouter
from app.api.v1 import farmers, fields, insurance, satellite  # ← Add satellite

api_router = APIRouter()

api_router.include_router(farmers.router)
api_router.include_router(fields.router)
api_router.include_router(insurance.router)
# api_router.include_router(satellite.router)  # ← Add this line
