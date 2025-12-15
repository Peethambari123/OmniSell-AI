# app.py
import streamlit as st
import pandas as pd
from datetime import datetime
from catalog import PRODUCTS

st.set_page_config("OmniRetail IQ", layout="wide")

# ------------------- FULL COLOR STYLES -------------------
st.markdown("""
<style>
body { background: linear-gradient(135deg, #ffecd2, #fcb69f, #ff6f91, #845ec2); }

h1, h2, h3, h4 { font-family: 'Comic Sans MS', cursive; color: #ffe066; }

.price { color: #ff6f61; font-weight: bold; font-size: 1.2em; }

.card {
    background: linear-gradient(145deg, #ff9a9e, #fad0c4);
    border-radius: 20px;
    padding: 15px;
    margin-bottom: 20px;
    box-shadow: 5px 5px 15px #f7b2b7, -5px -5px 15px #ffdac1;
}

.button-buy {
    background: linear-gradient(45deg, #ff6f61, #ff9472);
    color: #ffffff;
    font-weight: bold;
    border-radius: 12px;
    padding: 10px 15px;
    margin-top: 10px;
    text-align: center;
}

.button-wish {
    background: linear-gradient(45deg, #845ec2, #d65db1);
    color: #ffffff;
    font-weight: bold;
    border-radius: 12px;
    padding: 10px 15px;
    margin-top: 5px;
}

.stButton>button {
    background: linear-gradient(45deg, #ff6f61, #ff9472);
    color: #ffffff;
    font-weight: bold;
    border-radius: 12px;
}

.dataframe tbody tr:nth-child(even) { background-color: #ffb3ba; }
.dataframe tbody tr:nth-child(odd) { background-color: #ffdfba; }
.dataframe thead { background-color: #ffdfba; color: #6a0572; }
</style>
""", unsafe_allow_html=True)

# ------------------- SESSION STATE -------------------
for key in ["records", "cart", "wishlist"]:
    if key not in st.session_state:
        st.session_state[key] = []

# ------------------- SIDEBAR -------------------
st.sidebar.markdown("<h2 style='color:#ffd700'>🎨 Retail Dashboard</h2>", unsafe_allow_html=True)
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
    st.markdown("<h1 style='text-align:center; color:#ffde59'>🏬 Product Store</h1>", unsafe_allow_html=True)
    cols = st.columns(3)
    for i, p in enumerate(PRODUCTS):
        with cols[i % 3]:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.image(p["image"], use_column_width=True)
            st.markdown(f"<h3 style='color:#ff6f61'>{p['name']}</h3>", unsafe_allow_html=True)
            st.markdown(f"<b>Category:</b> <span style='color:#845ec2'>{p['category']}</span>", unsafe_allow_html=True)
            st.markdown(f"<div class='price'>₹ {p['price']}</div>", unsafe_allow_html=True)

            if st.button("🛒 Add to Cart", key=f"cart_{i}"):
                existing = next((item for item in st.session_state.cart if item["name"] == p["name"]), None)
                if existing:
                    existing["Quantity"] += 1
                    st.success(f"Quantity of {p['name']} increased in cart")
                else:
                    item_copy = p.copy()
                    item_copy["Quantity"] = 1
                    st.session_state.cart.append(item_copy)
                    st.success(f"{p['name']} added to cart")

            if st.button("💖 Add to Wishlist", key=f"wish_{i}"):
                if p not in st.session_state.wishlist:
                    st.session_state.wishlist.append(p)
                    st.success(f"{p['name']} added to wishlist")
                else:
                    st.info(f"{p['name']} is already in wishlist")
            st.markdown("</div>", unsafe_allow_html=True)

# ==================== CART PAGE ====================
elif page == "🛒 Cart":
    st.markdown("<h1 style='text-align:center; color:#ff6f61'>🛒 Cart Items</h1>", unsafe_allow_html=True)
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
    st.markdown("<h1 style='text-align:center; color:#845ec2'>💖 Wishlist Items</h1>", unsafe_allow_html=True)
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
    st.markdown("<h1 style='text-align:center; color:#ffd700'>📊 Sales Records & Insights</h1>", unsafe_allow_html=True)
    if not st.session_state.records:
        st.info("No purchase records available yet 📁")
    else:
        df = pd.DataFrame(st.session_state.records)
        st.dataframe(df, use_container_width=True)

        st.markdown("### 📈 Insights")
        st.markdown(f"<span style='color:#ff6f61; font-weight:bold'>Total Revenue:</span> 💰 ₹ {df['Total Amount'].sum()}", unsafe_allow_html=True)
        st.markdown(f"<span style='color:#845ec2; font-weight:bold'>Average Rating:</span> ⭐ {round(df['Rating'].mean(),2)}", unsafe_allow_html=True)
        st.markdown(f"<span style='color:#ffde59; font-weight:bold'>Top Category:</span> 🏷️ {df['Category'].mode()[0]}", unsafe_allow_html=True)
