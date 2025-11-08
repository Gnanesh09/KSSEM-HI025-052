# app/schemas/payment.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class PaymentCreate(BaseModel):
    claim_id: str
    farmer_id: str
    field_id: str
    amount: float
    payment_method: str = "upi"  # upi, card, bank_transfer

class PaymentResponse(BaseModel):
    payment_id: str
    claim_id: str
    farmer_id: str
    amount: float
    status: str
    payment_method: str
    razorpay_order_id: Optional[str] = None
    upi_id: Optional[str] = None
    qr_code_path: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

class RazorpayVerify(BaseModel):
    razorpay_payment_id: str
    razorpay_order_id: str
    razorpay_signature: str

class UPIGenerate(BaseModel):
    payment_id: str
    upi_id: str
