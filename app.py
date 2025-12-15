# app.py
import streamlit as st
import pandas as pd
from datetime import datetime
from catalog import PRODUCTS

st.set_page_config("OmniRetail IQ", layout="wide")

# ------------------- STYLES -------------------
st.markdown("""
<style>
/* ---------- App Background ---------- */
body, .stApp {
    background: linear-gradient(135deg, #f5f7fa, #c3cfe2);
    color: #1e3a8a;
    font-family: 'Segoe UI', sans-serif;
}

/* ---------- Sidebar ---------- */
[data-testid="stSidebar"] {
    background: linear-gradient(135deg, #4facfe, #00f2fe);
    color: #ffffff;
}

/* ---------- Headers ---------- */
h1, h2, h3, h4 { 
    color: #1e3a8a; 
    font-family: 'Segoe UI', sans-serif;
}

/* ---------- Product Cards ---------- */
.stImage > img { 
    border-radius: 20px; 
    box-shadow: 0 6px 15px rgba(0,0,0,0.15);
}

/* Product text styles */
.product-name { color: #0d6efd; font-size: 1.2em; font-weight: bold; }
.product-category { color: #10b981; font-size: 1em; font-style: italic; }
.product-price { color: #f97316; font-weight: bold; font-size: 1.1em; }

/* ---------- Buttons ---------- */
.stButton>button {
    background: linear-gradient(90deg, #facc15, #f59e0b);
    color: #ffffff;
    font-weight: bold;
    border-radius: 12px;
    padding: 8px 14px;
    transition: all 0.3s ease;
}
.stButton>button:hover {
    background: linear-gradient(90deg, #f59e0b, #facc15);
    transform: scale(1.05);
}

/* ---------- Remove / Critical Button ---------- */
.remove-button { color: #ef4444; font-weight: bold; }

/* ---------- Tables ---------- */
.dataframe tbody tr:nth-child(even) { background-color: #e0f2fe; }
.dataframe tbody tr:nth-child(odd) { background-color: #bae6fd; }
.dataframe thead { background-color: #2563eb; color: #ffffff; font-weight: bold; }

/* ---------- Sidebar Inputs ---------- */
.stTextInput>div>input, .stSelectbox>div>div>div>input, .stNumberInput>div>input, .stSlider>div>div>div>input {
    border-radius: 8px;
    border: 1px solid #4facfe;
    padding: 6px;
}

/* ---------- Alerts ---------- */
.stSuccess { border-radius: 12px; padding: 10px 15px; font-weight: bold; background-color: #16a34a; color: #ffffff; }
.stInfo { border-radius: 12px; padding: 10px 15px; font-weight: bold; background-color: #0ea5e9; color: #ffffff; }
.stWarning { border-radius: 12px; padding: 10px 15px; font-weight: bold; background-color: #fbbf24; color: #333333; }
.stError { border-radius: 12px; padding: 10px 15px; font-weight: bold; background-color: #ef4444; color: #ffffff; }

/* Smooth scrollbar for sidebar */
[data-testid="stSidebar"]::-webkit-scrollbar { width: 6px; }
[data-testid="stSidebar"]::-webkit-scrollbar-thumb { background-color: #4facfe; border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

# ------------------- SESSION STATE -------------------
for key in ["records", "cart", "wishlist"]:
    if key not in st.session_state:
        st.session_state[key] = []

# ------------------- SIDEBAR -------------------
st.sidebar.title("Retail Dashboard")
page = st.sidebar.radio("Navigate", ["Store", "Cart", "Wishlist", "Records & Insights"])

# ------------------- PURCHASE RECORD FORM -------------------
st.sidebar.subheader("Add Purchase Record")
with st.sidebar.form("purchase_form"):
    customer = st.text_input("Customer Name")
    product_name = st.selectbox("Product", [p["name"] for p in PRODUCTS])
    quantity = st.number_input("Quantity", 1, 10, 1)
    payment = st.selectbox("Payment Mode", ["Cash", "UPI", "Card"])
    rating = st.slider("Rating", 1, 5, 3)
    feedback = st.text_area("Feedback")
    save = st.form_submit_button("Save Record")

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
        st.sidebar.success(f"Record saved for {customer}!")

# ==================== STORE PAGE ====================
if page == "Store":
    st.markdown("<h1 style='text-align:center'>Product Store</h1>", unsafe_allow_html=True)
    cols = st.columns(3)
    for i, p in enumerate(PRODUCTS):
        with cols[i % 3]:
            st.image(p["image"], use_column_width=True)
            st.markdown(f"<div class='product-name'>{p['name']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='product-category'>{p['category']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='product-price'>₹ {p['price']}</div>", unsafe_allow_html=True)

            if st.button("Add to Cart", key=f"cart_{i}"):
                existing = next((item for item in st.session_state.cart if item["name"] == p["name"]), None)
                if existing:
                    existing["Quantity"] += 1
                    st.success(f"Quantity of {p['name']} increased in cart")
                else:
                    item_copy = p.copy()
                    item_copy["Quantity"] = 1
                    st.session_state.cart.append(item_copy)
                    st.success(f"{p['name']} added to cart")

            if st.button("Add to Wishlist", key=f"wish_{i}"):
                if p not in st.session_state.wishlist:
                    st.session_state.wishlist.append(p)
                    st.success(f"{p['name']} added to wishlist")
                else:
                    st.info(f"{p['name']} is already in wishlist")

# ==================== CART PAGE ====================
elif page == "Cart":
    st.markdown("<h1 style='text-align:center'>Cart Items</h1>", unsafe_allow_html=True)
    if not st.session_state.cart:
        st.info("Cart is empty")
    else:
        df = pd.DataFrame(st.session_state.cart)
        df["Total"] = df["price"] * df["Quantity"]
        st.dataframe(df[["name", "category", "price", "Quantity", "Total"]], use_container_width=True)
        st.success(f"Grand Total: ₹ {df['Total'].sum()}")

        st.markdown("### Remove Item")
        remove_index = None
        for i, item in enumerate(st.session_state.cart):
            if st.button(f"Remove {item['name']}", key=f"remove_cart_{i}"):
                remove_index = i
        if remove_index is not None:
            st.session_state.cart.pop(remove_index)

# ==================== WISHLIST PAGE ====================
elif page == "Wishlist":
    st.markdown("<h1 style='text-align:center'>Wishlist Items</h1>", unsafe_allow_html=True)
    if not st.session_state.wishlist:
        st.info("Wishlist is empty")
    else:
        df = pd.DataFrame(st.session_state.wishlist)
        st.dataframe(df[["name", "category", "price"]], use_container_width=True)

        st.markdown("### Remove Item")
        remove_index = None
        for i, item in enumerate(st.session_state.wishlist):
            if st.button(f"Remove {item['name']}", key=f"remove_wish_{i}"):
                remove_index = i
        if remove_index is not None:
            st.session_state.wishlist.pop(remove_index)

# ==================== RECORDS PAGE ====================
elif page == "Records & Insights":
    st.markdown("<h1 style='text-align:center'>Sales Records & Insights</h1>", unsafe_allow_html=True)
    if not st.session_state.records:
        st.info("No purchase records available")
    else:
        df = pd.DataFrame(st.session_state.records)
        st.dataframe(df, use_container_width=True)

        st.markdown("### Insights")
        st.markdown(f"<b>Total Revenue:</b> ₹ {df['Total Amount'].sum()}", unsafe_allow_html=True)
        st.markdown(f"<b>Average Rating:</b> {round(df['Rating'].mean(),2)}", unsafe_allow_html=True)
        st.markdown(f"<b>Top Category:</b> {df['Category'].mode()[0]}", unsafe_allow_html=True)
