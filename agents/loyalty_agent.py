class LoyaltyAgent:
    def run(self, data):
        total = sum(item["price"] for item in data["cart"])
        discount = int(total * 0.1)
        final_price = total - discount

        return {
            "cart": data["cart"],
            "message": f"""
🎉 Loyalty discount applied!

🛒 Total: ₹{total}
💸 Discount: ₹{discount}
✅ Payable: ₹{final_price}

Would you like to proceed to payment?
"""
        }

