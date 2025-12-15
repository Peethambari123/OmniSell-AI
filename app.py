import streamlit as st
from data.catalog import PRODUCTS

st.set_page_config(page_title="OmniRetail IQ", layout="wide")

# ---------------- SESSION STORAGE ----------------
if "customers" not in st.session_state:
    st.session_state.customers = []

if "sales" not in st.session_state:
    st.session_state.sales = []

# ---------------- SIDEBAR ----------------
st.sidebar.title("🛍️ OmniRetail IQ")
page = st.sidebar.radio(
    "Navigation",
    ["🛒 Store", "👤 Add Customer", "📊 Customer Dashboard", "🧠 AI Insights"]
)

# ---------------- STORE PAGE ----------------
if page == "🛒 Store":
    st.title("🛒 Smart Retail Store")

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
            if st.button("Sell", key=p["id"]):
                st.session_state.sales.append(p)
                st.success("Added to sales")

# ---------------- ADD CUSTOMER ----------------
elif page == "👤 Add Customer":
    st.title("👤 Add / Update Customer")

    with st.form("customer_form"):
        name = st.text_input("Customer Name")
        age = st.number_input("Age", 1, 100)
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        preferences = st.multiselect(
            "Interested Categories",
            sorted(set(p["category"] for p in PRODUCTS))
        )
        submitted = st.form_submit_button("Save Customer")

    if submitted:
        st.session_state.customers.append({
            "name": name,
            "age": age,
            "gender": gender,
            "preferences": preferences,
            "purchases": []
        })
        st.success("Customer saved successfully")

# ---------------- CUSTOMER DASHBOARD ----------------
elif page == "📊 Customer Dashboard":
    st.title("📊 Customer Dashboard")

    for cust in st.session_state.customers:
        st.subheader(cust["name"])
        st.caption(f"Age: {cust['age']} | Gender: {cust['gender']}")
        st.write("Preferences:", ", ".join(cust["preferences"]))

        spent = sum(p["price"] for p in cust.get("purchases", []))
        st.success(f"Total Spent: ₹{spent}")

# ---------------- AI INSIGHTS ----------------
else:
    st.title("🧠 AI Retail Insights")

    total_sales = len(st.session_state.sales)
    revenue = sum(p["price"] for p in st.session_state.sales)

    st.metric("Total Products Sold", total_sales)
    st.metric("Total Revenue", f"₹{revenue}")

    if st.session_state.sales:
        top_category = max(
            set(p["category"] for p in st.session_state.sales),
            key=lambda x: sum(1 for p in st.session_state.sales if p["category"] == x)
        )
        st.success(f"🔥 Most Sold Category: {top_category}")

    st.info("""
    **AI Insight Summary**
    - Customers prefer casual & festive wear
    - Ethnic products have higher average value
    - Repeat purchases likely in same category
    - Kids & festive wear peaks seasonally
    """)
