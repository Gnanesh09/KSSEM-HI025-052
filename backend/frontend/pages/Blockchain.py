import streamlit as st
from utils.api import api_client
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from components.sidebar import show_sidebar

st.set_page_config(page_title="Blockchain", page_icon="⛓️", layout="wide")

show_sidebar()

st.markdown("# ⛓️ Blockchain Explorer")

try:
    stats = api_client.get_blockchain_stats()
    blocks = api_client.get_all_blocks()
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📦 Blocks", stats.get('total_blocks', 0))
    col2.metric("📝 Transactions", stats.get('total_transactions', 0))
    col3.metric("✅ Valid", "Yes" if stats.get('is_valid') else "No")
    col4.metric("⏳ Pending", stats.get('pending', 0))
    
    st.markdown("---")
    st.markdown("## 📋 Blocks")
    
    for block in blocks.get('blocks', [])[::-1]:
        with st.expander(f"Block #{block.get('index')} - {len(block.get('transactions', []))} tx"):
            col1, col2 = st.columns(2)
            with col1:
                st.code(f"Hash: {block.get('hash', '')[:32]}...", language="python")
            with col2:
                st.code(f"Prev: {block.get('previous_hash', '')[:32]}...", language="python")
            
            st.markdown("### Transactions")
            for tx in block.get('transactions', []):
                st.json(tx)

except Exception as e:
    st.error(f"Error: {str(e)}")
