# app/api/v1/credits.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.credit import FarmerCreditProfile, BankLoan, LoanRepayment
from app.models.insurance import InsuranceClaim
from app.models.fields import Field
from app.services.credit_service import credit_service
from app.schemas.credit import (
    LoanApplication, 
    CreditProfileResponse, 
    LoanResponse,
    LoanApprovalRequest,
    RepaymentResponse
)
from datetime import datetime, timedelta

router = APIRouter(prefix="/credits", tags=["Credits"])

@router.get("/profile/{farmer_id}", response_model=CreditProfileResponse)
def get_credit_profile(farmer_id: str, db: Session = Depends(get_db)):
    """Get farmer's credit profile"""
    
    profile = db.query(FarmerCreditProfile).filter(
        FarmerCreditProfile.farmer_id == farmer_id
    ).first()
    
    if not profile:
        # Create if doesn't exist
        # FIX: Join Field to get claims for this farmer
        claims = db.query(InsuranceClaim).join(
            Field, InsuranceClaim.field_id == Field.field_id
        ).filter(
            Field.farmer_id == farmer_id
        ).all()
        
        # Convert to dict for service
        claims_dict = [
            {
                'claim_id': c.claim_id,
                'field_id': c.field_id,
                'payout': c.payout,
                'status': c.status,
                'damage_type': c.damage_type
            }
            for c in claims
        ]
        
        result = credit_service.create_credit_profile(db, farmer_id, claims_dict)
        
        # Fetch and return the created profile
        profile = db.query(FarmerCreditProfile).filter(
            FarmerCreditProfile.farmer_id == farmer_id
        ).first()
    
    return profile
@router.post("/apply-loan")
def apply_for_loan(application: LoanApplication, db: Session = Depends(get_db)):
    """Apply for agricultural loan"""
    
    result = credit_service.create_loan_application(
        db,
        application.farmer_id,
        application.loan_amount,
        application.tenure_months,
        application.field_id,
        application.insurance_amount
    )
    
    if "error" in result:
        raise HTTPException(400, result["error"])
    
    # Return the dict directly (not the model)
    return result  # FIXED: Return dict, not BankLoan model

@router.get("/loan/{loan_id}", response_model=LoanResponse)
def get_loan_details(loan_id: str, db: Session = Depends(get_db)):
    """Get loan details"""
    
    loan = db.query(BankLoan).filter(BankLoan.loan_id == loan_id).first()
    
    if not loan:
        raise HTTPException(404, "Loan not found")
    
    return loan

@router.post("/loan/{loan_id}/approve")
def approve_loan(loan_id: str, bank_details: LoanApprovalRequest, db: Session = Depends(get_db)):
    """Bank approves loan"""
    
    loan = db.query(BankLoan).filter(BankLoan.loan_id == loan_id).first()
    
    if not loan:
        raise HTTPException(404, "Loan not found")
    
    loan.status = "approved"
    loan.bank_name = bank_details.bank_name
    loan.bank_account = bank_details.account_no
    loan.ifsc_code = bank_details.ifsc_code
    loan.approved_at = datetime.utcnow()
    
    db.commit()
    
    return {"status": "Loan approved!", "loan_id": loan_id}

@router.post("/loan/{loan_id}/disburse")
def disburse_loan(loan_id: str, db: Session = Depends(get_db)):
    """Disburse loan amount to farmer"""
    
    loan = db.query(BankLoan).filter(BankLoan.loan_id == loan_id).first()
    
    if not loan:
        raise HTTPException(404, "Loan not found")
    
    if loan.status != "approved":
        raise HTTPException(400, "Loan must be approved first")
    
    loan.status = "active"
    loan.disbursed_amount = loan.loan_amount
    loan.pending_amount = loan.loan_amount
    loan.disbursed_at = datetime.utcnow()
    loan.due_date = datetime.utcnow() + timedelta(days=30)
    
    db.commit()
    
    return {
        "status": "Loan disbursed!",
        "amount": loan.loan_amount,
        "disbursed_at": loan.disbursed_at,
        "first_emi_due": loan.due_date
    }

@router.get("/loans/{farmer_id}")
def list_farmer_loans(farmer_id: str, db: Session = Depends(get_db)):
    """List all loans for a farmer"""
    
    loans = db.query(BankLoan).filter(BankLoan.farmer_id == farmer_id).all()
    return loans

@router.post("/repayment/{loan_id}")
def record_repayment(loan_id: str, amount: float, payment_method: str, db: Session = Depends(get_db)):
    """Record loan repayment"""
    
    loan = db.query(BankLoan).filter(BankLoan.loan_id == loan_id).first()
    
    if not loan:
        raise HTTPException(404, "Loan not found")
    
    if loan.pending_amount <= 0:
        raise HTTPException(400, "Loan is already fully repaid")
    
    # Calculate interest
    interest_charged = (amount * loan.interest_rate) / 100 / 12
    principal_paid = amount - interest_charged
    
    # Create repayment record
    repayment = LoanRepayment(
        loan_id=loan_id,
        farmer_id=loan.farmer_id,
        amount=amount,
        interest_charged=interest_charged,
        principal_paid=principal_paid,
        payment_method=payment_method,
        status="completed",
        paid_date=datetime.utcnow()
    )
    
    # Update loan
    loan.repaid_amount += principal_paid
    loan.pending_amount -= principal_paid
    
    if loan.pending_amount <= 0:
        loan.status = "closed"
    
    db.add(repayment)
    db.commit()
    
    return {
        "status": "Repayment recorded",
        "amount_paid": amount,
        "remaining_balance": max(0, loan.pending_amount)
    }

@router.get("/dashboard/{farmer_id}")
def credit_dashboard(farmer_id: str, db: Session = Depends(get_db)):
    """Get complete credit dashboard for farmer"""
    
    # Get profile
    profile = db.query(FarmerCreditProfile).filter(
        FarmerCreditProfile.farmer_id == farmer_id
    ).first()
    
    # Get loans
    loans = db.query(BankLoan).filter(BankLoan.farmer_id == farmer_id).all()
    
    # Get repayments
    repayments = db.query(LoanRepayment).filter(
        LoanRepayment.farmer_id == farmer_id
    ).all()
    
    return {
        "credit_profile": profile,
        "loans": loans,
        "repayments": repayments,
        "summary": {
            "total_borrowed": sum(l.loan_amount for l in loans),
            "total_repaid": sum(r.principal_paid for r in repayments),
            "active_loans": len([l for l in loans if l.status == "active"]),
            "closed_loans": len([l for l in loans if l.status == "closed"])
        }
    }
