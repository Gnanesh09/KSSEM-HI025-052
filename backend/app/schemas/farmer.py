from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class FarmerCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    phone: str = Field(..., pattern=r"^\+?91[-\s]?\d{10}$")  # ← pattern
    location: str
    village: Optional[str] = None
    district: Optional[str] = "Ramanagara"
    state: Optional[str] = "Karnataka"

class FarmerResponse(BaseModel):
    farmer_id: str
    name: str
    phone: str
    location: str
    village: Optional[str]
    district: Optional[str]
    state: str
    created_at: datetime
    
    class Config:
        from_attributes = True
