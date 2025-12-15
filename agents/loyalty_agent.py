class LoyaltyAgent:
    def run(self, data):
        price = data["cart"][0]["price"]
        discount = int(price * 0.1)
        final_price = price - discount

        data["message"] = f"""
🎉 Loyalty Offer Applied!

Original Price: ₹{price}  
Discount: ₹{discount}  
Final Price: ₹{final_price}
"""
        return data
