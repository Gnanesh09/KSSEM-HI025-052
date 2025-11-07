# app/api/v1/satellite.py
"""
Satellite data endpoints
"""
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import Optional
from app.database.session import get_db
from app.models.fields import Field
from app.services.satellite_service import get_ndvi_for_field, sentinel_service

router = APIRouter(prefix="/satellite", tags=["Satellite"])

@router.get("/ndvi/{field_id}")
def get_field_ndvi(
    field_id: str,
    date: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Get NDVI for field using real Sentinel-2 data
    
    Args:
        field_id: Field identifier
        date: Date (YYYY-MM-DD), defaults to today
    """
    # Get field from database
    field = db.query(Field).filter(Field.field_id == field_id).first()
    
    if not field:
        raise HTTPException(404, "Field not found")
    
    if not field.gps_latitude or not field.gps_longitude:
        raise HTTPException(400, "Field has no GPS coordinates")
    
    # Fetch NDVI from satellite
    ndvi_data = get_ndvi_for_field(
        field_id=field_id,
        latitude=field.gps_latitude,
        longitude=field.gps_longitude,
        date=date
    )
    
    # Update field's latest NDVI
    field.latest_ndvi = ndvi_data['ndvi']
    db.commit()
    
    return ndvi_data

@router.get("/timeline/{field_id}")
def get_field_timeline(
    field_id: str,
    start_date: str,
    end_date: str,
    db: Session = Depends(get_db)
):
    """
    Get NDVI timeline for field
    
    Args:
        field_id: Field identifier
        start_date: Start date (YYYY-MM-DD)
        end_date: End date (YYYY-MM-DD)
    """
    # Get field
    field = db.query(Field).filter(Field.field_id == field_id).first()
    
    if not field:
        raise HTTPException(404, "Field not found")
    
    if not field.gps_latitude or not field.gps_longitude:
        raise HTTPException(400, "Field has no GPS coordinates")
    
    # Get timeline
    timeline = sentinel_service.get_ndvi_timeline(
        latitude=field.gps_latitude,
        longitude=field.gps_longitude,
        start_date=start_date,
        end_date=end_date
    )
    
    return {
        "field_id": field_id,
        "crop": field.crop,
        "location": field.location,
        "timeline": timeline
    }

@router.get("/image/{field_id}")
def get_field_image(
    field_id: str,
    date: str,
    db: Session = Depends(get_db)
):
    """
    Get satellite image for field
    Returns image file path
    """
    # Get field
    field = db.query(Field).filter(Field.field_id == field_id).first()
    
    if not field:
        raise HTTPException(404, "Field not found")
    
    # Fetch NDVI (which also downloads image)
    ndvi_data = get_ndvi_for_field(
        field_id=field_id,
        latitude=field.gps_latitude,
        longitude=field.gps_longitude,
        date=date
    )
    
    if ndvi_data.get('image'):
        return {
            "field_id": field_id,
            "date": date,
            "image_path": ndvi_data['image'],
            "ndvi": ndvi_data['ndvi']
        }
    else:
        raise HTTPException(404, "Image not available")
