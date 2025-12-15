from data.catalog import PRODUCTS

class RecommendationAgent:
    def recommend(self, preferences):
        results = []

        for product in PRODUCTS:
            if (
                product["category"] == preferences["category"]
                and product["occasion"] == preferences["occasion"]
            ):
                results.append(product)

        return results
