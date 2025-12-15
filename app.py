import streamlit as st
import pandas as pd
from datetime import datetime
from catalog import PRODUCTS
from streamlit_chat import message
import openai

# ---------------- PAGE SETUP ----------------
st.set_page_config("OmniRetail IQ", layout="wide")

# ---------------- STYLE ----------------
st.markdown("""
<style>
body { background-color: #f6f8fc; }
.price { color: #2563eb; font-weight: 600; }
img { border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION STATE ----------------
for key in ["records", "cart", "wishlist", "chat_history"]:
    if key not in st.session_state:
        st.session_state[key] = []

# ---------------- SIDEBAR ----------------
st.sidebar.title("Retail Control Panel")
page = st.sidebar.radio("Navigate", ["Store", "Cart", "Wishlist", "Records & Insights", "AI Assistant"])

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
            if st.button("Add to Cart", key=f"cart_{i}"):
                st.session_state.cart.append(p)
            if st.button("Add to Wishlist", key=f"wish_{i}"):
                st.session_state.wishlist.append(p)

# ================= CART =================
elif page == "Cart":
    st.title("Cart Items")
    if not st.session_state.cart:
        st.info("Cart is empty")
    else:
        df = pd.DataFrame(st.session_state.cart)
        st.dataframe(df[["name", "category", "price"]], use_container_width=True)
        st.success(f"Total: ₹ {df['price'].sum()}")

# ================= WISHLIST =================
elif page == "Wishlist":
    st.title("Wishlist Items")
    if not st.session_state.wishlist:
        st.info("Wishlist is empty")
    else:
        df = pd.DataFrame(st.session_state.wishlist)
        st.dataframe(df[["name", "category", "price"]], use_container_width=True)

# ================= RECORDS & INSIGHTS =================
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

# ================= AI ASSISTANT =================
else:
    st.title("OmniRetail AI Assistant 🤖")
    user_input = st.text_input("You:", key="ai_input")

    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})

        openai.api_key = "YOUR_OPENAI_API_KEY"  # Replace with your key

        messages = [
            {"role": "system", "content": "You are OmniRetail IQ AI Assistant. Answer clearly about products, prices, categories, shopping advice."}
        ] + st.session_state.chat_history

        response = openai.chat.completions.create(
            model="gpt-5-mini",
            messages=messages
        )

        answer = response.choices[0].message.content
        st.session_state.chat_history.append({"role": "assistant", "content": answer})

    # Display chat history
    for chat in st.session_state.chat_history:
        if chat["role"] == "user":
            message(chat["content"], is_user=True)
        else:
            message(chat["content"])
