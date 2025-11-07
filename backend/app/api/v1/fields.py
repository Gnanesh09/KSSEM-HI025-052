# app/api/v1/fields.py
"""
Field endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database.session import get_db
from app.models.fields import Field
from app.schemas.field import FieldCreate, FieldResponse

router = APIRouter(prefix="/fields", tags=["Fields"])

@router.post("/register", response_model=FieldResponse, status_code=201)
def register_field(field_data: FieldCreate, db: Session = Depends(get_db)):
    """
    Register new field
    """
    # Generate field ID
    count = db.query(Field).count()
    field_id = f"FLD-{count + 1:03d}"
    
    # Create field
    field = Field(
        field_id=field_id,
        **field_data.dict()
    )
    
    db.add(field)
    db.commit()
    db.refresh(field)
    
    return field

@router.get("/{field_id}", response_model=FieldResponse)
def get_field(field_id: str, db: Session = Depends(get_db)):
    """
    Get field by ID
    """
    field = db.query(Field).filter(Field.field_id == field_id).first()
    
    if not field:
        raise HTTPException(404, "Field not found")
    
    return field

@router.get("/farmer/{farmer_id}", response_model=List[FieldResponse])
def get_farmer_fields(farmer_id: str, db: Session = Depends(get_db)):
    """
    Get all fields for a farmer
    """
    fields = db.query(Field).filter(Field.farmer_id == farmer_id).all()
    return fields
