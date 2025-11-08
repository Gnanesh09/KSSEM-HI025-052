# app/services/credit_service.py - FIXED VERSION

from app.database.session import get_db
from app.models.credit import FarmerCreditProfile, BankLoan, LoanRepayment
from app.models.insurance import InsuranceClaim
from app.models.fields import Field
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import math

class CreditService:
    """Agricultural Credit Scoring & Loan Management"""
    
    @staticmethod
    def calculate_credit_score(db: Session, farmer_id: str) -> int:
        """
        Calculate credit score based on:
        - Claims history
        - Insurance payouts
        - Approval rate
        """
        # FIX: Properly join Field to get claims for farmer
        claims = db.query(InsuranceClaim).join(
            Field, InsuranceClaim.field_id == Field.field_id
        ).filter(
            Field.farmer_id == farmer_id
        ).all()
        
        if not claims:
            return 30  # Default score for new farmers
        
        approved = len([c for c in claims if c.status == 'APPROVED'])
        total = len(claims)
        
        # Score calculation
        base_score = 20
        approval_score = (approved / total) * 50 if total > 0 else 0
        consistency_score = min(len(claims) * 10, 30)  # More claims = higher
        
        score = int(base_score + approval_score + consistency_score)
        return min(score, 100)
    
    @staticmethod
    def calculate_max_credit(credit_score: int, annual_income: float) -> float:
        """
        Calculate max credit limit based on score & income
        
        Score 80+: 300% of annual income
        Score 60-80: 200% of annual income
        Score 40-60: 100% of annual income
        Score <40: Not eligible
        """
        if credit_score < 40:
            return 0
        elif credit_score < 60:
            return annual_income * 1.0
        elif credit_score < 80:
            return annual_income * 2.0
        else:
            return annual_income * 3.0
    
    @staticmethod
    def calculate_interest_rate(credit_score: int) -> float:
        """
        Interest rates based on credit score
        
        Score 80+: 3% (Excellent)
        Score 60-80: 5% (Good)
        Score 40-60: 8% (Fair)
        Score <40: Not eligible
        """
        if credit_score >= 80:
            return 3.0
        elif credit_score >= 60:
            return 5.0
        elif credit_score >= 40:
            return 8.0
        else:
            return 0  # Not eligible
    
    @staticmethod
    def create_credit_profile(db: Session, farmer_id: str, claims: list) -> dict:
        """Create/update farmer credit profile"""
        
        # Calculate metrics
        total_payouts = sum(c.get('payout', 0) for c in claims if c.get('status') == 'APPROVED')
        approved_count = len([c for c in claims if c.get('status') == 'APPROVED'])
        total_count = len(claims)
        approval_rate = (approved_count / total_count * 100) if total_count > 0 else 0
        
        # Annual income (estimated from claims)
        annual_income = total_payouts * 1.2  # Assume 120% of payouts
        
        # Calculate score
        credit_score = CreditService.calculate_credit_score(db, farmer_id)
        max_credit = CreditService.calculate_max_credit(credit_score, annual_income)
        
        # Create profile
        profile = FarmerCreditProfile(
            farmer_id=farmer_id,
            credit_score=credit_score,
            total_income_annual=annual_income,
            total_claims_filed=total_count,
            total_approved_claims=approved_count,
            total_payouts_received=total_payouts,
            approval_rate=approval_rate,
            is_eligible=credit_score >= 40,
            max_credit_limit=max_credit
        )
        
        db.add(profile)
        db.commit()
        
        return {
            "profile_id": profile.profile_id,
            "credit_score": credit_score,
            "max_credit_limit": max_credit,
            "is_eligible": credit_score >= 40
        }
    
    @staticmethod
    def create_loan_application(db: Session, farmer_id: str, loan_amount: float, 
                               tenure_months: int, field_id: str, insurance_amount: float) -> dict:
        """Create loan application"""
        
        # Get credit profile
        profile = db.query(FarmerCreditProfile).filter(
            FarmerCreditProfile.farmer_id == farmer_id
        ).first()
        
        if not profile:
            return {"error": "Credit profile not found"}
        
        if not profile.is_eligible:
            return {"error": "Not eligible for credit"}
        
        if loan_amount > profile.max_credit_limit:
            return {"error": f"Loan exceeds max limit: ₹{profile.max_credit_limit:,}"}
        
        # Calculate interest
        interest_rate = CreditService.calculate_interest_rate(profile.credit_score)
        
        # Create loan
        loan = BankLoan(
            farmer_id=farmer_id,
            profile_id=profile.profile_id,
            loan_amount=loan_amount,
            loan_tenure_months=tenure_months,
            interest_rate=interest_rate,
            linked_field_id=field_id,
            insurance_coverage=insurance_amount,
            status="pending"
        )
        
        db.add(loan)
        db.commit()
        
        return {
            "loan_id": loan.loan_id,
            "loan_amount": loan_amount,
            "interest_rate": interest_rate,
            "tenure_months": tenure_months,
            "monthly_payment": CreditService.calculate_monthly_payment(
                loan_amount, interest_rate, tenure_months
            ),
            "insurance_coverage": insurance_amount,
            "status": "pending"
        }
    
    @staticmethod
    def calculate_monthly_payment(principal: float, annual_rate: float, months: int) -> float:
        """Calculate monthly EMI"""
        monthly_rate = annual_rate / 100 / 12
        if monthly_rate == 0:
            return principal / months
        
        emi = (principal * monthly_rate * (1 + monthly_rate) ** months) / \
              ((1 + monthly_rate) ** months - 1)
        return round(emi, 2)

credit_service = CreditService()
