# app/api/v1/insurance.py
"""
Insurance claim endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database.session import get_db
from app.models.insurance import InsuranceClaim
from app.schemas.insurance import ClaimCreate, ClaimResponse
from app.services.insurance_service import process_insurance_claim

router = APIRouter(prefix="/insurance", tags=["Insurance"])

@router.post("/claim", response_model=ClaimResponse, status_code=201)
def file_claim(claim_data: ClaimCreate, db: Session = Depends(get_db)):
    """
    File insurance claim
    Uses satellite data + blockchain
    """
    # Process claim (includes blockchain)
    claim = process_insurance_claim(claim_data, db)
    
    return claim

@router.get("/claim/{claim_id}", response_model=ClaimResponse)
def get_claim(claim_id: str, db: Session = Depends(get_db)):
    """
    Get claim by ID
    """
    claim = db.query(InsuranceClaim).filter(InsuranceClaim.claim_id == claim_id).first()
    
    if not claim:
        raise HTTPException(404, "Claim not found")
    
    return claim

@router.get("/claims", response_model=List[ClaimResponse])
def list_claims(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    List all claims
    """
    claims = db.query(InsuranceClaim).offset(skip).limit(limit).all()
    return claims
