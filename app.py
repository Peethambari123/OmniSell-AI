import streamlit as st
from data.catalog import PRODUCTS

# -------- FORCE LIGHT UI --------
st.set_page_config(
    page_title="OmniRetail IQ",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
body {
    background-color: #ffffff;
}
.stApp {
    background-color: #ffffff;
}
h1, h2, h3 {
    color: #1f2937;
}
.css-1d391kg {
    background-color: #f9fafb;
}
</style>
""", unsafe_allow_html=True)

# -------- SESSION STORAGE --------
if "customers" not in st.session_state:
    st.session_state.customers = []

if "sales" not in st.session_state:
    st.session_state.sales = []

# -------- SIDEBAR --------
st.sidebar.title("🛍️ OmniRetail IQ")
page = st.sidebar.radio(
    "Navigate",
    ["🛒 Store", "👤 Add Customer", "📊 Customer Dashboard", "🧠 AI Insights"]
)

# -------- STORE --------
if page == "🛒 Store":
    st.title("🛒 Smart Fashion Store")

    genders = sorted(set(p["gender"] for p in PRODUCTS))
    categories = sorted(set(p["category"] for p in PRODUCTS))
    occasions = sorted(set(p["occasion"] for p in PRODUCTS))

    col1, col2, col3 = st.columns(3)
    with col1:
        g = st.selectbox("Gender", ["All"] + genders)
    with col2:
        c = st.selectbox("Category", ["All"] + categories)
    with col3:
        o = st.selectbox("Occasion", ["All"] + occasions)

    filtered = PRODUCTS
    if g != "All":
        filtered = [p for p in filtered if p["gender"] == g]
    if c != "All":
        filtered = [p for p in filtered if p["category"] == c]
    if o != "All":
        filtered = [p for p in filtered if p["occasion"] == o]

    cols = st.columns(4)
    for i, p in enumerate(filtered):
        with cols[i % 4]:
            st.image(p["image"], use_column_width=True)
            st.markdown(f"**{p['name']}**")
            st.markdown(f"₹{p['price']}")
            if st.button("🛒 Sell", key=p["id"]):
                st.session_state.sales.append(p)
                st.success("Added to sales")

# -------- ADD CUSTOMER --------
elif page == "👤 Add Customer":
    st.title("👤 Customer Registration")

    with st.form("customer_form"):
        name = st.text_input("Customer Name")
        age = st.number_input("Age", 1, 100)
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        prefs = st.multiselect(
            "Interested Categories",
            sorted(set(p["category"] for p in PRODUCTS))
        )
        submit = st.form_submit_button("Save Customer")

    if submit:
        st.session_state.customers.append({
            "name": name,
            "age": age,
            "gender": gender,
            "preferences": prefs,
            "purchases": []
        })
        st.success("Customer saved successfully")

# -------- CUSTOMER DASHBOARD --------
elif page == "📊 Customer Dashboard":
    st.title("📊 Customer Insights")

    for cust in st.session_state.customers:
        st.subheader(cust["name"])
        st.caption(f"Age: {cust['age']} | Gender: {cust['gender']}")
        st.write("Preferences:", ", ".join(cust["preferences"]))

# -------- AI INSIGHTS --------
else:
    st.title("🧠 AI Retail Insights")

    revenue = sum(p["price"] for p in st.session_state.sales)
    st.metric("Total Revenue", f"₹{revenue}")
    st.metric("Products Sold", len(st.session_state.sales))

    st.info("""
    🔍 **AI Observations**
    - Festive & traditional wear has higher ticket size
    - Customers often buy within preferred categories
    - Kids & ethnic wear shows seasonal spikes
    - Bundling accessories can increase AOV
    """)
