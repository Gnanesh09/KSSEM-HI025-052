from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class FieldCreate(BaseModel):
    farmer_id: str
    size_acres: float = Field(..., gt=0, lt=1000)
    crop: str
    location: str
    gps_latitude: Optional[float] = Field(None, ge=-90, le=90)
    gps_longitude: Optional[float] = Field(None, ge=-180, le=180)
    survey_number: Optional[str] = None

class FieldResponse(BaseModel):
    field_id: str
    farmer_id: str
    size_acres: float
    crop: str
    location: str
    gps_latitude: Optional[float]
    gps_longitude: Optional[float]
    latest_ndvi: float
    created_at: datetime
    
    class Config:
        from_attributes = True
