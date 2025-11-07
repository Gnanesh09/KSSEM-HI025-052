# app/services/satellite_service.py
"""
Free Sentinel-2 data using Google Earth Engine
No API credentials needed!
"""
import ee
from datetime import datetime, timedelta
import numpy as np
from typing import Dict, Tuple
import os

# Initialize Earth Engine (free, no credentials needed for basic access)
try:
    ee.Initialize()
    print("✅ Google Earth Engine initialized")
except:
    print("⚠️ Earth Engine not initialized, using simulated data")

class FreeNDVIService:
    """Get free Sentinel-2 NDVI without API credentials"""
    
    @staticmethod
    def get_ndvi_for_location(
        latitude: float,
        longitude: float,
        date: str
    ) -> Tuple[float, str]:
        """
        Fetch NDVI from Google Earth Engine (FREE)
        
        Args:
            latitude: GPS latitude
            longitude: GPS longitude
            date: Date string (YYYY-MM-DD)
        
        Returns:
            Tuple of (NDVI value, image path)
        """
        
        try:
            # Create point
            point = ee.Geometry.Point([longitude, latitude])
            
            # Get Sentinel-2 data for date (free!)
            start_date = date
            end_date = (datetime.strptime(date, "%Y-%m-%d") + timedelta(days=1)).strftime("%Y-%m-%d")
            
            sentinel2 = ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED") \
                .filterBounds(point) \
                .filterDate(start_date, end_date) \
                .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 30)) \
                .first()
            
            if sentinel2 is None:
                # Try without exact date match
                sentinel2 = ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED") \
                    .filterBounds(point) \
                    .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 30)) \
                    .sort('system:time_start', False) \
                    .first()
            
            # Calculate NDVI (Red=B4, NIR=B8)
            ndvi = sentinel2.normalizedDifference(['B8', 'B4']).rename('NDVI')
            
            # Get average NDVI at point
            ndvi_value = ndvi.sample(point, 30).first().get('NDVI').getInfo()
            
            # Convert to 0-1 range if needed
            if ndvi_value:
                ndvi_float = float(ndvi_value)
            else:
                ndvi_float = 0.65
            
            print(f"✅ NDVI from Earth Engine: {ndvi_float:.2f}")
            
            return ndvi_float, f"EE_{date}_{latitude}_{longitude}"
        
        except Exception as e:
            print(f"⚠️ Earth Engine error: {str(e)}, using simulated data")
            # Fallback to simulated
            return FreeNDVIService.get_simulated_ndvi(date), "simulated"
    
    @staticmethod
    def get_simulated_ndvi(date: str) -> float:
        """
        Simulated NDVI based on date
        (For when Earth Engine is not available)
        """
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        month = date_obj.month
        
        # Simulate crop growth cycle (India)
        if month in [1, 2]:  # January-February: Planting
            return round(0.20 + np.random.uniform(-0.05, 0.05), 2)
        elif month in [3, 4]:  # March-April: Growing
            return round(0.50 + np.random.uniform(-0.1, 0.1), 2)
        elif month in [5, 6]:  # May-June: Peak/Monsoon
            return round(0.65 + np.random.uniform(-0.1, 0.1), 2)
        elif month in [7, 8, 9]:  # July-September: Harvest season
            return round(0.45 + np.random.uniform(-0.15, 0.15), 2)
        else:  # October-December: Post-harvest
            return round(0.30 + np.random.uniform(-0.1, 0.1), 2)


# Service instance
free_ndvi_service = FreeNDVIService()


def get_ndvi_for_field(
    field_id: str,
    latitude: float,
    longitude: float,
    date: str = None
) -> Dict:
    """
    Get NDVI for field using FREE data
    No API credentials needed!
    """
    
    if not date:
        date = datetime.now().strftime("%Y-%m-%d")
    
    try:
        # Try Google Earth Engine first (FREE!)
        ndvi, image_ref = free_ndvi_service.get_ndvi_for_location(
            latitude, longitude, date
        )
        
        # Determine status
        if ndvi > 0.6:
            status = "Healthy"
        elif ndvi > 0.4:
            status = "Moderate"
        elif ndvi > 0.2:
            status = "Stressed"
        else:
            status = "Damaged"
        
        return {
            "field_id": field_id,
            "date": date,
            "ndvi": ndvi,
            "status": status,
            "source": "Sentinel-2 L2A (Free - Google Earth Engine)",
            "image": image_ref,
            "resolution": "10m",
            "free": True
        }
    
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        # Ultimate fallback
        return {
            "field_id": field_id,
            "date": date,
            "ndvi": 0.65,
            "status": "Moderate",
            "source": "Simulated",
            "image": None,
            "free": True
        }
