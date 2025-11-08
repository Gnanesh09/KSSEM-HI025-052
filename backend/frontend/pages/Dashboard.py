import streamlit as st
from utils.api import api_client
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from components.sidebar import show_sidebar
from components.translations import get_text

st.set_page_config(page_title="Dashboard", page_icon="👤", layout="wide")

show_sidebar()

def t(key):
    return get_text(st.session_state.language, key, key)

st.markdown("# 👤 Dashboard")

# Initialize session state for farmer
if 'farmer_id' not in st.session_state:
    st.session_state.farmer_id = None

# If not logged in, show login/register
if not st.session_state.farmer_id:
    st.markdown("## 🔐 Farmer Login / Register")
    
    tab1, tab2 = st.tabs(["📝 Login", "🆕 Register"])
    
    with tab1:
        st.markdown("### Existing Farmer Login")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            farmer_id = st.text_input("Enter Farmer ID", placeholder="FAR-0001")
        
        with col2:
            st.write("")
            st.write("")
            login_btn = st.button("🔓 Login", use_container_width=True, type="primary")
        
        if login_btn:
            if not farmer_id:
                st.error("Please enter Farmer ID")
            else:
                try:
                    # Check if farmer exists
                    farmer = api_client.get_farmer(farmer_id)
                    st.session_state.farmer_id = farmer_id
                    st.session_state.farmer_name = farmer.get('name', 'Farmer')
                    st.success(f"✅ Welcome back, {farmer.get('name')}!")
                    st.rerun()
                except:
                    st.error(f"❌ Farmer ID '{farmer_id}' not found. Please register first!")
    
    with tab2:
        st.markdown("### Register New Farmer")
        
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Full Name", placeholder="Rajesh Kumar")
            phone = st.text_input("Phone", placeholder="+91-9876543210")
            location = st.text_input("Location", placeholder="Ramanagara")
        
        with col2:
            village = st.text_input("Village", placeholder="Kengeri")
            district = st.text_input("District", placeholder="Ramanagara", value="Ramanagara")
            state = st.text_input("State", placeholder="Karnataka", value="Karnataka")
        
        if st.button("✅ Register", use_container_width=True, type="primary"):
            if not all([name, phone, location]):
                st.error("Please fill all required fields")
            else:
                try:
                    response = api_client.register_farmer({
                        "name": name,
                        "phone": phone,
                        "location": location,
                        "village": village,
                        "district": district,
                        "state": state
                    })
                    
                    farmer_id = response.get('farmer_id')
                    st.session_state.farmer_id = farmer_id
                    st.session_state.farmer_name = name
                    st.balloons()
                    st.success(f"✅ Registration successful!")
                    st.info(f"**Your Farmer ID:** `{farmer_id}`")
                    st.write("Redirecting to dashboard...")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Registration failed: {str(e)}")

else:
    # LOGGED IN - Show Dashboard
    try:
        farmer = api_client.get_farmer(st.session_state.farmer_id)
        fields = api_client.get_farmer_fields(st.session_state.farmer_id)
        claims = api_client.list_claims()
        
        # Header with logout
        col1, col2 = st.columns([4, 1])
        
        with col1:
            st.markdown(f"### Welcome, {farmer.get('name')}! 👋")
            st.markdown(f"**Farmer ID:** {farmer.get('farmer_id')} | **Location:** {farmer.get('location')}")
        
        with col2:
            if st.button("🚪 Logout", type="secondary"):
                st.session_state.farmer_id = None
                st.rerun()
        
        st.markdown("---")
        
        # Stats
        approved_claims = [c for c in claims if c.get('status') == 'APPROVED' and c.get('field_id') in [f.get('field_id') for f in fields]]
        total_payout = sum(c.get('payout', 0) for c in approved_claims)
        
        col1, col2, col3 = st.columns(3)
        col1.metric("🌾 My Fields", len(fields))
        col2.metric("✅ Claims Approved", len(approved_claims))
        col3.metric("💰 Total Payouts", f"₹{total_payout:,}")
        
        st.markdown("---")
        
        # Fields Section
        st.markdown("## 🌾 My Fields")
        
        tab1, tab2 = st.tabs(["📋 View Fields", "➕ Register New Field"])
        
        with tab1:
            if fields:
                for field in fields:
                    with st.expander(f"🌾 {field.get('field_id')} - {field.get('crop')}"):
                        col1, col2, col3, col4 = st.columns(4)
                        col1.metric("Size", f"{field.get('size_acres')} acres")
                        col2.metric("Crop", field.get('crop'))
                        col3.metric("Location", field.get('location'))
                        col4.metric("NDVI", field.get('latest_ndvi', 'N/A'))
                        
                        st.markdown(f"**Field ID:** `{field.get('field_id')}`")
            else:
                st.warning("No fields registered yet. Register your first field!")
        
        with tab2:
            st.markdown("### Register New Field")
            
            col1, col2 = st.columns(2)
            
            with col1:
                size_acres = st.number_input("Field Size (acres)", min_value=0.1, value=1.0, step=0.1)
                crop = st.selectbox("Crop Type", ["Tomatoes", "Onions", "Rice", "Potatoes", "Wheat", "Corn"])
            
            with col2:
                location = st.text_input("Field Location", placeholder="Ramanagara")
                gps_lat = st.number_input("GPS Latitude", value=12.72)
                gps_lon = st.number_input("GPS Longitude", value=77.28)
            
            if st.button("✅ Register Field", use_container_width=True, type="primary"):
                try:
                    response = api_client.register_field({
                        "farmer_id": st.session_state.farmer_id,
                        "size_acres": size_acres,
                        "crop": crop,
                        "location": location,
                        "gps_latitude": gps_lat,
                        "gps_longitude": gps_lon,
                    })
                    
                    st.success(f"✅ Field registered successfully!")
                    st.info(f"**Field ID:** `{response.get('field_id')}`")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

    except Exception as e:
        st.error(f"Error loading dashboard: {str(e)}")
        st.info("Make sure backend is running on http://localhost:8000")
