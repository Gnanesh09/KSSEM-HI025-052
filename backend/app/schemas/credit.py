# app/schemas/credit.py
from pydantic import BaseModel, computed_field
from datetime import datetime
from typing import Optional

class CreditProfileResponse(BaseModel):
    profile_id: str
    farmer_id: str
    credit_score: int
    total_income_annual: float
    total_claims_filed: int
    total_approved_claims: int
    total_payouts_received: float
    approval_rate: float
    is_eligible: bool
    max_credit_limit: float
    created_at: datetime
    
    class Config:
        from_attributes = True


class LoanApplication(BaseModel):
    farmer_id: str
    loan_amount: float
    tenure_months: int
    field_id: str
    insurance_amount: float


class LoanResponse(BaseModel):
    loan_id: str
    farmer_id: str
    loan_amount: float
    interest_rate: float
    loan_tenure_months: int  # FIXED: Match DB field name
    insurance_coverage: float
    status: str
    linked_field_id: Optional[str] = None
    applied_at: datetime
    
    @computed_field  # FIXED: Compute monthly payment
    @property
    def monthly_payment(self) -> float:
        """Calculate monthly EMI"""
        monthly_rate = self.interest_rate / 100 / 12
        months = self.loan_tenure_months
        
        if monthly_rate == 0:
            return self.loan_amount / months
        
        emi = (self.loan_amount * monthly_rate * (1 + monthly_rate) ** months) / \
              ((1 + monthly_rate) ** months - 1)
        return round(emi, 2)
    
    @computed_field  # FIXED: Compute total interest
    @property
    def total_interest(self) -> float:
        """Calculate total interest"""
        return (self.monthly_payment * self.loan_tenure_months) - self.loan_amount
    
    class Config:
        from_attributes = True


class LoanApprovalRequest(BaseModel):
    bank_name: str
    account_no: str
    ifsc_code: str


class RepaymentResponse(BaseModel):
    repayment_id: str
    loan_id: str
    amount: float
    interest_charged: float
    principal_paid: float
    status: str
    due_date: datetime
    paid_date: Optional[datetime] = None
    
    class Config:
        from_attributes = True
