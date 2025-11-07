import streamlit as st
from utils.api import api_client
from components.sidebar import show_sidebar
from components.translations import get_text

st.set_page_config(page_title="Satellite", page_icon="🛰️", layout="wide")

show_sidebar()

st.markdown("# 🛰️ Satellite Verification")

try:
    fields = api_client.get_farmer_fields("FAR-0001")
    
    field_options = {f"{f['field_id']} - {f['crop']}": f['field_id'] for f in fields}
    selected = st.selectbox("Select Field", list(field_options.keys()))
    field_id = field_options[selected]
    
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

except Exception as e:
    st.error(f"Error: {str(e)}")
