import streamlit as st
from utils.api import api_client
from components.sidebar import show_sidebar
from components.translations import get_text

st.set_page_config(page_title="File Claim", page_icon="📋", layout="wide")

show_sidebar()

def t(key):
    return get_text(st.session_state.language, key, key)

st.markdown("# 📋 " + t('claim.title'))

try:
    fields = api_client.get_farmer_fields("FAR-0001")
    
    if not fields:
        st.error("No fields found!")
        st.stop()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("## 📝 Claim Details")
        
        field_options = {f"{f['field_id']} - {f['crop']}": f['field_id'] for f in fields}
        selected_field = st.selectbox("Select Field", list(field_options.keys()))
        field_id = field_options[selected_field]
        
        damage_type = st.radio(
            "Type of Damage",
            ["drought", "flood", "pest", "hailstorm"],
            captions=[t('claim.drought'), t('claim.flood'), t('claim.pest'), t('claim.hailstorm')]
        )
        
        col_a, col_b = st.columns(2)
        with col_a:
            pre_ndvi = st.slider("Pre-Damage NDVI", 0.0, 1.0, 0.78, 0.01)
        with col_b:
            post_ndvi = st.slider("Post-Damage NDVI", 0.0, 1.0, 0.29, 0.01)
        
        damage_pct = ((pre_ndvi - post_ndvi) / pre_ndvi) * 100
        
        st.markdown("---")
        
        if damage_pct > 50:
            st.success(f"### Damage: {damage_pct:.1f}% - QUALIFIES ✅")
        else:
            st.warning(f"### Damage: {damage_pct:.1f}% - Below threshold ❌")
    
    with col2:
        st.markdown("## 🛰️ Satellite Data")
        
        try:
            sat_data = api_client.get_ndvi(field_id)
            
            st.markdown("### Before")
            col_a, col_b = st.columns(2)
            with col_a:
                st.metric("NDVI", pre_ndvi)
            with col_b:
                st.success("✅ Healthy")
            
            st.markdown("### After")
            col_a, col_b = st.columns(2)
            with col_a:
                st.metric("NDVI", post_ndvi)
            with col_b:
                if damage_pct > 50:
                    st.error("❌ Damaged")
                else:
                    st.warning("⚠️ Stressed")
        except:
            st.info("Fetching satellite data...")
    
    st.markdown("---")
    
    if st.button("⛓️ Submit Claim", use_container_width=True, type="primary"):
        with st.spinner("Processing..."):
            claim_response = api_client.file_claim({
                "field_id": field_id,
                "damage_type": damage_type,
                "pre_ndvi": pre_ndvi,
                "post_ndvi": post_ndvi,
            })
            
            if claim_response.get('status') == 'APPROVED':
                st.balloons()
                st.success("### ✅ " + t('claim.approved'))
                st.metric("Claim ID", claim_response.get('claim_id'))
                st.metric("Payout", f"₹{claim_response.get('payout', 0):,}")
                st.metric("Blockchain", claim_response.get('blockchain_tx', '')[:16] + "...")
            else:
                st.error("### ❌ " + t('claim.rejected'))

except Exception as e:
    st.error(f"Error: {str(e)}")
