import streamlit as st
from streamlit_extras.switch_page_button import switch_page  # ✅ Added correct import

# ✅ Import sidebar and translations (ensure these files exist)
from components.sidebar import show_sidebar
from components.translations import TRANSLATIONS, get_text

# ✅ Page configuration (must come first)
st.set_page_config(
    page_title="GreenChain",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ✅ Initialize session state for language
if 'language' not in st.session_state:
    st.session_state.language = 'en'

# ✅ Show sidebar
show_sidebar()

# ✅ Helper translation function
def t(key: str, default: str = None):
    return get_text(st.session_state.language, key, default)

# --------------------------------------------------
# 🌾 MAIN PAGE CONTENT
# --------------------------------------------------
st.markdown("# 🌾 GreenChain")
st.markdown("### Blockchain-Powered Crop Insurance")
st.markdown("---")

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    #### Instant verification. Zero fraud. Fair payouts.
    
    Transform agriculture with cutting-edge blockchain and satellite technology.
    """)
    
    # ✅ Navigation button (uses switch_page)
    if st.button("🚀 Go to Dashboard", use_container_width=True):
        switch_page("👤_Dashboard")

with col2:
    st.success("""
    ### ✨ Features
    - 🛰️ Satellite Verification
    - ⛓️ Blockchain Recording
    - 💰 Fair Pricing
    - 🌍 Multilingual
    """)

st.markdown("---")

# --------------------------------------------------
# 🎯 KEY FEATURES
# --------------------------------------------------
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

# --------------------------------------------------
# 📊 IMPACT SECTION
# --------------------------------------------------
st.markdown("## 📊 Impact")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Farmers", "500K+", "+25%")
col2.metric("Claims", "125K", "+40%")
col3.metric("Fraud Prevented", "₹9Cr", "99%")
col4.metric("Avg Payout", "24 hrs", "-95%")

st.markdown("---")

# --------------------------------------------------
# 🌐 LANGUAGE DISPLAY
# --------------------------------------------------
languages = {
    'en': '🇬🇧 English',
    'hi': '🇮🇳 हिन्दी',
    'kn': '🌾 ಕನ್ನಡ',
    'te': '🏞️ తెలుగు'
}

st.info(f"🌐 **Language:** {languages[st.session_state.language]}")
