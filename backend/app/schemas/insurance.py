from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class ClaimCreate(BaseModel):
    field_id: str
    damage_type: str = Field(..., pattern="^(drought|flood|pest|hailstorm)$")  # ← pattern
    pre_ndvi: float = Field(..., ge=0, le=1)
    post_ndvi: float = Field(..., ge=0, le=1)

class ClaimResponse(BaseModel):
    claim_id: str
    field_id: str
    damage_type: str
    pre_ndvi: float
    post_ndvi: float
    damage_percent: float
    status: str
    payout: int
    blockchain_tx: str
    block_number: int
    filed_at: datetime
    
    class Config:
        from_attributes = True
