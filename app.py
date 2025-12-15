import streamlit as st
from datetime import datetime
from catalog import PRODUCTS

st.set_page_config("OmniRetail IQ", layout="wide")

# ---------- CLEAN IMAGE-FIRST UI ----------
st.markdown("""
<style>
body { background-color: #f6f8fc; }
img { border-radius: 12px; }
.price { font-weight: 600; color: #2563eb; }
</style>
""", unsafe_allow_html=True)

# ---------- SESSION ----------
for key in ["records", "cart", "wishlist"]:
    if key not in st.session_state:
        st.session_state[key] = []

# ---------- SIDEBAR ----------
st.sidebar.title("Retail Control Panel")
page = st.sidebar.radio("Navigate", ["Store", "Cart", "Wishlist"])

# ---------- PURCHASE ENTRY ----------
st.sidebar.subheader("Save Customer Purchase")

with st.sidebar.form("purchase"):
    customer = st.text_input("Customer Name")
    product_name = st.selectbox("Product", [p["name"] for p in PRODUCTS])
    qty = st.number_input("Quantity", 1, 10, 1)
    payment = st.selectbox("Payment Mode", ["Cash", "UPI", "Card"])
    rating = st.slider("Rating", 1, 5, 3)
    feedback = st.text_area("Feedback")
    save = st.form_submit_button("Save")

if save:
    p = next(x for x in PRODUCTS if x["name"] == product_name)
    st.session_state.records.append({
        "customer": customer,
        "product": p["name"],
        "category": p["category"],
        "qty": qty,
        "payment": payment,
        "rating": rating,
        "feedback": feedback,
        "total": p["price"] * qty,
        "time": datetime.now().strftime("%d-%m-%Y %H:%M")
    })
    st.sidebar.success("Saved")

# ---------- AI INSIGHTS ----------
st.sidebar.markdown("---")
st.sidebar.subheader("AI Insights")

if st.session_state.records:
    revenue = sum(r["total"] for r in st.session_state.records)
    avg_rating = round(sum(r["rating"] for r in st.session_state.records) / len(st.session_state.records), 2)
    st.sidebar.write(f"Total Revenue: ₹{revenue}")
    st.sidebar.write(f"Average Rating: {avg_rating}/5")
    st.sidebar.write("High-rated items should be promoted")
else:
    st.sidebar.write("No data yet")

# ================= STORE =================
if page == "Store":
    st.title("Product Store")

    cols = st.columns(3)
    for i, p in enumerate(PRODUCTS):
        with cols[i % 3]:
            st.image(p["image"], use_column_width=True)
            st.subheader(p["name"])
            st.write(p["category"])
            st.markdown(f"<div class='price'>₹ {p['price']}</div>", unsafe_allow_html=True)

            if st.button("Add to Cart", key=f"cart_{i}"):
                st.session_state.cart.append(p)

            if st.button("Add to Wishlist", key=f"wish_{i}"):
                st.session_state.wishlist.append(p)

# ================= CART =================
elif page == "Cart":
    st.title("Your Cart")

    if not st.session_state.cart:
        st.info("Cart is empty")
    else:
        total = 0
        for p in st.session_state.cart:
            st.write(f"{p['name']} - ₹{p['price']}")
            total += p["price"]
        st.success(f"Total Cart Value: ₹ {total}")

# ================= WISHLIST =================
elif page == "Wishlist":
    st.title("Your Wishlist")

    if not st.session_state.wishlist:
        st.info("Wishlist is empty")
    else:
        for p in st.session_state.wishlist:
            st.write(f"{p['name']} - ₹{p['price']}")

# ---------- STORED DATA ----------
st.markdown("---")
st.subheader("Stored Purchase Records")

for r in st.session_state.records:
    st.write(
        f"{r['customer']} | {r['product']} | {r['qty']} | "
        f"{r['payment']} | ₹{r['total']} | Rating {r['rating']}"
    )
