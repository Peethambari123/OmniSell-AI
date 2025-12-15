import streamlit as st
from agents.recommendation_agent import RecommendationAgent
from agents.inventory_agent import InventoryAgent
from agents.loyalty_agent import LoyaltyAgent

st.set_page_config(page_title="Agentic Retail AI", layout="centered")
st.title("🛍️ Agentic AI Conversational Retail Assistant")

# ---------------- Customer Profile ----------------
st.header("👤 Customer Profile")

with st.form("customer_form"):
    name = st.text_input("Customer Name")
    age = st.number_input("Age", min_value=15, max_value=80)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])

    category = st.selectbox("Interested Category", ["Shirts", "Pants", "Jeans"])
    occasion = st.selectbox("Occasion", ["Casual", "Formal", "Festive"])
    budget = st.selectbox("Budget", ["Under 2000", "2000-3000", "Above 3000"])

    submitted = st.form_submit_button("Get Recommendations")

# ---------------- Agentic Processing ----------------
if submitted:
    customer_context = {
        "name": name,
        "age": age,
        "gender": gender,
        "category": category,
        "occasion": occasion,
        "budget": budget
    }

    reco_agent = RecommendationAgent()
    inventory_agent = InventoryAgent()
    loyalty_agent = LoyaltyAgent()

    reco = reco_agent.run(customer_context)
    inv = inventory_agent.run(reco)
    final = loyalty_agent.run(inv)

    # ---------------- Output ----------------
    st.success("🎯 Personalized Recommendations Ready!")

    for item in final["cart"]:
        st.markdown(f"""
        ### 👕 {item['name']}
        💰 Price: ₹{item['price']}  
        📦 Availability: {inv['availability']}
        """)

    st.info(final["message"])
