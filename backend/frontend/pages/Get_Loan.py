import streamlit as st
from utils.api import api_client
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from components.sidebar import show_sidebar

st.set_page_config(page_title="Get Loan", page_icon="💳", layout="wide")

show_sidebar()

st.markdown("# 💳 Agricultural Credit Line")

if 'farmer_id' not in st.session_state or not st.session_state.farmer_id:
    st.warning("⚠️ Please login first")
    st.stop()

try:
    farmer_id = st.session_state.farmer_id
    
    # Get credit profile
    profile = api_client.get_credit_profile(farmer_id)
    
    st.markdown("## 📊 Your Credit Profile")
    
    col1, col2, col3, col4 = st.columns(4)
    
    col1.metric("📈 Credit Score", profile['credit_score'], "/100")
    col2.metric("✅ Approval Rate", f"{profile['approval_rate']:.1f}%")
    col3.metric("💰 Max Credit", f"₹{profile['max_credit_limit']:,.0f}")
    col4.metric("📦 Claims Approved", profile['total_approved_claims'])
    
    st.markdown("---")
    
    if profile['is_eligible']:
        st.success(f"✅ You're eligible for agricultural credit!")
        
        st.markdown("## 💸 Apply for Loan")
        
        col1, col2 = st.columns(2)
        
        with col1:
            loan_amount = st.number_input(
                "Loan Amount (₹)",
                min_value=10000,
                max_value=int(profile['max_credit_limit']),
                step=10000,
                value=50000
            )
        
        with col2:
            tenure = st.selectbox(
                "Loan Duration",
                [6, 12, 24],
                format_func=lambda x: f"{x} months"
            )
        
        fields = api_client.get_farmer_fields(farmer_id)
        
        if fields:
            field_options = {f"{f['field_id']} - {f['crop']}": f for f in fields}
            selected_field_label = st.selectbox("Linked Field", list(field_options.keys()))
            selected_field = field_options[selected_field_label]
            
            # Estimate insurance coverage
            insurance_amount = loan_amount * 1.2  # 120% insurance
            
            st.markdown("---")
            
            # Show loan details
            st.markdown("### 📋 Loan Summary")
            
            col1, col2, col3, col4 = st.columns(4)
            
            # Calculate monthly payment
            monthly_rate = 5.0 / 100 / 12  # Assuming 5% interest
            months = tenure
            if monthly_rate == 0:
                monthly_payment = loan_amount / months
            else:
                monthly_payment = (loan_amount * monthly_rate * (1 + monthly_rate) ** months) / \
                                 ((1 + monthly_rate) ** months - 1)
            
            col1.metric("💰 Loan Amount", f"₹{loan_amount:,}")
            col2.metric("📅 Duration", f"{tenure} months")
            col3.metric("💵 Monthly EMI", f"₹{monthly_payment:,.0f}")
            col4.metric("🛡️ Insurance", f"₹{insurance_amount:,.0f}")
            
            st.info(f"""
            ### Key Benefits
            - ✅ Interest Rate: 5% (based on your credit score)
            - ✅ Automatic crop insurance (linked to field)
            - ✅ Insurance covers loan in case of damage
            - ✅ Flexible repayment options
            - ✅ Fast approval (blockchain verified)
            """)
            
            st.markdown("---")
            
            if st.button("📝 Apply for Loan", use_container_width=True, type="primary"):
                with st.spinner("Processing loan application..."):
                    try:
                        loan_response = api_client.apply_for_loan({
                            "farmer_id": farmer_id,
                            "loan_amount": loan_amount,
                            "tenure_months": tenure,
                            "field_id": selected_field['field_id'],
                            "insurance_amount": insurance_amount
                        })
                        
                        st.balloons()
                        st.success("✅ Loan Application Submitted!")
                        
                        st.json({
                            "Loan ID": loan_response['loan_id'],
                            "Amount": f"₹{loan_response['loan_amount']:,}",
                            "Monthly EMI": f"₹{loan_response['monthly_payment']:,.0f}",
                            "Status": "Pending Bank Approval"
                        })
                        
                        st.info("""
                        ⏱️ **Next Steps:**
                        1. Bank will review your application
                        2. You'll receive approval confirmation
                        3. Loan amount credited to your account
                        4. Start repayment after 1 month grace period
                        """)
                    
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
        else:
            st.warning("⚠️ Please register a field first")
    
    else:
        st.warning(f"""
        ⚠️ Your credit score ({profile['credit_score']}/100) is below eligibility threshold.
        
        **How to Improve:**
        - File more insurance claims ✅
        - Get them approved consistently ✅
        - Build a track record 📈
        """)

except Exception as e:
    st.error(f"Error: {str(e)}")
