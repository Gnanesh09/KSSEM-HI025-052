import streamlit as st
from utils.api import api_client

def show_sidebar():
    with st.sidebar:
        st.markdown("## ⚙️ Settings")
        
        lang = st.selectbox(
            "🌐 Language",
            options=['en', 'hi', 'kn', 'te'],
            format_func=lambda x: {'en': '🇬🇧 English', 'hi': '🇮🇳 हिन्दी', 'kn': '🌾 ಕನ್ನಡ', 'te': '🏞️ తెలుగు'}[x]
        )
        
        st.session_state.language = lang
        
        st.markdown("---")
        st.markdown("### 📊 System Status")
        
        try:
            stats = api_client.get_blockchain_stats()
            st.success("✅ Backend: Connected")
            st.metric("Blocks", stats.get('total_blocks', 0))
            st.metric("Transactions", stats.get('total_transactions', 0))
        except:
            st.error("❌ Backend: Disconnected")
        
        st.markdown("---")
        st.markdown("### 📱 Demo Info")
        st.info("**Farmer ID:** FAR-0001\n\n**Test Mode:** Enabled")
