# app/api/v1/farmers.py
"""
Farmer endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database.session import get_db
from app.models.farmer import Farmer
from app.schemas.farmer import FarmerCreate, FarmerResponse

router = APIRouter(prefix="/farmers", tags=["Farmers"])

@router.post("/register", response_model=FarmerResponse, status_code=201)
def register_farmer(farmer_data: FarmerCreate, db: Session = Depends(get_db)):
    """
    Register new farmer
    """
    # Check if phone already exists
    existing = db.query(Farmer).filter(Farmer.phone == farmer_data.phone).first()
    if existing:
        raise HTTPException(400, "Phone number already registered")
    
    # Generate farmer ID
    count = db.query(Farmer).count()
    farmer_id = f"FAR-{count + 1:04d}"
    
    # Create farmer
    farmer = Farmer(
        farmer_id=farmer_id,
        **farmer_data.dict()
    )
    
    db.add(farmer)
    db.commit()
    db.refresh(farmer)
    
    return farmer

@router.get("/{farmer_id}", response_model=FarmerResponse)
def get_farmer(farmer_id: str, db: Session = Depends(get_db)):
    """
    Get farmer by ID
    """
    farmer = db.query(Farmer).filter(Farmer.farmer_id == farmer_id).first()
    
    if not farmer:
        raise HTTPException(404, "Farmer not found")
    
    return farmer

@router.get("/", response_model=List[FarmerResponse])
def list_farmers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    List all farmers
    """
    farmers = db.query(Farmer).offset(skip).limit(limit).all()
    return farmers
