class SalesAgent:
    def __init__(self):
        self.reco = RecommendationAgent()
        self.inventory = InventoryAgent()
        self.loyalty = LoyaltyAgent()
        self.payment = PaymentAgent()
        self.fulfillment = FulfillmentAgent()

    def handle(self, user_input, session):
        user_input = user_input.lower().strip()
        session["conversation"].append(("user", user_input))

        prefs = session["preferences"]
        stage = session["stage"]

        # ---------------- START ----------------
        if stage == "START":
            if any(cat in user_input for cat in ["shirt", "shirts", "pant", "pants", "jeans"]):
                prefs["category"] = user_input
                session["stage"] = "ASK_OCCASION"
                reply = "Sure 😊 Is this for a casual, formal, or festive occasion?"
            else:
                reply = "What are you shopping for today? (shirts, pants, jeans)"

        # ---------------- ASK OCCASION ----------------
        elif stage == "ASK_OCCASION":
            if user_input in ["casual", "formal", "festive"]:
                prefs["occasion"] = user_input
                session["stage"] = "ASK_BUDGET"
                reply = "Got it 👍 Do you have a budget range in mind?"
            else:
                reply = "Please choose one: casual, formal, or festive."

        # ---------------- ASK BUDGET ----------------
        elif stage == "ASK_BUDGET":
            prefs["budget"] = user_input
            session["stage"] = "RECOMMEND"

            reco = self.reco.run(session)
            inv = self.inventory.run(reco)
            final = self.loyalty.run(inv)

            session["cart"] = final["cart"]
            reply = final["message"]

        # ---------------- PAYMENT ----------------
        elif "pay" in user_input:
            payment = self.payment.run(session)
            final = self.fulfillment.run(payment)
            reply = final["message"]

        else:
            reply = "Let me know if you want to continue shopping 😊"

        session["conversation"].append(("assistant", reply))
        return reply
