# GreenChain Farmer Authentication System - Land Document OCR
# Integrates with GreenChain Payment Section

import cv2
import numpy as np
from PIL import Image
import pytesseract
import re
from typing import Dict, Optional
from datetime import datetime
import json


class FarmerAuthentication:
    """
    Authenticates farmers by scanning Indian land documents (Patta, 7/12, etc.)
    Extracts: Name, District, Survey Number, Land Area, Village
    Returns dictionary compatible with payment system
    """
    
    def __init__(self):
        # Configure Tesseract for Indian documents
        self.tesseract_config = r'--oem 3 --psm 6'
        
        # Common field patterns in Indian land documents
        self.patterns = {
            'name': [
                r'(?:Name|Owner|Holder|नाम)[\s:]+([A-Za-z\s\.]+)',
                r'(?:Farmer|Cultivator)[\s:]+([A-Za-z\s\.]+)',
                r'(?:श्री|श्रीमती|Shri|Smt\.)[\s]*([A-Za-z\s\.]+)'
            ],
            'district': [
                r'(?:District|Taluk|जिला)[\s:]+([A-Za-z\s]+)',
                r'(?:Revenue|Sub-Division)[\s:]+([A-Za-z\s]+)'
            ],
            'survey_number': [
                r'(?:Survey|S\.No\.|Sy\.No\.|खसरा)[\s:]+([0-9/\-A-Z]+)',
                r'(?:Plot|Khasra|Khata)[\s:]+([0-9/\-A-Z]+)'
            ],
            'land_area': [
                r'(?:Area|Extent|क्षेत्रफल)[\s:]+([0-9\.]+)\s*(?:Acres?|Hectares?|Ha|एकड़)',
                r'([0-9\.]+)\s*(?:Acres?|Hectares?|Ha)'
            ],
            'village': [
                r'(?:Village|Gram|गाँव)[\s:]+([A-Za-z\s]+)',
            ]
        }
    
    def preprocess_image(self, image_path: str) -> np.ndarray:
        """Preprocess land document image for better OCR accuracy"""
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Could not read image: {image_path}")
        
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        binary = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                       cv2.THRESH_BINARY, 11, 2)
        denoised = cv2.fastNlMeansDenoising(binary, None, 10, 7, 21)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        enhanced = clahe.apply(denoised)
        
        return enhanced
    
    def extract_text_from_image(self, image_path: str) -> str:
        """Extract text from preprocessed image using OCR"""
        try:
            processed_img = self.preprocess_image(image_path)
            pil_img = Image.fromarray(processed_img)
            text = pytesseract.image_to_string(pil_img, config=self.tesseract_config)
            return text
        except Exception as e:
            print(f"OCR Error: {e}")
            return ""
    
    def extract_field(self, text: str, field_name: str) -> Optional[str]:
        """Extract specific field from OCR text using regex patterns"""
        if field_name not in self.patterns:
            return None
        
        for pattern in self.patterns[field_name]:
            match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
            if match:
                value = match.group(1).strip()
                value = re.sub(r'\s+', ' ', value)
                return value
        
        return None
    
    def validate_survey_number(self, survey_no: str) -> bool:
        """Validate survey number format (common Indian formats)"""
        if not survey_no:
            return False
        pattern = r'^[0-9]+(?:[/-][0-9A-Z]+)*$'
        return bool(re.match(pattern, survey_no))
    
    def validate_land_area(self, area: str) -> float:
        """Convert and validate land area to hectares"""
        if not area:
            return 0.0
        try:
            area_value = float(re.search(r'[0-9\.]+', area).group())
            if 'acre' in area.lower():
                area_value = area_value * 0.404686
            return round(area_value, 2)
        except:
            return 0.0
    
    def farmer_authentic(self, image_path: str, farmer_id: Optional[str] = None) -> Dict:
        """
        Main authentication function - scans land document and returns farmer details
        
        Parameters:
        - image_path: Path to land document image
        - farmer_id: Optional farmer ID (auto-generated if not provided)
        
        Returns:
        - Dictionary with farmer details compatible with payment system
        """
        print(f"\n{'='*70}")
        print("FARMER AUTHENTICATION - LAND DOCUMENT SCAN")
        print(f"{'='*70}\n")
        
        result = {
            'authentication_status': 'PENDING',
            'farmer_details': {},
            'land_details': {},
            'extracted_fields': {},
            'verification': {}
        }
        
        try:
            # Step 1: Extract text from image
            print("Step 1: Extracting text from land document...")
            ocr_text = self.extract_text_from_image(image_path)
            
            if not ocr_text:
                result['authentication_status'] = 'FAILED'
                result['verification']['error'] = 'Could not extract text from image'
                return result
            
            print(f"  ✓ Text extracted ({len(ocr_text)} characters)\n")
            
            # Step 2: Extract fields
            print("Step 2: Extracting farmer and land details...")
            
            name = self.extract_field(ocr_text, 'name')
            district = self.extract_field(ocr_text, 'district')
            survey_number = self.extract_field(ocr_text, 'survey_number')
            land_area = self.extract_field(ocr_text, 'land_area')
            village = self.extract_field(ocr_text, 'village')
            
            result['extracted_fields'] = {
                'name': name,
                'district': district,
                'survey_number': survey_number,
                'land_area_raw': land_area,
                'village': village,
                'ocr_text_preview': ocr_text[:200] + "..." if len(ocr_text) > 200 else ocr_text
            }
            
            print(f"  Name: {name}")
            print(f"  District: {district}")
            print(f"  Survey Number: {survey_number}")
            print(f"  Land Area: {land_area}")
            print(f"  Village: {village}")
            print(f"  ✓ Fields extracted\n")
            
            # Step 3: Validate extracted data
            print("Step 3: Validating extracted data...")
            
            validation_results = {
                'name_valid': bool(name and len(name) > 2),
                'district_valid': bool(district and len(district) > 2),
                'survey_number_valid': self.validate_survey_number(survey_number),
                'land_area_valid': bool(land_area)
            }
            
            all_valid = all(validation_results.values())
            
            for field, valid in validation_results.items():
                status = "✓" if valid else "✗"
                print(f"  {status} {field}: {valid}")
            
            result['verification'] = {
                'validation_results': validation_results,
                'all_fields_valid': all_valid,
                'confidence_score': sum(validation_results.values()) / len(validation_results) * 100,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            print(f"\n  Confidence Score: {result['verification']['confidence_score']:.1f}%\n")
            
            # Step 4: Generate farmer ID if not provided
            if not farmer_id:
                district_code = (district[:3].upper() if district else "UNK")
                timestamp_code = datetime.now().strftime('%m%d%H%M')
                farmer_id = f"FRM{district_code}{timestamp_code}"
            
            # Step 5: Prepare farmer details (compatible with payment system)
            land_area_hectares = self.validate_land_area(land_area) if land_area else 0.0
            
            result['farmer_details'] = {
                'farmer_id': farmer_id,
                'name': name if name else 'Unknown',
                'phone': '+91-0000000000',
                'land_area_hectares': land_area_hectares,
                'district': district if district else 'Unknown',
                'crop_type': 'To be specified',
                'verified_harvests': 0
            }
            
            result['land_details'] = {
                'survey_number': survey_number if survey_number else 'Unknown',
                'village': village if village else 'Unknown',
                'land_area_hectares': land_area_hectares,
                'land_area_raw': land_area,
                'document_verified': all_valid
            }
            
            # Step 6: Set authentication status
            if all_valid:
                result['authentication_status'] = 'VERIFIED'
                print(f"Step 4: Authentication Status: ✓ VERIFIED\n")
            elif sum(validation_results.values()) >= 2:
                result['authentication_status'] = 'PARTIAL'
                print(f"Step 4: Authentication Status: ⚠ PARTIAL (Manual review required)\n")
            else:
                result['authentication_status'] = 'FAILED'
                print(f"Step 4: Authentication Status: ✗ FAILED\n")
            
            print(f"{'='*70}")
            print(f"AUTHENTICATION COMPLETE - Status: {result['authentication_status']}")
            print(f"{'='*70}\n")
            
        except Exception as e:
            result['authentication_status'] = 'ERROR'
            result['verification']['error'] = str(e)
            print(f"Error during authentication: {e}")
        
        return result


# Mock function for testing without actual images
def mock_farmer_authentic(sample_data: Dict) -> Dict:
    """Simulates farmer_authentic() for testing without images"""
    farmer_id = sample_data.get('farmer_id', f"FRM{datetime.now().strftime('%m%d%H%M')}")
    
    result = {
        'authentication_status': 'VERIFIED',
        'farmer_details': {
            'farmer_id': farmer_id,
            'name': sample_data.get('name', 'Rajesh Kumar'),
            'phone': sample_data.get('phone', '+91-9876543210'),
            'land_area_hectares': sample_data.get('land_area_hectares', 2.5),
            'district': sample_data.get('district', 'Mysuru'),
            'crop_type': sample_data.get('crop_type', 'Rice'),
            'verified_harvests': sample_data.get('verified_harvests', 6)
        },
        'land_details': {
            'survey_number': sample_data.get('survey_number', '123/4-A'),
            'village': sample_data.get('village', 'Kanakapura'),
            'land_area_hectares': sample_data.get('land_area_hectares', 2.5),
            'land_area_raw': f"{sample_data.get('land_area_hectares', 2.5)} Hectares",
            'document_verified': True
        },
        'extracted_fields': {
            'name': sample_data.get('name'),
            'district': sample_data.get('district'),
            'survey_number': sample_data.get('survey_number'),
            'land_area_raw': f"{sample_data.get('land_area_hectares', 2.5)} Hectares",
            'village': sample_data.get('village'),
            'ocr_text_preview': 'Mock land document data...'
        },
        'verification': {
            'validation_results': {
                'name_valid': True,
                'district_valid': True,
                'survey_number_valid': True,
                'land_area_valid': True
            },
            'all_fields_valid': True,
            'confidence_score': 100.0,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    }
    
    return result


# Example usage
if __name__ == "__main__":
    # Using actual image (requires opencv, tesseract)
    # auth = FarmerAuthentication()
    # result = auth.farmer_authentic('land_document.jpg')
    
    # Using mock for testing
    sample_data = {
        'name': 'Ramesh Patil',
        'district': 'Tumkur',
        'survey_number': '789/12-C',
        'land_area_hectares': 3.2,
        'village': 'Huliyar',
        'phone': '+91-9988776655',
        'crop_type': 'Cotton'
    }
    
    result = mock_farmer_authentic(sample_data)
    print(json.dumps(result, indent=2))
