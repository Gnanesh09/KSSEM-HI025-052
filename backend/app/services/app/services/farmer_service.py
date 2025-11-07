# app/services/farmer_service.py
"""
Farmer-related business logic
"""
from sqlalchemy.orm import Session
from app.models.farmer import Farmer
from app.models.fields import Field
from typing import Dict

def get_farmer_dashboard(farmer_id: str, db: Session) -> Dict:
    """
    Get complete farmer dashboard data
    """
    farmer = db.query(Farmer).filter(Farmer.farmer_id == farmer_id).first()
    
    if not farmer:
        return None
    
    fields = db.query(Field).filter(Field.farmer_id == farmer_id).all()
    
    # Calculate stats
    total_acres = sum(f.size_acres for f in fields)
    total_claims = sum(len(f.claims) for f in fields)
    approved_claims = sum(
        len([c for c in f.claims if c.status == "APPROVED"]) 
        for f in fields
    )
    total_payouts = sum(
        sum(c.payout for c in f.claims if c.status == "APPROVED")
        for f in fields
    )
    
    return {
        "farmer": {
            "farmer_id": farmer.farmer_id,
            "name": farmer.name,
            "phone": farmer.phone,
            "location": farmer.location
        },
        "stats": {
            "total_fields": len(fields),
            "total_acres": total_acres,
            "total_claims": total_claims,
            "approved_claims": approved_claims,
            "total_payouts": total_payouts
        },
        "fields": [
            {
                "field_id": f.field_id,
                "crop": f.crop,
                "size_acres": f.size_acres,
                "latest_ndvi": f.latest_ndvi
            }
            for f in fields
        ]
    }
