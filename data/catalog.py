PRODUCTS = []

IMAGE_QUERY = {
    "Shirts": "men-shirt-fashion",
    "Pants": "men-pants-fashion",
    "Jeans": "denim-jeans",
    "Dhotis": "men-dhoti-traditional",
    "Tops": "women-top-fashion",
    "Kurtis": "women-kurti",
    "Sarees": "indian-saree",
    "Skirts": "women-skirt-fashion",
    "Frocks": "girls-frock",
    "Tshirts": "kids-tshirt",
    "Shorts": "kids-shorts"
}

categories = [
    ("Men", ["Shirts", "Pants", "Jeans", "Dhotis"]),
    ("Women", ["Tops", "Kurtis", "Sarees", "Skirts"]),
    ("Boys", ["Shirts", "Shorts", "Jeans"]),
    ("Girls", ["Frocks", "Tops", "Skirts"]),
    ("Kids", ["Tshirts", "Shorts"]),
]

occasions = ["Casual", "Formal", "Festive", "Traditional"]

price_base = {
    "Casual": 999,
    "Formal": 1999,
    "Festive": 2999,
    "Traditional": 3499
}

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
                "price": price_base[occ] + (pid % 5) * 300,
                "image": f"https://source.unsplash.com/600x800/?{IMAGE_QUERY[item]}"
            })
            pid += 1
