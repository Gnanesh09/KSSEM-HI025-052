# app/models/field.py
"""
Field database model
"""
from sqlalchemy import Column, String, Float, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.session import Base

class Field(Base):
    __tablename__ = "fields"
    
    field_id = Column(String, primary_key=True, index=True)
    farmer_id = Column(String, ForeignKey("farmers.farmer_id"))
    
    # Field details
    size_acres = Column(Float, nullable=False)
    crop = Column(String, nullable=False)
    location = Column(String)
    
    # GPS coordinates
    gps_latitude = Column(Float)
    gps_longitude = Column(Float)
    
    # Survey number (government land record)
    survey_number = Column(String)
    
    # Current NDVI
    latest_ndvi = Column(Float, default=0.0)
    latest_ndvi_date = Column(DateTime)
    
    # Relationships
    farmer = relationship("Farmer", back_populates="fields")
    claims = relationship("InsuranceClaim", back_populates="field")
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Field {self.field_id}: {self.crop}>"
