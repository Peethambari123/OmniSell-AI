class RecommendationAgent:
    def run(self, context):
        if context["category"] == "Shirts" and context["occasion"] == "Festive":
            product = {
                "name": "Festive Printed Cotton Shirt",
                "price": 2499
            }
        elif context["category"] == "Pants":
            product = {
                "name": "Slim Fit Casual Pants",
                "price": 2199
            }
        else:
            product = {
                "name": "Classic Denim Jeans",
                "price": 2799
            }

        return {
            "cart": [product]
        }
