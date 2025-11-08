# app/models/payment.py
from sqlalchemy import Column, String, Float, DateTime, Integer
from sqlalchemy.sql import func
from app.database.session import Base
import uuid

class Payment(Base):
    __tablename__ = "payments"
    
    payment_id = Column(String, primary_key=True, default=lambda: f"PAY-{str(uuid.uuid4())[:8]}")
    claim_id = Column(String, nullable=False, index=True)
    farmer_id = Column(String, nullable=False, index=True)
    field_id = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    
    # Payment status: pending, initiated, completed, failed
    status = Column(String, default="pending")
    
    # Payment method: upi, card, bank_transfer
    payment_method = Column(String, default="upi")
    
    # Razorpay order details
    razorpay_order_id = Column(String, nullable=True)
    razorpay_payment_id = Column(String, nullable=True)
    razorpay_signature = Column(String, nullable=True)
    
    # UPI details
    upi_id = Column(String, nullable=True)
    upi_transaction_id = Column(String, nullable=True)
    qr_code_path = Column(String, nullable=True)
    
    # Bank transfer details
    bank_account = Column(String, nullable=True)
    bank_ifsc = Column(String, nullable=True)
    transaction_reference = Column(String, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    completed_at = Column(DateTime, nullable=True)
    
    def __repr__(self):
        return f"<Payment {self.payment_id} - {self.status}>"
