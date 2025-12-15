class FulfillmentAgent:
    def run(self, payment):
        if payment["status"] == "success":
            return {
                "message": "🚚 Order confirmed! Delivery in 3–5 days."
            }
        return {
            "message": "❌ Payment failed. Please try another method."
        }

