import streamlit as st
from data.catalog import PRODUCTS

st.set_page_config(
    page_title="OmniRetail IQ",
    layout="wide"
)

# ---------------- LIGHT UI ----------------
st.markdown("""
<style>
.stApp {
    background-color: #f9fafb;
}
.product-card {
    background: white;
    padding: 14px;
    border-radius: 14px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.08);
    margin-bottom: 20px;
}
.product-title {
    font-weight: 600;
    font-size: 16px;
}
.price {
    color: #2563eb;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION STORAGE ----------------
if "customers" not in st.session_state:
    st.session_state.customers = []

if "sales" not in st.session_state:
    st.session_state.sales = []

# ---------------- SIDEBAR ----------------
st.sidebar.title("🛍️ OmniRetail IQ")
page = st.sidebar.radio(
    "Navigation",
    ["🛒 Store", "👤 Add Customer", "📊 Customers", "🧠 AI Insights"]
)

# ---------------- STORE ----------------
if page == "🛒 Store":
    st.title("🛒 Fashion Store")

    categories = sorted(set(p["category"] for p in PRODUCTS))
    occasions = sorted(set(p["occasion"] for p in PRODUCTS))

    c1, c2 = st.columns(2)
    with c1:
        cat = st.selectbox("Category", ["All"] + categories)
    with c2:
        occ = st.selectbox("Occasion", ["All"] + occasions)

    filtered = PRODUCTS
    if cat != "All":
        filtered = [p for p in filtered if p["category"] == cat]
    if occ != "All":
        filtered = [p for p in filtered if p["occasion"] == occ]

    cols = st.columns(4)
    for i, p in enumerate(filtered):
        with cols[i % 4]:
            st.markdown("<div class='product-card'>", unsafe_allow_html=True)
            st.image(p["image"], use_column_width=True)
            st.markdown(f"<div class='product-title'>{p['name']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='price'>₹{p['price']}</div>", unsafe_allow_html=True)
            if st.button("Sell", key=p["id"]):
                st.session_state.sales.append(p)
            st.markdown("</div>", unsafe_allow_html=True)

# ---------------- ADD CUSTOMER ----------------
elif page == "👤 Add Customer":
    st.title("👤 Add Customer")

    with st.form("customer_form"):
        name = st.text_input("Name")
        age = st.number_input("Age", 1, 100)
        submit = st.form_submit_button("Save")

    if submit:
        st.session_state.customers.append({
            "name": name,
            "age": age,
            "purchases": []
        })
        st.success("Customer added")

# ---------------- CUSTOMERS ----------------
elif page == "📊 Customers":
    st.title("📊 Customer Dashboard")

    for c in st.session_state.customers:
        st.subheader(c["name"])
        st.caption(f"Age: {c['age']}")
        spent = sum(p["price"] for p in st.session_state.sales)
        st.success(f"Total Spent: ₹{spent}")

# ---------------- AI INSIGHTS ----------------
else:
    st.title("🧠 AI Retail Insights")

    revenue = sum(p["price"] for p in st.session_state.sales)
    total_items = len(st.session_state.sales)

    st.metric("Total Revenue", f"₹{revenue}")
    st.metric("Items Sold", total_items)

    if total_items > 0:
        top_cat = max(
            set(p["category"] for p in st.session_state.sales),
            key=lambda x: sum(1 for p in st.session_state.sales if p["category"] == x)
        )
        st.success(f"🔥 Top Category: {top_cat}")

    st.info("""
    AI Observations:
    • Traditional & festive wear generate higher revenue  
    • Customers repeat purchases within same category  
    • Bundling accessories can increase AOV  
    • Kids wear shows seasonal demand spikes
    """)
