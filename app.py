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
    padding: 16px;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}
.price {
    color: #2563eb;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION STORAGE ----------------
if "records" not in st.session_state:
    st.session_state.records = []

# ---------------- SIDEBAR ----------------
st.sidebar.title("Retail Management Panel")

# --- PURCHASE ENTRY ---
st.sidebar.subheader("Add Customer Purchase")

with st.sidebar.form("purchase_form"):
    customer_name = st.text_input("Customer Name")

    product_name = st.selectbox(
        "Product",
        [p["name"] for p in PRODUCTS]
    )

    quantity = st.number_input("Quantity", 1, 10, 1)
    payment_mode = st.selectbox("Payment Mode", ["Cash", "UPI", "Card"])

    rating = st.slider("Customer Rating", 1, 5, 3)
    feedback = st.text_area("Customer Feedback")

    save = st.form_submit_button("Save")

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
        "rating": rating,
        "feedback": feedback,
        "total": total,
        "time": datetime.now().strftime("%d-%m-%Y %H:%M")
    })

    st.sidebar.success("Purchase and feedback saved")

# --- AI INSIGHTS ---
st.sidebar.markdown("---")
st.sidebar.subheader("AI Insights")

if st.session_state.records:
    total_revenue = sum(r["total"] for r in st.session_state.records)
    avg_rating = round(
        sum(r["rating"] for r in st.session_state.records) / len(st.session_state.records),
        2
    )

    top_category = max(
        set(r["category"] for r in st.session_state.records),
        key=lambda c: sum(1 for r in st.session_state.records if r["category"] == c)
    )

    top_payment = max(
        set(r["payment"] for r in st.session_state.records),
        key=lambda p: sum(1 for r in st.session_state.records if r["payment"] == p)
    )

    st.sidebar.write(f"Total Revenue: ₹ {total_revenue}")
    st.sidebar.write(f"Average Rating: {avg_rating} / 5")
    st.sidebar.write(f"Top Category: {top_category}")
    st.sidebar.write(f"Most Used Payment Mode: {top_payment}")

    st.sidebar.markdown("""
    **Insights Generated**
    - High-rated products should be promoted more
    - Traditional and festive items generate higher revenue
    - Digital payments are increasingly preferred
    """)
else:
    st.sidebar.write("No data available yet")

# ---------------- MAIN PAGE ----------------
st.title("Product Catalog")

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
st.subheader("Stored Purchase & Feedback Records")

if not st.session_state.records:
    st.info("No records stored yet.")
else:
    for r in st.session_state.records:
        st.markdown("----")
        st.write(f"Customer: {r['customer']}")
        st.write(f"Product: {r['product']} ({r['category']})")
        st.write(f"Quantity: {r['quantity']}")
        st.write(f"Payment Mode: {r['payment']}")
        st.write(f"Rating: {r['rating']} / 5")
        st.write(f"Feedback: {r['feedback']}")
        st.write(f"Total Paid: ₹ {r['total']}")
        st.write(f"Date & Time: {r['time']}")
