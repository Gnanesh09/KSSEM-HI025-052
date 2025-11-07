# app/models/farmer.py
"""
Farmer database model
"""
from sqlalchemy import Column, String, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.session import Base

class Farmer(Base):
    __tablename__ = "farmers"
    
    farmer_id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    phone = Column(String, unique=True, nullable=False)
    location = Column(String)
    village = Column(String)
    district = Column(String)
    state = Column(String, default="Karnataka")
    
    # Relationships
    fields = relationship("Field", back_populates="farmer")
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Farmer {self.farmer_id}: {self.name}>"
