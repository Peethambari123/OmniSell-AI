PRODUCTS = []

categories = [
    ("Men", ["Shirts", "Pants", "Jeans", "Dhotis"]),
    ("Women", ["Tops", "Kurtis", "Sarees", "Skirts"]),
    ("Boys", ["Shirts", "Shorts", "Jeans"]),
    ("Girls", ["Frocks", "Tops", "Skirts"]),
    ("Kids", ["Tshirts", "Shorts"]),
]

occasions = ["Casual", "Formal", "Festive", "Traditional"]
price_map = {
    "Casual": 999,
    "Formal": 1999,
    "Festive": 2999,
    "Traditional": 3499
}

img = "https://images.unsplash.com/photo-1521334884684-d80222895322"

pid = 1
for gender, items in categories:
    for item in items:
        for occ in occasions:
            PRODUCTS.append({
                "id": pid,
                "name": f"{gender} {item} ({occ})",
                "gender": gender,
                "category": item,
                "occasion": occ,
                "price": price_map[occ] + (pid % 5) * 200,
                "image": img
            })
            pid += 1
