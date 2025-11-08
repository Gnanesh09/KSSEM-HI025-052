import streamlit as st
from utils.api import api_client
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from components.sidebar import show_sidebar
from components.translations import get_text

st.set_page_config(page_title="File Claim", page_icon="📋", layout="wide")

show_sidebar()

def t(key):
    return get_text(st.session_state.language, key, key)

st.markdown("# 📋 File Insurance Claim")

# Check if farmer is logged in
if 'farmer_id' not in st.session_state or not st.session_state.farmer_id:
    st.warning("⚠️ Please login first to file a claim")
    st.info("Go to Dashboard page and login/register")
    st.stop()

farmer_id = st.session_state.farmer_id

try:
    # Get farmer's fields - FIX: Use session farmer_id, not hardcoded
    fields = api_client.get_farmer_fields(farmer_id)
    
    if not fields:
        st.error(f"❌ No fields found for Farmer ID: {farmer_id}")
        st.info("Please register a field in the Dashboard first!")
        st.stop()
    
    st.markdown(f"**Filing claim for:** {farmer_id}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("## 📝 Claim Details")
        
        # FIX: Create proper field options without duplicates
        field_options = {}
        for f in fields:
            field_label = f"{f['field_id']} - {f['crop']} ({f['size_acres']} acres)"
            field_options[field_label] = f['field_id']
        
        if not field_options:
            st.error("No fields available")
            st.stop()
        
        selected_field_label = st.selectbox(
            "Select Your Field",
            list(field_options.keys()),
            help="Choose a field to file claim for"
        )
        
        field_id = field_options[selected_field_label]
        
        st.success(f"✅ Selected: {field_id}")
        
        # Damage type
        damage_type = st.radio(
            "Type of Damage",
            ["drought", "flood", "pest", "hailstorm"],
            captions=[t('claim.drought'), t('claim.flood'), t('claim.pest'), t('claim.hailstorm')],
            horizontal=True
        )
        
        # NDVI values
        col_a, col_b = st.columns(2)
        with col_a:
            pre_ndvi = st.slider("Pre-Damage NDVI", 0.0, 1.0, 0.78, 0.01, help="Health before damage (0-1)")
        with col_b:
            post_ndvi = st.slider("Post-Damage NDVI", 0.0, 1.0, 0.29, 0.01, help="Health after damage (0-1)")
        
        # Calculate damage
        if pre_ndvi > 0:
            damage_pct = ((pre_ndvi - post_ndvi) / pre_ndvi) * 100
        else:
            damage_pct = 0
        
        st.markdown("---")
        
        # Display damage assessment
        if damage_pct > 50:
            st.success(f"### 🎯 Damage: {damage_pct:.1f}%")
            st.success("✅ **QUALIFIES FOR INSURANCE**")
            st.info(f"Expected payout: ₹{int(damage_pct * 1000):,}")
        else:
            st.warning(f"### 🎯 Damage: {damage_pct:.1f}%")
            st.warning("❌ **Below 50% threshold - Does not qualify**")
    
    with col2:
        st.markdown("## 🛰️ Satellite Verification")
        
        if st.button("🛰️ Fetch Satellite Data", use_container_width=True):
            with st.spinner("Fetching satellite data..."):
                try:
                    sat_data = api_client.get_ndvi(field_id)
                    
                    st.markdown("### Real Satellite Data")
                    st.json(sat_data)
                    
                    st.markdown("### Before (Healthy)")
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.metric("NDVI", f"{pre_ndvi:.2f}", delta="Healthy", delta_color="normal")
                    with col_b:
                        st.success("✅ Crop is healthy")
                    
                    st.markdown("### After (Damaged)")
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.metric("NDVI", f"{post_ndvi:.2f}", delta=f"-{damage_pct:.1f}%", delta_color="inverse")
                    with col_b:
                        if damage_pct > 30:
                            st.error("❌ Crop is damaged")
                        else:
                            st.warning("⚠️ Crop is stressed")
                
                except Exception as e:
                    st.error(f"Error fetching satellite data: {str(e)}")
        else:
            st.info("📡 Click button to fetch real satellite data for this field")
    
    st.markdown("---")
    
    # Submit button
    if st.button("⛓️ Submit Claim to Blockchain", use_container_width=True, type="primary"):
        with st.spinner("Processing claim on blockchain..."):
            try:
                claim_response = api_client.file_claim({
                    "field_id": field_id,
                    "damage_type": damage_type,
                    "pre_ndvi": pre_ndvi,
                    "post_ndvi": post_ndvi,
                })
                
                st.markdown("---")
                
                if claim_response.get('status') == 'APPROVED':
                    st.balloons()
                    st.success("### ✅ CLAIM APPROVED!")
                    
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Claim ID", claim_response.get('claim_id', 'N/A'))
                    col2.metric("Payout", f"₹{claim_response.get('payout', 0):,}")
                    col3.metric("Status", "Approved ✅")
                    
                    st.markdown("### 📋 Claim Details")
                    col1, col2, col3 = st.columns(3)
                    col1.info(f"**Field:** {claim_response.get('field_id')}")
                    col2.info(f"**Damage:** {claim_response.get('damage_percent', 0):.1f}%")
                    col3.info(f"**Blockchain TX:** {claim_response.get('blockchain_tx', '')[:16]}...")
                    
                    st.success("✨ **Payment will be credited within 24 hours**")
                
                else:
                    st.error("### ❌ CLAIM REJECTED")
                    st.error(f"❌ Damage percentage ({damage_pct:.1f}%) is below 50% threshold")
                    st.warning("This field does not have enough damage to qualify for insurance")
            
            except Exception as e:
                st.error(f"❌ Error filing claim: {str(e)}")
                st.info("Make sure backend is running")

except Exception as e:
    st.error(f"Error: {str(e)}")
    st.info("1. Make sure backend is running on http://localhost:8000")
    st.info("2. Go to Dashboard and register a field first")
