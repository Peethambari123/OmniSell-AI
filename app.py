import streamlit as st
from agents.recommendation_agent import RecommendationAgent
from data.catalog import PRODUCTS

st.set_page_config(
    page_title="OmniSell AI – Agentic Retail",
    layout="wide"
)

# ---------------- SIDEBAR ----------------
st.sidebar.title("🛍️ OmniSell AI")

categories = sorted(set(p["category"] for p in PRODUCTS))
occasions = ["Casual", "Formal", "Festive"]

st.sidebar.subheader("Browse Categories")
selected_category = st.sidebar.selectbox(
    "Category",
    ["All"] + categories
)

st.sidebar.subheader("Occasion")
selected_occasion = st.sidebar.selectbox(
    "Occasion",
    ["All"] + occasions
)

st.sidebar.markdown("---")
st.sidebar.markdown("""
### Why Shop With Us?
✔ AI-powered personalization  
✔ Omnichannel experience  
✔ Loyalty benefits  
✔ In-store & online support  
""")

# ---------------- HEADER ----------------
st.title("🛍️ Agentic AI Conversational Retail Assistant")
st.caption("A complete AI-powered shopping experience like real retail websites")

st.divider()

# ---------------- CUSTOMER INTEREST ----------------
st.subheader("🎯 Personalize Your Shopping")

col1, col2 = st.columns(2)

with col1:
    pref_category = st.selectbox("Interested Category", categories)

with col2:
    pref_occasion = st.selectbox("Occasion", occasions)

if st.button("✨ Get AI Recommendations"):
    agent = RecommendationAgent()
    prefs = {
        "category": pref_category,
        "occasion": pref_occasion
    }

    recommendations = agent.run(prefs)

    st.subheader("✨ Recommended For You")

    if not recommendations:
        st.warning("No matching products found.")
    else:
        cols = st.columns(4)
        for idx, item in enumerate(recommendations):
            with cols[idx % 4]:
                st.image(item["image"], use_column_width=True)
                st.markdown(f"**{item['name']}**")
                st.markdown(f"₹{item['price']}")
                st.caption(f"{item['category']} | {item['occasion']}")

st.divider()

# ---------------- FULL CATALOG ----------------
st.subheader("🛒 Explore Our Collection")

filtered_products = PRODUCTS

if selected_category != "All":
    filtered_products = [
        p for p in filtered_products if p["category"] == selected_category
    ]

if selected_occasion != "All":
    filtered_products = [
        p for p in filtered_products if p["occasion"] == selected_occasion
    ]

cols = st.columns(4)

for idx, product in enumerate(filtered_products):
    with cols[idx % 4]:
        st.image(product["image"], use_column_width=True)
        st.markdown(f"**{product['name']}**")
        st.markdown(f"₹{product['price']}")
        st.caption(f"{product['category']} | {product['occasion']}")
