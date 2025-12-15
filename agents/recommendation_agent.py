from data.catalog import PRODUCTS

class RecommendationAgent:
    def run(self, preferences):
        recommendations = []

        for product in PRODUCTS:
            if (
                product["category"] == preferences["category"]
                and product["occasion"] == preferences["occasion"]
            ):
                recommendations.append(product)

        return recommendations
