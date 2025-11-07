# app/models/insurance.py
"""
Insurance claim database model
"""
from sqlalchemy import Column, String, Float, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.session import Base

class InsuranceClaim(Base):
    __tablename__ = "insurance_claims"
    
    claim_id = Column(String, primary_key=True, index=True)
    field_id = Column(String, ForeignKey("fields.field_id"))
    
    # Damage details
    damage_type = Column(String)  # drought, flood, pest, hailstorm
    pre_ndvi = Column(Float)
    post_ndvi = Column(Float)
    damage_percent = Column(Float)
    
    # Decision
    status = Column(String)  # APPROVED, REJECTED, PENDING
    payout = Column(Integer, default=0)
    
    # Blockchain
    blockchain_tx = Column(String)
    block_number = Column(Integer)
    
    # Relationships
    field = relationship("Field", back_populates="claims")
    
    # Metadata
    filed_at = Column(DateTime, default=datetime.utcnow)
    processed_at = Column(DateTime)
    
    def __repr__(self):
        return f"<Claim {self.claim_id}: {self.status}>"
