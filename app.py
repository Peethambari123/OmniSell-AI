import streamlit as st
from data.catalog import PRODUCTS

st.set_page_config(
    page_title="OmniSell AI – Smart Retail",
    layout="wide"
)

# ---------------- SIDEBAR ----------------
st.sidebar.title("🛍️ OmniSell AI")

categories = sorted(set(p["category"] for p in PRODUCTS))
occasions = sorted(set(p["occasion"] for p in PRODUCTS))

st.sidebar.subheader("Filter Products")
selected_category = st.sidebar.selectbox("Category", ["All"] + categories)
selected_occasion = st.sidebar.selectbox("Occasion", ["All"] + occasions)

st.sidebar.markdown("---")
st.sidebar.markdown("""
### Why OmniSell AI?
✔ Personalized retail experience  
✔ Omnichannel ready design  
✔ Loyalty driven shopping  
✔ Smart recommendations  
""")

st.sidebar.markdown("📍 **Stores:** Bangalore | Mumbai | Hyderabad")

# ---------------- HEADER ----------------
st.title("🛍️ OmniSell AI – Smart Retail Experience")
st.caption("A modern, AI-inspired retail platform inspired by real shopping websites")

st.divider()

# ---------------- CUSTOMER INTEREST ----------------
st.subheader("🎯 Tell Us Your Interest")

col1, col2 = st.columns(2)

with col1:
    interest_category = st.selectbox("What are you looking for?", categories)
with col2:
    interest_occasion = st.selectbox("For which occasion?", occasions)

if st.button("✨ Show Matching Products"):
    st.subheader("✨ Products Matching Your Interest")

    matches = [
        p for p in PRODUCTS
        if p["category"] == interest_category
        and p["occasion"] == interest_occasion
    ]

    if not matches:
        st.warning("No products found. Try different options.")
    else:
        cols = st.columns(4)
        for i, item in enumerate(matches):
            with cols[i % 4]:
                st.image(item["image"], use_column_width=True)
                st.markdown(f"**{item['name']}**")
                st.markdown(f"₹{item['price']}")
                st.caption(f"{item['category']} | {item['occasion']}")

st.divider()

# ---------------- FULL CATALOG ----------------
st.subheader("🛒 Explore Full Collection")

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

for i, product in enumerate(filtered_products):
    with cols[i % 4]:
        st.image(product["image"], use_column_width=True)
        st.markdown(f"**{product['name']}**")
        st.markdown(f"₹{product['price']}")
        st.caption(f"{product['category']} | {product['occasion']}")
