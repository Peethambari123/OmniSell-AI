import streamlit as st

def init_session():
    if "context" not in st.session_state:
        st.session_state.context = {
            "session_id": "SESSION_001",
            "user_id": "USER_01",
            "channel": "web",
            "cart": [],
            "conversation": []
        }
    return st.session_state.context
