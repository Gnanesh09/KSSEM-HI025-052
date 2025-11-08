# app/models/credit.py
from sqlalchemy import Column, String, Float, DateTime, Integer, Boolean
from sqlalchemy.sql import func
from app.database.session import Base
import uuid

class FarmerCreditProfile(Base):
    __tablename__ = "farmer_credit_profiles"
    
    profile_id = Column(String, primary_key=True, default=lambda: f"PROF-{str(uuid.uuid4())[:8]}")
    farmer_id = Column(String, nullable=False, unique=True, index=True)
    
    # Credit Score (0-100)
    credit_score = Column(Integer, default=0)
    
    # Financial Profile
    total_income_annual = Column(Float, default=0)  # From past claims/payouts
    total_claims_filed = Column(Integer, default=0)
    total_approved_claims = Column(Integer, default=0)
    total_payouts_received = Column(Float, default=0)
    approval_rate = Column(Float, default=0)  # %
    
    # Risk Assessment
    default_history = Column(String, default="NONE")  # NONE, LOW, MEDIUM, HIGH
    payment_delays = Column(Integer, default=0)
    
    # Credit Status
    is_eligible = Column(Boolean, default=False)
    max_credit_limit = Column(Float, default=0)
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    last_updated_by = Column(String, default="system")


class BankLoan(Base):
    __tablename__ = "bank_loans"
    
    loan_id = Column(String, primary_key=True, default=lambda: f"LOAN-{str(uuid.uuid4())[:8]}")
    farmer_id = Column(String, nullable=False, index=True)
    profile_id = Column(String, nullable=False)
    
    # Loan Details
    loan_amount = Column(Float, nullable=False)
    loan_tenure_months = Column(Integer, nullable=False)  # 6, 12, 24 months
    interest_rate = Column(Float, nullable=False)  # Based on credit score
    
    # Linked Insurance
    linked_field_id = Column(String, nullable=True)
    insurance_coverage = Column(Float, nullable=False)  # Insurance amount
    
    # Status: pending, approved, rejected, active, closed, defaulted
    status = Column(String, default="pending")
    
    # Bank Details
    bank_name = Column(String, nullable=True)
    bank_account = Column(String, nullable=True)
    ifsc_code = Column(String, nullable=True)
    
    # Blockchain
    blockchain_tx = Column(String, nullable=True)
    smart_contract_address = Column(String, nullable=True)
    
    # Repayment
    disbursed_amount = Column(Float, default=0)
    repaid_amount = Column(Float, default=0)
    pending_amount = Column(Float, default=0)
    
    # Dates
    applied_at = Column(DateTime, server_default=func.now())
    approved_at = Column(DateTime, nullable=True)
    disbursed_at = Column(DateTime, nullable=True)
    due_date = Column(DateTime, nullable=True)
    
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class LoanRepayment(Base):
    __tablename__ = "loan_repayments"
    
    repayment_id = Column(String, primary_key=True, default=lambda: f"REP-{str(uuid.uuid4())[:8]}")
    loan_id = Column(String, nullable=False, index=True)
    farmer_id = Column(String, nullable=False)
    
    # Payment Details
    amount = Column(Float, nullable=False)
    interest_charged = Column(Float, nullable=False)
    principal_paid = Column(Float, nullable=False)
    
    # Status: pending, completed, late, waived
    status = Column(String, default="pending")
    
    # Payment Method: upi, bank_transfer, auto_debit
    payment_method = Column(String, nullable=True)
    
    # Blockchain
    blockchain_tx = Column(String, nullable=True)
    
    # Dates
    due_date = Column(DateTime, nullable=False)
    paid_date = Column(DateTime, nullable=True)
    days_late = Column(Integer, default=0)
    
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
