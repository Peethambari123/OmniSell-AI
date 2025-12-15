import random

class PaymentAgent:
    def run(self, session):
        if random.choice([True, False]):
            return {"status": "success"}
        return {"status": "failure"}

