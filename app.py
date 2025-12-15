# app.py
import streamlit as st
import pandas as pd
from datetime import datetime
from catalog import PRODUCTS

st.set_page_config("OmniRetail IQ", layout="wide")

# ---------------- STYLE ----------------
st.markdown("""
<style>
body { background-color: #f6f8fc; }
.price { color: #2563eb; font-weight: 600; }
img { border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION ----------------
for key in ["records", "cart", "wishlist"]:
    if key not in st.session_state:
        st.session_state[key] = []

# ---------------- SIDEBAR ----------------
st.sidebar.title("Retail Control Panel")

page = st.sidebar.radio("Navigate", ["Store", "Cart", "Wishlist", "Records & Insights"])

# ---- Purchase Entry ----
st.sidebar.subheader("Add Purchase Record")
with st.sidebar.form("purchase_form"):
    customer = st.text_input("Customer Name")
    product_name = st.selectbox("Product", [p["name"] for p in PRODUCTS])
    quantity = st.number_input("Quantity", 1, 10, 1)
    payment = st.selectbox("Payment Mode", ["Cash", "UPI", "Card"])
    rating = st.slider("Rating", 1, 5, 3)
    feedback = st.text_area("Feedback")
    save = st.form_submit_button("Save")

if save:
    p = next(x for x in PRODUCTS if x["name"] == product_name)
    st.session_state.records.append({
        "Customer": customer,
        "Product": p["name"],
        "Category": p["category"],
        "Price": p["price"],
        "Quantity": quantity,
        "Total Amount": p["price"] * quantity,
        "Payment Mode": payment,
        "Rating": rating,
        "Feedback": feedback,
        "Date & Time": datetime.now().strftime("%d-%m-%Y %H:%M")
    })
    st.sidebar.success("Record saved")

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

            # Add to Cart
            if st.button("Add to Cart", key=f"cart_{i}"):
                # Check if already in cart
                existing = next((item for item in st.session_state.cart if item["name"] == p["name"]), None)
                if existing:
                    existing["Quantity"] += 1
                    st.success(f"Increased quantity of {p['name']} in cart")
                else:
                    item_copy = p.copy()
                    item_copy["Quantity"] = 1
                    st.session_state.cart.append(item_copy)
                    st.success(f"{p['name']} added to cart")

            # Add to Wishlist
            if st.button("Add to Wishlist", key=f"wish_{i}"):
                if p not in st.session_state.wishlist:
                    st.session_state.wishlist.append(p)
                    st.success(f"{p['name']} added to wishlist")
                else:
                    st.info(f"{p['name']} is already in wishlist")

# ================= CART =================
elif page == "Cart":
    st.title("Cart Items")

    if not st.session_state.cart:
        st.info("Cart is empty")
    else:
        df = pd.DataFrame(st.session_state.cart)
        df["Total"] = df["price"] * df["Quantity"]
        st.dataframe(df[["name", "category", "price", "Quantity", "Total"]], use_container_width=True)
        st.success(f"Grand Total: ₹ {df['Total'].sum()}")

        # Remove items
        st.markdown("### Remove Item")
        for i, item in enumerate(st.session_state.cart):
            if st.button(f"Remove {item['name']}", key=f"remove_cart_{i}"):
                st.session_state.cart.pop(i)
                st.experimental_rerun()

# ================= WISHLIST =================
elif page == "Wishlist":
    st.title("Wishlist Items")

    if not st.session_state.wishlist:
        st.info("Wishlist is empty")
    else:
        df = pd.DataFrame(st.session_state.wishlist)
        st.dataframe(df[["name", "category", "price"]], use_container_width=True)

        # Remove items
        st.markdown("### Remove Item")
        for i, item in enumerate(st.session_state.wishlist):
            if st.button(f"Remove {item['name']}", key=f"remove_wish_{i}"):
                st.session_state.wishlist.pop(i)
                st.experimental_rerun()

# ================= RECORDS & AI INSIGHTS =================
else:
    st.title("Stored Records")

    if not st.session_state.records:
        st.info("No records available")
    else:
        df = pd.DataFrame(st.session_state.records)
        st.dataframe(df, use_container_width=True)

        st.markdown("### AI Insights")
        st.write(f"Total Revenue: ₹ {df['Total Amount'].sum()}")
        st.write(f"Average Rating: {round(df['Rating'].mean(), 2)}")
        st.write(f"Top Category: {df['Category'].mode()[0]}")
