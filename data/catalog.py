PRODUCTS = []

IMAGE_MAP = {
    "Shirts": "https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf",
    "Pants": "https://images.unsplash.com/photo-1503342217505-b0a15ec3261c",
    "Jeans": "https://images.unsplash.com/photo-1542272604-787c3835535d",
    "Dhotis": "https://images.unsplash.com/photo-1623071160280-98b33a776f85",
    "Tops": "https://images.unsplash.com/photo-1495121605193-b116b5b09a04",
    "Kurtis": "https://images.unsplash.com/photo-1618354691373-d851c5c3a990",
    "Sarees": "https://images.unsplash.com/photo-1583391733956-6c78276477e1",
    "Skirts": "https://images.unsplash.com/photo-1594633312681-425c7b97ccd1",
    "Frocks": "https://images.unsplash.com/photo-1601972599720-0b8c5b84bde8",
    "Tshirts": "https://images.unsplash.com/photo-1521334884684-d80222895322",
    "Shorts": "https://images.unsplash.com/photo-1593032465171-8fdd5d5c8b68"
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
                "price": price_base[occ] + (pid % 4) * 250,
                "image": IMAGE_MAP.get(item)
            })
            pid += 1
