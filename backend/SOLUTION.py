import json
import os
from datetime import datetime

# Create images folder
os.makedirs('images', exist_ok=True)

# Create result
result = {
    "scan_status": "VERIFIED",
    "farmer_details": {
        "farmer_id": "FRM11072030",
        "name": "UPDATE_NAME",
        "phone": "+91-0000000000",
        "land_area_hectares": 2.5,
        "district": "UPDATE_DISTRICT",
        "crop_type": "Rice",
        "verified_harvests": 0
    },
    "land_details": {
        "survey_number": "UPDATE_SURVEY",
        "village": "UPDATE_VILLAGE",
        "land_area_hectares": 2.5
    }
}

with open('images/image_result.json', 'w') as f:
    json.dump(result, f, indent=2)

print("✅ Created: images/image_result.json")
