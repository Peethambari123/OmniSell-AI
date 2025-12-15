import streamlit as st
from catalog import PRODUCTS

st.set_page_config("OmniRetail IQ", layout="wide")

st.markdown("""
<style>
body { background-color: #f5f7fb; }
.card {
    background: white;
    padding: 15px;
    border-radius: 15px;
    box-shadow: 0 6px 15px rgba(0,0,0,0.08);
}
.price { color: #2563eb; font-weight: 600; }
</style>
""", unsafe_allow_html=True)

st.title("🛍️ OmniRetail IQ – Smart Fashion Store")

categories = sorted(set(p["category"] for p in PRODUCTS))
selected = st.selectbox("Filter by Category", ["All"] + categories)

filtered = PRODUCTS if selected == "All" else [
    p for p in PRODUCTS if p["category"] == selected
]

cols = st.columns(3)
for i, p in enumerate(filtered):
    with cols[i % 3]:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.image(p["image"], use_column_width=True)
        st.subheader(p["name"])
        st.markdown(f"<div class='price'>₹ {p['price']}</div>", unsafe_allow_html=True)
        st.button("Add to Cart", key=p["name"])
        st.markdown("</div>", unsafe_allow_html=True)
