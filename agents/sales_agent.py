class SalesAgent:
    def __init__(self):
        self.reco = RecommendationAgent()
        self.inventory = InventoryAgent()
        self.loyalty = LoyaltyAgent()
        self.payment = PaymentAgent()
        self.fulfillment = FulfillmentAgent()

    def handle(self, user_input, session):
        user_input = user_input.lower()
        session["conversation"].append(("user", user_input))

        prefs = session["preferences"]

        # Step 1: Capture category
        if "shirt" in user_input:
            prefs["category"] = "shirts"
            reply = "Nice choice 👕 Is this for a casual, formal, or festive occasion?"

        # Step 2: Capture occasion
        elif user_input in ["casual", "formal", "festive"]:
            prefs["occasion"] = user_input
            reply = "Got it 👍 Do you have a budget range in mind?"

        # Step 3: Capture budget
        elif any(word in user_input for word in ["under", "below", "above", "between"]):
            prefs["budget"] = user_input

            # Now enough info → recommend
            reco_data = self.reco.run(session)
            inv_data = self.inventory.run(reco_data)
            final = self.loyalty.run(inv_data)

            session["cart"] = final["cart"]
            reply = final["message"]

        # Step 4: Payment
        elif "pay" in user_input:
            payment = self.payment.run(session)
            final = self.fulfillment.run(payment)
            reply = final["message"]

        else:
            reply = "Tell me what you’re shopping for 😊 (e.g., shirts, jeans, dresses)"

        session["conversation"].append(("assistant", reply))
        return reply
