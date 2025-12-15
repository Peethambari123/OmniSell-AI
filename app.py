# app.py
import streamlit as st
import pandas as pd
from datetime import datetime
from catalog import PRODUCTS

# ——————— Page Config ———————
st.set_page_config("OmniRetail IQ", layout="wide")

# ——————— Custom Styles ———————
st.markdown("""
<style>
body { background-color: #f6f8fc; }
.price { color: #2563eb; font-weight: 600; }
img { border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

# ——————— Session Setup ———————
for key in ["records", "cart", "wishlist", "gemini_key"]:
    if key not in st.session_state:
        st.session_state[key] = []

# ——————— Sidebar ———————
st.sidebar.title("Retail Control Panel")

page = st.sidebar.radio(
    "Navigate",
    ["Store", "Cart", "Wishlist", "Records & Insights", "AI Assistant"]
)

# ——————— Gemini API Key Input ———————
st.sidebar.subheader("Gemini API Key (for AI Assistant)")
api_key_input = st.sidebar.text_input(
    "Enter your Gemini API Key",
    type="password",
    key="gemini_key"
)
if api_key_input:
    st.session_state.gemini_key = api_key_input

# ——————— Add Purchase Record ———————
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
        st.sidebar.success("Record saved")

# ——————— Store ———————
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
                existing = next((item for item in st.session_state.cart if item["name"] == p["name"]), None)
                if existing:
                    existing["Quantity"] += 1
                    st.success(f"Increased quantity of {p['name']} in cart")
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

# ——————— Cart ———————
elif page == "Cart":
    st.title("Cart Items")
    if not st.session_state.cart:
        st.info("Cart is empty")
    else:
        df = pd.DataFrame(st.session_state.cart)
        df["Total"] = df["price"] * df["Quantity"]
        st.dataframe(df[["name", "category", "price", "Quantity", "Total"]], use_container_width=True)
        st.success(f"Grand Total: ₹ {df['Total'].sum()}")

        st.markdown("### Remove Item")
        for i, item in enumerate(st.session_state.cart):
            if st.button(f"Remove {item['name']}", key=f"remove_cart_{i}"):
                st.session_state.cart.pop(i)
                st.experimental_rerun()

# ——————— Wishlist ———————
elif page == "Wishlist":
    st.title("Wishlist Items")
    if not st.session_state.wishlist:
        st.info("Wishlist is empty")
    else:
        df = pd.DataFrame(st.session_state.wishlist)
        st.dataframe(df[["name", "category", "price"]], use_container_width=True)

        st.markdown("### Remove Item")
        for i, item in enumerate(st.session_state.wishlist):
            if st.button(f"Remove {item['name']}", key=f"remove_wish_{i}"):
                st.session_state.wishlist.pop(i)
                st.experimental_rerun()

# ——————— Records & Insights ———————
elif page == "Records & Insights":
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

# ——————— AI Assistant ———————
else:
    st.title("AI Assistant")

    if not st.session_state.gemini_key:
        st.warning("Enter your Gemini API key above to use the assistant")
    else:
        prompt = st.text_area("Ask the AI assistant something about your store data:")

        if st.button("Send to Gemini"):
            with st.spinner("Generating response…"):
                from google import generativeai as genai

                # configure with your Gemini API key
                genai.configure(api_key=st.session_state.gemini_key)

                # call the Gemini model
                ai_response = genai.Client().models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt
                )

                st.markdown("**Gemini Response:**")
                st.write(ai_response.text)
