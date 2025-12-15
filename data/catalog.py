import itertools

IMAGE_POOL = {
    "Shirts": [
        "https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf",
        "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab",
        "https://images.unsplash.com/photo-1503341455253-b2e723bb3dbb"
    ],
    "Jeans": [
        "https://images.unsplash.com/photo-1542272604-787c3835535d",
        "https://images.unsplash.com/photo-1512436991641-6745cdb1723f",
        "https://images.unsplash.com/photo-1582552938357-32b906df40cb"
    ],
    "Sarees": [
        "https://images.unsplash.com/photo-1583391733956-6c78276477e1",
        "https://images.unsplash.com/photo-1610030469983-98e550d6193c",
        "https://images.unsplash.com/photo-1622445275576-721325763afe"
    ],
    "Dhotis": [
        "https://images.unsplash.com/photo-1623071160280-98b33a776f85",
        "https://images.unsplash.com/photo-1618354691373-d851c5c3a990"
    ],
    "Kurtis": [
        "https://images.unsplash.com/photo-1618354691373-d851c5c3a990",
        "https://images.unsplash.com/photo-1594633312681-425c7b97ccd1"
    ],
    "Kids": [
        "https://images.unsplash.com/photo-1519238263530-99bdd11df2ea",
        "https://images.unsplash.com/photo-1604917869287-3ae73c77aefc"
    ]
}

PRODUCTS = []
pid = 1

for category, images in IMAGE_POOL.items():
    img_cycle = itertools.cycle(images)
    for i in range(1, 21):  # 20 items per category
        PRODUCTS.append({
            "id": pid,
            "name": f"{category} Item {i}",
            "category": category,
            "occasion": ["Casual", "Festive", "Traditional"][i % 3],
            "price": 999 + i * 120,
            "image": next(img_cycle)
        })
        pid += 1
