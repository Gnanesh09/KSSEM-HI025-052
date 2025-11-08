import streamlit as st
from utils.api import api_client
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from components.sidebar import show_sidebar

st.set_page_config(page_title="Satellite", page_icon="🛰️", layout="wide")

show_sidebar()

st.markdown("# 🛰️ Satellite Verification")

if 'farmer_id' not in st.session_state or not st.session_state.farmer_id:
    st.warning("⚠️ Please login first")
    st.stop()

try:
    # Use session farmer_id - FIX: Not hardcoded
    fields = api_client.get_farmer_fields(st.session_state.farmer_id)
    
    if not fields:
        st.error("No fields found")
        st.stop()
    
    # Create field options
    field_options = {}
    for f in fields:
        field_label = f"{f['field_id']} - {f['crop']}"
        field_options[field_label] = f['field_id']
    
    selected = st.selectbox("Select Field", list(field_options.keys()))
    field_id = field_options[selected]
    
    # Fetch satellite data
    sat_data = api_client.get_ndvi(field_id)
    
    col1, col2, col3 = st.columns(3)
    col1.metric("NDVI", f"{sat_data.get('ndvi', 0):.2f}")
    col2.metric("Status", sat_data.get('status', 'N/A'))
    col3.metric("Date", sat_data.get('date', 'N/A'))
    
    ndvi = sat_data.get('ndvi', 0)
    if ndvi > 0.6:
        st.success("✅ HEALTHY CROP")
    elif ndvi > 0.4:
        st.warning("⚠️ MODERATE HEALTH")
    elif ndvi > 0.2:
        st.warning("❌ STRESSED CROP")
    else:
        st.error("🔴 SEVERELY DAMAGED")
    
    st.info(f"**Source:** {sat_data.get('source', 'Unknown')}")
    st.json(sat_data)

except Exception as e:
    st.error(f"Error: {str(e)}")
