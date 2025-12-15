import streamlit as st
from agents.sales_agent import SalesAgent
from utils.session import init_session

st.set_page_config(page_title="Agentic Retail AI", layout="centered")

# Initialize session
session = init_session()

st.title("🛍️ Agentic AI Conversational Retail Assistant")

# Display conversation
for role, msg in session["conversation"]:
    with st.chat_message(role):
        st.write(msg)

# User input
user_input = st.chat_input("What are you looking for today?")

if user_input:
    sales_agent = SalesAgent()
    reply = sales_agent.handle(user_input, session)
    st.rerun()

