import streamlit as st
from datetime import datetime
from catalog import PRODUCTS

st.set_page_config("OmniRetail IQ", layout="wide")

# ---------------- STYLE ----------------
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
.sidebar-section { margin-bottom: 25px; }
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION ----------------
if "records" not in st.session_state:
    st.session_state.records = []

# ---------------- SIDEBAR ----------------
st.sidebar.title("🧾 Retail Control Panel")

# --- CUSTOMER ENTRY ---
st.sidebar.markdown("### 👤 Add Purchase")

with st.sidebar.form("purchase_form"):
    customer_name = st.text_input("Customer Name")

    product_name = st.selectbox(
        "Product Purchased",
        [p["name"] for p in PRODUCTS]
    )

    quantity = st.number_input("Quantity", 1, 10, 1)
    payment_mode = st.selectbox("Payment Mode", ["Cash", "UPI", "Card"])

    save = st.form_submit_button("Save Purchase")

if save:
    product = next(p for p in PRODUCTS if p["name"] == product_name)
    total = product["price"] * quantity

    st.session_state.records.append({
        "customer": customer_name,
        "product": product["name"],
        "category": product["category"],
        "price": product["price"],
        "quantity": quantity,
        "payment": payment_mode,
        "total": total,
        "time": datetime.now().strftime("%d-%m-%Y %H:%M")
    })

    st.sidebar.success("Purchase saved")

# --- AI INSIGHTS ---
st.sidebar.markdown("---")
st.sidebar.markdown("### 🧠 AI Insights")

if st.session_state.records:
    total_sales = sum(r["total"] for r in st.session_state.records)
    most_common_category = max(
        set(r["category"] for r in st.session_state.records),
        key=lambda c: sum(1 for r in st.session_state.records if r["category"] == c)
    )

    st.sidebar.info(f"💰 Total Revenue: ₹ {total_sales}")
    st.sidebar.success(f"🔥 Top Category: {most_common_category}")
    st.sidebar.warning("📈 Festive & traditional wear drive higher value sales")
else:
    st.sidebar.info("No data yet to generate insights")

# ---------------- MAIN CONTENT ----------------
st.title("🛍️ OmniRetail IQ – Product Catalog")

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
st.markdown("## 📋 Stored Purchase Records")

if not st.session_state.records:
    st.info("No purchases recorded yet.")
else:
    for r in st.session_state.records:
        st.markdown("----")
        st.write(f"👤 **Customer:** {r['customer']}")
        st.write(f"🛍️ **Product:** {r['product']} ({r['category']})")
        st.write(f"🔢 **Quantity:** {r['quantity']}")
        st.write(f"💳 **Payment Mode:** {r['payment']}")
        st.write(f"🕒 **Date:** {r['time']}")
        st.write(f"💰 **Total Paid:** ₹ {r['total']}")
