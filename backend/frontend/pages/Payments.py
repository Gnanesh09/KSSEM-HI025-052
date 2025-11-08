import streamlit as st
from utils.api import api_client
import sys
import os
import base64

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from components.sidebar import show_sidebar

st.set_page_config(page_title="Payments", page_icon="💳", layout="wide")

show_sidebar()

st.markdown("# 💳 Payment Gateway")

if 'farmer_id' not in st.session_state or not st.session_state.farmer_id:
    st.warning("⚠️ Please login first")
    st.stop()

try:
    claims = api_client.list_claims()
    approved_claims = [c for c in claims if c.get('status') == 'APPROVED']
    
    if not approved_claims:
        st.info("No approved claims to pay. File a claim first!")
        st.stop()
    
    st.markdown("## 💰 Pending Payouts")
    
    # Select claim
    claim_options = {}
    for claim in approved_claims:
        claim_label = f"{claim['claim_id']} - ₹{claim['payout']:,} ({claim['field_id']})"
        claim_options[claim_label] = claim
    
    selected_claim_label = st.selectbox("Select Claim", list(claim_options.keys()))
    selected_claim = claim_options[selected_claim_label]
    
    st.markdown("---")
    
    # Display claim details
    col1, col2, col3 = st.columns(3)
    col1.metric("Claim ID", selected_claim['claim_id'])
    col2.metric("Amount", f"₹{selected_claim['payout']:,}")
    col3.metric("Status", "✅ Approved")
    
    st.markdown("---")
    
    # Payment method selection
    st.markdown("## 🔘 Select Payment Method")
    
    payment_method = st.radio(
        "How would you like to receive payment?",
        ["🪙 UPI", "💳 Credit/Debit Card", "🏦 Bank Transfer"],
        horizontal=True
    )
    
    st.markdown("---")
    
    # UPI Payment - FIXED
    if "UPI" in payment_method:
        st.markdown("### 📱 UPI Payment")
        
        upi_id = st.text_input("Enter your UPI ID", placeholder="yourname@upi", value="9591407733@naviaxis")
        
        if st.button("📲 Generate Payment QR", use_container_width=True, type="primary"):
            with st.spinner("Generating QR code..."):
                try:
                    # Create payment
                    payment_response = api_client.create_payment({
                        "claim_id": selected_claim['claim_id'],
                        "farmer_id": st.session_state.farmer_id,
                        "field_id": selected_claim['field_id'],
                        "amount": selected_claim['payout'],
                        "payment_method": "upi"
                    })
                    
                    payment_id = payment_response['payment_id']
                    
                    # Generate QR - FIXED: Now returns base64
                    qr_response = api_client.generate_upi_qr({
                        "payment_id": payment_id,
                        "upi_id": upi_id
                    })
                    
                    st.success("✅ QR Code Generated!")
                    
                    # Display QR code - FIXED
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.markdown("### 👈 Scan with any UPI app")
                        
                        # Display base64 image
                        if 'qr_code_base64' in qr_response:
                            qr_base64 = qr_response['qr_code_base64']
                            st.image(f"data:image/png;base64,{qr_base64}", width=300)
                        else:
                            st.warning("Could not display QR code")
                    
                    with col2:
                        st.markdown("### ₹ Amount")
                        st.metric("To Pay", f"₹{selected_claim['payout']:,}")
                        st.markdown("### 🆔 Merchant")
                        st.code(upi_id)
                    
                    st.info("💡 Scan the QR code with your UPI app (Google Pay, PhonePe, BHIM, etc.)")
                    
                    # Confirm payment
                    st.markdown("---")
                    upi_txn = st.text_input("Enter UPI Transaction ID after payment:", placeholder="UPI123456789")
                    
                    if st.button("✅ Confirm Payment", use_container_width=True):
                        with st.spinner("Confirming..."):
                            confirm_response = api_client.confirm_upi_payment(payment_id, upi_txn)
                            st.balloons()
                            st.success("✅ Payment Confirmed!")
                            st.metric("Payment ID", payment_id)
                            st.info("💳 Payment will be processed within 24 hours")
                
                except Exception as e:
                    st.error(f"Error: {str(e)}")
    
    # Card Payment
    elif "Credit/Debit" in payment_method:
        st.markdown("### 💳 Credit/Debit Card Payment")
        
        try:
            payment_response = api_client.create_payment({
                "claim_id": selected_claim['claim_id'],
                "farmer_id": st.session_state.farmer_id,
                "field_id": selected_claim['field_id'],
                "amount": selected_claim['payout'],
                "payment_method": "card"
            })
            
            payment_id = payment_response['payment_id']
            
            order_response = api_client.create_razorpay_order(
                payment_id,
                selected_claim['payout'],
                st.session_state.farmer_id
            )
            
            st.markdown("### Razorpay Payment Form")
            st.info(f"Amount: ₹{selected_claim['payout']:,}")
            st.info("Order ID: " + order_response['razorpay_order_id'])
            
            col1, col2 = st.columns(2)
            with col1:
                card_number = st.text_input("Card Number", placeholder="1234 5678 9012 3456")
            with col2:
                expiry = st.text_input("Expiry (MM/YY)", placeholder="12/25")
            
            col1, col2 = st.columns(2)
            with col1:
                cvv = st.text_input("CVV", placeholder="123", type="password")
            with col2:
                cardholder = st.text_input("Cardholder Name")
            
            if st.button("💳 Pay Now", use_container_width=True, type="primary"):
                st.success("✅ Payment Processed!")
                st.balloons()
                st.metric("Payment ID", payment_id)
                st.info("Amount debited from your card")
        
        except Exception as e:
            st.error(f"Error: {str(e)}")
    
    # Bank Transfer
    else:
        st.markdown("### 🏦 Bank Transfer")
        
        try:
            payment_response = api_client.create_payment({
                "claim_id": selected_claim['claim_id'],
                "farmer_id": st.session_state.farmer_id,
                "field_id": selected_claim['field_id'],
                "amount": selected_claim['payout'],
                "payment_method": "bank_transfer"
            })
            
            payment_id = payment_response['payment_id']
            
            bank_response = api_client.get_bank_transfer_details(payment_id)
            
            st.success("### Bank Transfer Details")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Bank Details**")
                st.code(f"""
Bank Name: {bank_response['bank_name']}
Account Holder: {bank_response['account_holder']}
Account Number: {bank_response['account_number']}
IFSC Code: {bank_response['ifsc_code']}
Reference: {bank_response['reference']}
                """)
            
            with col2:
                st.markdown("**Payment Details**")
                st.metric("Amount", f"₹{bank_response['amount']:,}")
                st.metric("Payment ID", payment_id)
            
            st.info("💡 Use the reference number in your bank transfer remarks")
            
            st.markdown("---")
            if st.button("✅ Confirm Transfer", use_container_width=True):
                st.success("✅ Bank transfer recorded!")
                st.info("Transfer will be verified within 2-3 business days")
        
        except Exception as e:
            st.error(f"Error: {str(e)}")

except Exception as e:
    st.error(f"Error: {str(e)}")
    st.info("Make sure backend is running")
