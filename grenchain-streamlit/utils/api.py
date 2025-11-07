import requests
import streamlit as st
from typing import Dict, List, Any

API_URL = "http://localhost:8000"
API_BASE = "/api/v1"

class APIClient:
    def __init__(self):
        self.base_url = f"{API_URL}{API_BASE}"
        self.headers = {"Content-Type": "application/json"}
    
    def register_farmer(self, data: Dict) -> Dict:
        response = requests.post(f"{self.base_url}/farmers/register", json=data, headers=self.headers)
        return response.json()
    
    def get_farmer(self, farmer_id: str) -> Dict:
        response = requests.get(f"{self.base_url}/farmers/{farmer_id}", headers=self.headers)
        return response.json()
    
    def list_farmers(self) -> List[Dict]:
        response = requests.get(f"{self.base_url}/farmers/", headers=self.headers)
        return response.json()
    
    def register_field(self, data: Dict) -> Dict:
        response = requests.post(f"{self.base_url}/fields/register", json=data, headers=self.headers)
        return response.json()
    
    def get_field(self, field_id: str) -> Dict:
        response = requests.get(f"{self.base_url}/fields/{field_id}", headers=self.headers)
        return response.json()
    
    def get_farmer_fields(self, farmer_id: str) -> List[Dict]:
        response = requests.get(f"{self.base_url}/fields/farmer/{farmer_id}", headers=self.headers)
        return response.json()
    
    def file_claim(self, data: Dict) -> Dict:
        response = requests.post(f"{self.base_url}/insurance/claim", json=data, headers=self.headers)
        return response.json()
    
    def get_claim(self, claim_id: str) -> Dict:
        response = requests.get(f"{self.base_url}/insurance/claim/{claim_id}", headers=self.headers)
        return response.json()
    
    def list_claims(self) -> List[Dict]:
        response = requests.get(f"{self.base_url}/insurance/claims", headers=self.headers)
        return response.json()
    
    def get_ndvi(self, field_id: str, date: str = None) -> Dict:
        params = {"date": date} if date else {}
        response = requests.get(f"{self.base_url}/satellite/ndvi/{field_id}", params=params, headers=self.headers)
        return response.json()
    
    def get_satellite_timeline(self, field_id: str, start_date: str, end_date: str) -> Dict:
        params = {"start_date": start_date, "end_date": end_date}
        response = requests.get(f"{self.base_url}/satellite/timeline/{field_id}", params=params, headers=self.headers)
        return response.json()
    
    def get_blockchain_stats(self) -> Dict:
        response = requests.get(f"{API_URL}/blockchain/stats", headers=self.headers)
        return response.json()
    
    def get_all_blocks(self) -> Dict:
        response = requests.get(f"{API_URL}/blockchain/blocks", headers=self.headers)
        return response.json()

api_client = APIClient()
