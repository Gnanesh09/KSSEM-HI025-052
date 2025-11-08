# app/api/v1/payments.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.payment import Payment
from app.schemas.payment import PaymentCreate, PaymentResponse, RazorpayVerify, UPIGenerate
from app.services.payment_service import payment_service
from datetime import datetime

router = APIRouter(prefix="/payments", tags=["Payments"])

@router.post("/create", response_model=PaymentResponse)
def create_payment(payment: PaymentCreate, db: Session = Depends(get_db)):
    """Create a payment order"""
    
    # Create payment record
    db_payment = Payment(
        claim_id=payment.claim_id,
        farmer_id=payment.farmer_id,
        field_id=payment.field_id,
        amount=payment.amount,
        payment_method=payment.payment_method,
        status="initiated"
    )
    
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    
    return db_payment

@router.post("/razorpay/create-order")
def create_razorpay_order(payment_id: str, amount: float, farmer_id: str, db: Session = Depends(get_db)):
    """Create Razorpay order"""
    
    payment = db.query(Payment).filter(Payment.payment_id == payment_id).first()
    if not payment:
        raise HTTPException(404, "Payment not found")
    
    order_data = payment_service.create_razorpay_order(payment_id, amount, farmer_id)
    
    if not order_data:
        raise HTTPException(500, "Failed to create Razorpay order")
    
    payment.razorpay_order_id = order_data['razorpay_order_id']
    db.commit()
    
    return order_data

@router.post("/razorpay/verify")
def verify_razorpay_payment(verify_data: RazorpayVerify, db: Session = Depends(get_db)):
    """Verify Razorpay payment"""
    
    if not payment_service.verify_razorpay_payment(
        verify_data.razorpay_payment_id,
        verify_data.razorpay_order_id,
        verify_data.razorpay_signature
    ):
        raise HTTPException(400, "Invalid payment signature")
    
    payment = db.query(Payment).filter(
        Payment.razorpay_order_id == verify_data.razorpay_order_id
    ).first()
    
    if not payment:
        raise HTTPException(404, "Payment not found")
    
    payment.razorpay_payment_id = verify_data.razorpay_payment_id
    payment.razorpay_signature = verify_data.razorpay_signature
    payment.status = "completed"
    payment.completed_at = datetime.utcnow()
    
    db.commit()
    
    return {"status": "Payment verified successfully", "payment_id": payment.payment_id}

@router.post("/upi/generate-qr")
def generate_upi_qr(upi_data: UPIGenerate, db: Session = Depends(get_db)):
    """Generate UPI QR code - FIXED"""
    
    payment = db.query(Payment).filter(Payment.payment_id == upi_data.payment_id).first()
    if not payment:
        raise HTTPException(404, "Payment not found")
    
    # Generate QR - FIXED: Now returns base64
    qr_data = payment_service.generate_upi_qr(
        upi_data.payment_id,
        payment.amount,
        payment.farmer_id,
        "Farmer"
    )
    
    if not qr_data:
        raise HTTPException(500, "Failed to generate QR code")
    
    # Update payment - FIXED: Use qr_code_base64 instead of qr_code_path
    payment.upi_id = upi_data.upi_id
    payment.status = "initiated"
    
    # Don't store base64 in DB - it's huge! Just keep upi_id
    # qr_code_base64 is generated on-demand, not stored
    
    db.commit()
    
    # Return response with base64 QR code
    return {
        "qr_code_base64": qr_data['qr_code_base64'],  # FIXED
        "upi_string": qr_data['upi_string'],
        "payment_id": upi_data.payment_id
    }

@router.post("/upi/confirm")
def confirm_upi_payment(payment_id: str, upi_transaction_id: str, db: Session = Depends(get_db)):
    """Confirm UPI payment"""
    
    payment = db.query(Payment).filter(Payment.payment_id == payment_id).first()
    if not payment:
        raise HTTPException(404, "Payment not found")
    
    payment.upi_transaction_id = upi_transaction_id
    payment.status = "completed"
    payment.completed_at = datetime.utcnow()
    
    db.commit()
    
    return {"status": "UPI payment confirmed", "payment_id": payment_id}

@router.post("/bank-transfer/details")
def get_bank_transfer_details(payment_id: str, db: Session = Depends(get_db)):
    """Get bank transfer details"""
    
    payment = db.query(Payment).filter(Payment.payment_id == payment_id).first()
    if not payment:
        raise HTTPException(404, "Payment not found")
    
    details = payment_service.generate_bank_transfer_details(payment_id, payment.farmer_id, payment.amount)
    
    payment.bank_account = details['account_number']
    payment.bank_ifsc = details['ifsc_code']
    payment.transaction_reference = details['reference']
    payment.status = "initiated"
    
    db.commit()
    
    return details

@router.get("/get/{payment_id}", response_model=PaymentResponse)
def get_payment(payment_id: str, db: Session = Depends(get_db)):
    """Get payment details"""
    
    payment = db.query(Payment).filter(Payment.payment_id == payment_id).first()
    if not payment:
        raise HTTPException(404, "Payment not found")
    
    return payment

@router.get("/list/{farmer_id}")
def list_payments(farmer_id: str, db: Session = Depends(get_db)):
    """List all payments for farmer"""
    
    payments = db.query(Payment).filter(Payment.farmer_id == farmer_id).all()
    return payments
