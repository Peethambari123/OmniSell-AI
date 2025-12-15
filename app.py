import streamlit as st
from datetime import datetime
from catalog import PRODUCTS

st.set_page_config("OmniRetail IQ", layout="wide")

# ---------------- UI STYLE ----------------
st.markdown("""
<style>
body { background-color: #f6f8fc; }
.card {
    background: white;
    padding: 15px;
    border-radius: 15px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}
.price { color: #2563eb; font-weight: bold; }
.section-title { font-size: 20px; font-weight: 600; }
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION STORAGE ----------------
if "records" not in st.session_state:
    st.session_state.records = []

# ---------------- SIDEBAR (MANUAL ENTRY) ----------------
st.sidebar.title("🧾 Customer Purchase Entry")

with st.sidebar.form("customer_form"):
    customer_name = st.text_input("Customer Name")
    phone = st.text_input("Phone Number")

    product_name = st.selectbox(
        "Product Purchased",
        [p["name"] for p in PRODUCTS]
    )

    quantity = st.number_input("Quantity", 1, 10, 1)
    payment_mode = st.selectbox("Payment Mode", ["Cash", "UPI", "Card"])

    submit = st.form_submit_button("Save Record")

if submit:
    product = next(p for p in PRODUCTS if p["name"] == product_name)
    total = product["price"] * quantity

    st.session_state.records.append({
        "customer": customer_name,
        "phone": phone,
        "product": product["name"],
        "category": product["category"],
        "price": product["price"],
        "quantity": quantity,
        "payment": payment_mode,
        "total": total,
        "time": datetime.now().strftime("%d-%m-%Y %H:%M")
    })
    st.sidebar.success("✅ Purchase Stored")

# ---------------- MAIN PAGE ----------------
st.title("🛍️ OmniRetail IQ – Store Overview")

st.markdown("### 🧵 Available Products")
cols = st.columns(3)

for i, p in enumerate(PRODUCTS):
    with cols[i % 3]:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.image(p["image"], use_column_width=True)
        st.subheader(p["name"])
        st.write(f"Category: {p['category']}")
        st.markdown(f"<div class='price'>₹ {p['price']}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")
st.markdown("### 📋 Customer Purchase Records")

if not st.session_state.records:
    st.info("No purchases recorded yet.")
else:
    total_revenue = 0
    for r in st.session_state.records:
        st.markdown("----")
        st.write(f"👤 **Customer:** {r['customer']} ({r['phone']})")
        st.write(f"🛍️ **Product:** {r['product']} ({r['category']})")
        st.write(f"🔢 **Quantity:** {r['quantity']}")
        st.write(f"💳 **Payment:** {r['payment']}")
        st.write(f"🕒 **Purchased On:** {r['time']}")
        st.write(f"💰 **Total Paid:** ₹ {r['total']}")
        total_revenue += r["total"]

    st.success(f"💵 Total Revenue: ₹ {total_revenue}")
