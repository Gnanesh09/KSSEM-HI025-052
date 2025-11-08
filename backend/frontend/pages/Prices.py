import streamlit as st
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from components.sidebar import show_sidebar

st.set_page_config(page_title="Prices", page_icon="💰", layout="wide")

show_sidebar()

st.markdown("# 💰 Fair Mandi Prices")

commodities = ['Tomatoes', 'Onions', 'Rice', 'Potatoes']
commodity = st.selectbox("Select Commodity", commodities)

location = st.selectbox("Select Location", ["Kolar", "Ramanagara", "Bangalore"])

if st.button("🔍 Check Fair Price"):
    col1, col2 = st.columns(2)
    with col1:
        st.success("### Fair Market Price")
        st.metric("Price", "₹22.50/kg")
    with col2:
        st.warning("### Offered Price")
        st.metric("Price", "₹19.13/kg", delta="By middlemen")
    
    st.info("On blockchain, verified by farmers!")
