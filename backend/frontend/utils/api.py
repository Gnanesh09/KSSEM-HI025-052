# frontend/utils/api.py
import requests
from typing import Dict, List, Any

API_URL = "http://localhost:8000"
API_BASE = "/api/v1"


class APIClient:
    def __init__(self):
        self.base_url = f"{API_URL}{API_BASE}"
        self.headers = {"Content-Type": "application/json"}
    
    # ============ FARMER APIs ============
    def register_farmer(self, data: Dict) -> Dict:
        response = requests.post(f"{self.base_url}/farmers/register", json=data, headers=self.headers)
        return response.json()
    
    def get_farmer(self, farmer_id: str) -> Dict:
        response = requests.get(f"{self.base_url}/farmers/{farmer_id}", headers=self.headers)
        return response.json()
    
    def list_farmers(self) -> List[Dict]:
        response = requests.get(f"{self.base_url}/farmers/", headers=self.headers)
        return response.json()
    
    # ============ FIELD APIs ============
    def register_field(self, data: Dict) -> Dict:
        response = requests.post(f"{self.base_url}/fields/register", json=data, headers=self.headers)
        return response.json()
    
    def get_field(self, field_id: str) -> Dict:
        response = requests.get(f"{self.base_url}/fields/{field_id}", headers=self.headers)
        return response.json()
    
    def get_farmer_fields(self, farmer_id: str) -> List[Dict]:
        response = requests.get(f"{self.base_url}/fields/farmer/{farmer_id}", headers=self.headers)
        return response.json()
    
    # ============ INSURANCE APIs ============
    def file_claim(self, data: Dict) -> Dict:
        response = requests.post(f"{self.base_url}/insurance/claim", json=data, headers=self.headers)
        return response.json()
    
    def get_claim(self, claim_id: str) -> Dict:
        response = requests.get(f"{self.base_url}/insurance/claim/{claim_id}", headers=self.headers)
        return response.json()
    
    def list_claims(self) -> List[Dict]:
        response = requests.get(f"{self.base_url}/insurance/claims", headers=self.headers)
        return response.json()
    
    # ============ SATELLITE APIs ============
    def get_ndvi(self, field_id: str, date: str = None) -> Dict:
        params = {"date": date} if date else {}
        response = requests.get(f"{self.base_url}/satellite/ndvi/{field_id}", params=params, headers=self.headers)
        return response.json()
    
    def get_satellite_timeline(self, field_id: str, start_date: str, end_date: str) -> Dict:
        params = {"start_date": start_date, "end_date": end_date}
        response = requests.get(f"{self.base_url}/satellite/timeline/{field_id}", params=params, headers=self.headers)
        return response.json()
    
    # ============ BLOCKCHAIN APIs ============
    def get_blockchain_stats(self) -> Dict:
        response = requests.get(f"{API_URL}/blockchain/stats", headers=self.headers)
        return response.json()
    
    def get_all_blocks(self) -> Dict:
        response = requests.get(f"{API_URL}/blockchain/blocks", headers=self.headers)
        return response.json()
    
    # ============ PAYMENT APIs ============
    def create_payment(self, data: Dict) -> Dict:
        """Create payment"""
        response = requests.post(f"{self.base_url}/payments/create", json=data, headers=self.headers)
        return response.json()
    
    def create_razorpay_order(self, payment_id: str, amount: float, farmer_id: str) -> Dict:
        """Create Razorpay order"""
        response = requests.post(
            f"{self.base_url}/payments/razorpay/create-order",
            params={"payment_id": payment_id, "amount": amount, "farmer_id": farmer_id},
            headers=self.headers
        )
        return response.json()
    
    def generate_upi_qr(self, data: Dict) -> Dict:
        """Generate UPI QR code - Returns base64 encoded QR"""
        response = requests.post(f"{self.base_url}/payments/upi/generate-qr", json=data, headers=self.headers)
        return response.json()
    
    def confirm_upi_payment(self, payment_id: str, upi_txn: str) -> Dict:
        """Confirm UPI payment"""
        response = requests.post(
            f"{self.base_url}/payments/upi/confirm",
            params={"payment_id": payment_id, "upi_transaction_id": upi_txn},
            headers=self.headers
        )
        return response.json()
    
    def get_bank_transfer_details(self, payment_id: str) -> Dict:
        """Get bank transfer details"""
        response = requests.post(
            f"{self.base_url}/payments/bank-transfer/details",
            params={"payment_id": payment_id},
            headers=self.headers
        )
        return response.json()
    
    # ============ CREDIT APIs ============
    def get_credit_profile(self, farmer_id: str) -> Dict:
        """Get farmer's credit profile"""
        response = requests.get(f"{self.base_url}/credits/profile/{farmer_id}", headers=self.headers)
        return response.json()
    
    def apply_for_loan(self, data: Dict) -> Dict:
        """Apply for agricultural loan"""
        response = requests.post(f"{self.base_url}/credits/apply-loan", json=data, headers=self.headers)
        return response.json()
    
    def get_loan_details(self, loan_id: str) -> Dict:
        """Get loan details"""
        response = requests.get(f"{self.base_url}/credits/loan/{loan_id}", headers=self.headers)
        return response.json()
    
    def approve_loan(self, loan_id: str, bank_name: str, account_no: str, ifsc: str) -> Dict:
        """Bank approves loan"""
        data = {
            "bank_name": bank_name,
            "account_no": account_no,
            "ifsc_code": ifsc
        }
        response = requests.post(
            f"{self.base_url}/credits/loan/{loan_id}/approve",
            json=data,
            headers=self.headers
        )
        return response.json()
    
    def disburse_loan(self, loan_id: str) -> Dict:
        """Disburse loan amount"""
        response = requests.post(
            f"{self.base_url}/credits/loan/{loan_id}/disburse",
            headers=self.headers
        )
        return response.json()
    
    def list_farmer_loans(self, farmer_id: str) -> List[Dict]:
        """List all loans for farmer"""
        response = requests.get(f"{self.base_url}/credits/loans/{farmer_id}", headers=self.headers)
        return response.json()
    
    def record_repayment(self, loan_id: str, amount: float, payment_method: str) -> Dict:
        """Record loan repayment"""
        params = {
            "amount": amount,
            "payment_method": payment_method
        }
        response = requests.post(
            f"{self.base_url}/credits/repayment/{loan_id}",
            params=params,
            headers=self.headers
        )
        return response.json()
    
    def get_credit_dashboard(self, farmer_id: str) -> Dict:
        """Get complete credit dashboard"""
        response = requests.get(f"{self.base_url}/credits/dashboard/{farmer_id}", headers=self.headers)
        return response.json()


# Global instance
api_client = APIClient()
