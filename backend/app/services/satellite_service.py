# app/services/satellite_service.py
"""
Satellite data service (NDVI calculations)
For hackathon: Simulated data
For production: Real Copernicus API
"""
from datetime import datetime
import random
from app.config import settings

def get_ndvi_for_field(field_id: str, date: str = None) -> dict:
    """
    Get NDVI for field
    
    For hackathon: Returns simulated data
    For production: Would call Copernicus API
    """
    
    if settings.DEMO_MODE:
        # Simulated NDVI based on date
        if date:
            if "jan" in date.lower() or "feb" in date.lower():
                ndvi = random.uniform(0.75, 0.85)  # Healthy
                status = "Healthy"
            elif "mar" in date.lower():
                ndvi = random.uniform(0.65, 0.75)  # Good
                status = "Good"
            elif "apr" in date.lower():
                ndvi = random.uniform(0.40, 0.55)  # Stressed
                status = "Stressed"
            else:  # May onwards
                ndvi = random.uniform(0.25, 0.35)  # Damaged
                status = "Damaged"
        else:
            ndvi = random.uniform(0.5, 0.8)
            status = "Moderate"
        
        return {
            "field_id": field_id,
            "date": date or datetime.now().strftime("%Y-%m-%d"),
            "ndvi": round(ndvi, 2),
            "status": status,
            "source": "Sentinel-2 L2A (Simulated)",
            "resolution": "10m"
        }
    else:
        # TODO: Real Copernicus API integration
        # This is where you'd call actual satellite API
        pass


def get_ndvi_timeline(field_id: str, start_date: str, end_date: str) -> list:
    """
    Get NDVI timeline for field
    Returns list of NDVI readings over time
    """
    
    timeline = []
    
    # Simulated timeline (for demo)
    dates = [
        ("2024-01-15", 0.78, "Healthy"),
        ("2024-02-01", 0.82, "Peak"),
        ("2024-02-15", 0.79, "Healthy"),
        ("2024-03-01", 0.74, "Good"),
        ("2024-03-15", 0.68, "Moderate"),
        ("2024-04-01", 0.52, "Stressed"),
        ("2024-04-15", 0.42, "Stressed"),
        ("2024-05-01", 0.29, "Damaged")
    ]
    
    for date, ndvi, status in dates:
        timeline.append({
            "date": date,
            "ndvi": ndvi,
            "status": status
        })
    
    return timeline
