def init_session():
    if "context" not in st.session_state:
        st.session_state.context = {
            "session_id": "SESSION_001",
            "user_id": "USER_01",
            "channel": "web",
            "cart": [],
            "conversation": [],
            "preferences": {
                "category": None,
                "occasion": None,
                "budget": None
            },
            "stage": "START"   # 👈 conversation state
        }
    return st.session_state.context
