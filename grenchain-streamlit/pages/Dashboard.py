import streamlit as st
from utils.api import api_client
from components.sidebar import show_sidebar
from components.translations import get_text

st.set_page_config(page_title="Dashboard", page_icon="👤", layout="wide")

show_sidebar()

def t(key):
    return get_text(st.session_state.language, key, key)

st.markdown("# 👤 " + t('dashboard.welcome'))

try:
    farmer = api_client.get_farmer("FAR-0001")
    fields = api_client.get_farmer_fields("FAR-0001")
    claims = api_client.list_claims()
    
    st.markdown(f"### Welcome, {farmer.get('name', 'Farmer')}! 👋")
    st.markdown(f"**Farmer ID:** {farmer.get('farmer_id')}")
    st.markdown("---")
    
    approved_claims = [c for c in claims if c.get('status') == 'APPROVED']
    total_payout = sum(c.get('payout', 0) for c in approved_claims)
    
    col1, col2, col3 = st.columns(3)
    col1.metric("🌾 " + t('dashboard.my_fields'), len(fields))
    col2.metric("✅ " + t('dashboard.approved'), len(approved_claims))
    col3.metric("💰 " + t('dashboard.payout'), f"₹{total_payout:,}")
    
    st.markdown("---")
    st.markdown("## 🌾 " + t('dashboard.my_fields'))
    
    if fields:
        for field in fields:
            with st.expander(f"🌾 {field.get('field_id')} - {field.get('crop')}"):
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Size", f"{field.get('size_acres')} acres")
                col2.metric("Crop", field.get('crop'))
                col3.metric("Location", field.get('location'))
                col4.metric("NDVI", field.get('latest_ndvi', 'N/A'))
    else:
        st.warning("No fields registered yet!")

except Exception as e:
    st.error(f"Error: {str(e)}")
    st.info("Make sure backend is running on http://localhost:8000")
