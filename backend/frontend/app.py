import streamlit as st
from components.sidebar import show_sidebar
from components.translations import get_text

st.set_page_config(
    page_title="GreenChain",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

if 'language' not in st.session_state:
    st.session_state.language = 'en'

show_sidebar()

def t(key: str, default: str = None):
    return get_text(st.session_state.language, key, default)

st.markdown("# 🌾 GreenChain")
st.markdown("### Blockchain-Powered Crop Insurance")
st.markdown("---")

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    #### Instant verification. Zero fraud. Fair payouts.
    
    Transform agriculture with cutting-edge blockchain and satellite technology.
    """)
    
    # ✅ FIXED: Use simple button without switch_page
    if st.button("🚀 Go to Dashboard", use_container_width=True):
        st.write("📍 Navigate using the sidebar menu on the left")
        st.info("Click **👤 Dashboard** in the sidebar to continue")

with col2:
    st.success("""
    ### ✨ Features
    - 🛰️ Satellite Verification
    - ⛓️ Blockchain Recording
    - 💰 Fair Pricing
    - 🌍 Multilingual
    """)

st.markdown("---")

st.markdown("## 🎯 Key Features")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    ### 🛰️ Satellite Truth
    Sentinel-2 captures NDVI every 5 days.
    Physics doesn't lie!
    """)

with col2:
    st.markdown("""
    ### ⛓️ Blockchain Security
    Every claim recorded permanently.
    Immutable. Transparent.
    """)

with col3:
    st.markdown("""
    ### 💰 Fair Pricing
    Real-time mandi prices on blockchain.
    No middleman exploitation.
    """)

st.markdown("---")

st.markdown("## 📊 Impact")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Farmers", "500K+", "+25%")
col2.metric("Claims", "125K", "+40%")
col3.metric("Fraud Prevented", "₹9Cr", "99%")
col4.metric("Avg Payout", "24 hrs", "-95%")

st.markdown("---")

# Fixed: Dictionary outside f-string
lang_names = {
    'en': '🇬🇧 English',
    'hi': '🇮🇳 हिन्दी',
    'kn': '🌾 ಕನ್ನಡ',
    'te': '🏞️ తెలుగు'
}

st.info(f"🌐 **Language:** {lang_names[st.session_state.language]}")
