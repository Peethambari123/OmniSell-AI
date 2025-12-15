from agents.recommendation_agent import RecommendationAgent
from agents.inventory_agent import InventoryAgent
from agents.loyalty_agent import LoyaltyAgent
from agents.payment_agent import PaymentAgent
from agents.fulfillment_agent import FulfillmentAgent

class SalesAgent:
    def __init__(self):
        self.reco = RecommendationAgent()
        self.inventory = InventoryAgent()
        self.loyalty = LoyaltyAgent()
        self.payment = PaymentAgent()
        self.fulfillment = FulfillmentAgent()

    def handle(self, user_input, session):
        session["conversation"].append(("user", user_input))

        if any(word in user_input.lower() for word in ["buy", "looking", "need"]):
            reco_data = self.reco.run(session)
            inv_data = self.inventory.run(reco_data)
            final = self.loyalty.run(inv_data)

            session["cart"] = final["cart"]
            reply = final["message"]

        elif "pay" in user_input.lower():
            payment = self.payment.run(session)
            final = self.fulfillment.run(payment)
            reply = final["message"]

        else:
            reply = "Sure 😊 Is this for a casual, formal, or festive occasion?"

        session["conversation"].append(("assistant", reply))
        return reply

