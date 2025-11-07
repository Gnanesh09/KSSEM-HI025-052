# app/services/insurance_service.py
"""
Insurance claim processing logic
"""
from sqlalchemy.orm import Session
from app.models.insurance import InsuranceClaim
from app.schemas.insurance import ClaimCreate
from app.blockchain.blockchain import record_insurance_claim
from datetime import datetime

def process_insurance_claim(claim_data: ClaimCreate, db: Session) -> InsuranceClaim:
    """
    Process insurance claim
    1. Calculate damage
    2. Make decision
    3. Record on blockchain
    4. Save to database
    """
    
    # Calculate damage percentage
    damage_percent = (
        (claim_data.pre_ndvi - claim_data.post_ndvi) / claim_data.pre_ndvi
    ) * 100
    
    # Auto-decision (>50% = approved)
    approved = damage_percent > 50
    status = "APPROVED" if approved else "REJECTED"
    
    # Calculate payout
    # Formula: damage_percent * 1000 (₹1000 per % damage)
    payout = int(damage_percent * 1000) if approved else 0
    
    # Generate claim ID
    count = db.query(InsuranceClaim).count()
    claim_id = f"CLM-{count + 1:04d}"
    
    # Record on blockchain
    blockchain_tx, block_number = record_insurance_claim({
        "claim_id": claim_id,
        "field_id": claim_data.field_id,
        "damage_type": claim_data.damage_type,
        "pre_ndvi": claim_data.pre_ndvi,
        "post_ndvi": claim_data.post_ndvi,
        "damage_percent": round(damage_percent, 2),
        "status": status,
        "payout": payout
    })
    
    # Create database record
    claim = InsuranceClaim(
        claim_id=claim_id,
        field_id=claim_data.field_id,
        damage_type=claim_data.damage_type,
        pre_ndvi=claim_data.pre_ndvi,
        post_ndvi=claim_data.post_ndvi,
        damage_percent=round(damage_percent, 2),
        status=status,
        payout=payout,
        blockchain_tx=blockchain_tx,
        block_number=block_number,
        processed_at=datetime.utcnow()
    )
    
    db.add(claim)
    db.commit()
    db.refresh(claim)
    
    print(f"✅ Claim {claim_id} processed: {status} - ₹{payout:,}")
    
    return claim
