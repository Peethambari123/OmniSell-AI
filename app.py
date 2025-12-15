# app.py
import streamlit as st
import pandas as pd
from datetime import datetime
from catalog import PRODUCTS

st.set_page_config("OmniRetail IQ", layout="wide")

# ------------------- STYLES -------------------
st.markdown("""
<style>
body { background-color: #f0f8ff; }
h1, h2, h3, h4 { color: #333333; font-family: 'Segoe UI', sans-serif; }
.price { color: #ff4b4b; font-weight: bold; font-size: 1.1em; }
.card {
    background: linear-gradient(145deg, #ffffff, #e0f7fa);
    border-radius: 15px;
    padding: 15px;
    margin-bottom: 20px;
    box-shadow: 5px 5px 15px #b0e0e6, -5px -5px 15px #ffffff;
}
.button-buy {
    background-color: #ff6f61;
    color: white;
    font-weight: bold;
    border-radius: 10px;
    padding: 8px 12px;
    margin-top: 10px;
}
.button-wish {
    background-color: #4caf50;
    color: white;
    font-weight: bold;
    border-radius: 10px;
    padding: 8px 12px;
    margin-top: 5px;
}
</style>
""", unsafe_allow_html=True)

# ------------------- SESSION STATE -------------------
for key in ["records", "cart", "wishlist"]:
    if key not in st.session_state:
        st.session_state[key] = []

# ------------------- SIDEBAR -------------------
st.sidebar.title("🎨 Retail Dashboard Control Panel")
page = st.sidebar.radio("Navigate", ["🏬 Store", "🛒 Cart", "💖 Wishlist", "📊 Records & Insights"])

# ------------------- PURCHASE RECORD FORM -------------------
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
    p = next((x for x in PRODUCTS if x["name"] == product_name), None)
    if p:
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
        st.sidebar.success("✅ Record saved!")

# ==================== STORE PAGE ====================
if page == "🏬 Store":
    st.title("🏬 Product Store")
    cols = st.columns(3)
    for i, p in enumerate(PRODUCTS):
        with cols[i % 3]:
            st.markdown(f"<div class='card'>", unsafe_allow_html=True)
            st.image(p["image"], use_column_width=True)
            st.markdown(f"### {p['name']}")
            st.markdown(f"Category: **{p['category']}**")
            st.markdown(f"<div class='price'>₹ {p['price']}</div>", unsafe_allow_html=True)

            if st.button("🛒 Add to Cart", key=f"cart_{i}", help="Add this product to cart"):
                existing = next((item for item in st.session_state.cart if item["name"] == p["name"]), None)
                if existing:
                    existing["Quantity"] += 1
                    st.success(f"Quantity of {p['name']} increased in cart")
                else:
                    item_copy = p.copy()
                    item_copy["Quantity"] = 1
                    st.session_state.cart.append(item_copy)
                    st.success(f"{p['name']} added to cart")

            if st.button("💖 Add to Wishlist", key=f"wish_{i}", help="Add this product to wishlist"):
                if p not in st.session_state.wishlist:
                    st.session_state.wishlist.append(p)
                    st.success(f"{p['name']} added to wishlist")
                else:
                    st.info(f"{p['name']} is already in wishlist")
            st.markdown("</div>", unsafe_allow_html=True)

# ==================== CART PAGE ====================
elif page == "🛒 Cart":
    st.title("🛒 Cart Items")
    if not st.session_state.cart:
        st.info("Your cart is empty 🛍️")
    else:
        df = pd.DataFrame(st.session_state.cart)
        df["Total"] = df["price"] * df["Quantity"]
        st.dataframe(df[["name", "category", "price", "Quantity", "Total"]], use_container_width=True)
        st.success(f"💰 Grand Total: ₹ {df['Total'].sum()}")

        st.markdown("### Remove Item from Cart")
        for i, item in enumerate(st.session_state.cart):
            if st.button(f"❌ Remove {item['name']}", key=f"remove_cart_{i}"):
                st.session_state.cart.pop(i)
                st.experimental_rerun()

# ==================== WISHLIST PAGE ====================
elif page == "💖 Wishlist":
    st.title("💖 Wishlist Items")
    if not st.session_state.wishlist:
        st.info("Your wishlist is empty ✨")
    else:
        df = pd.DataFrame(st.session_state.wishlist)
        st.dataframe(df[["name", "category", "price"]], use_container_width=True)

        st.markdown("### Remove Item from Wishlist")
        for i, item in enumerate(st.session_state.wishlist):
            if st.button(f"❌ Remove {item['name']}", key=f"remove_wish_{i}"):
                st.session_state.wishlist.pop(i)
                st.experimental_rerun()

# ==================== RECORDS PAGE ====================
elif page == "📊 Records & Insights":
    st.title("📊 Sales Records & Insights")
    if not st.session_state.records:
        st.info("No purchase records available yet 📁")
    else:
        df = pd.DataFrame(st.session_state.records)
        st.dataframe(df, use_container_width=True)

        st.markdown("### 📈 Insights")
        st.markdown(f"**Total Revenue:** 💰 ₹ {df['Total Amount'].sum()}")
        st.markdown(f"**Average Rating:** ⭐ {round(df['Rating'].mean(),2)}")
        st.markdown(f"**Top Category:** 🏷️ {df['Category'].mode()[0]}")
